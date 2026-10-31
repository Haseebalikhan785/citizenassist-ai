"""
Deterministic eligibility engine.

Evaluates structured rules against a citizen profile to determine eligibility
for government schemes and services.
"""

import logging
from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.database import EligibilityRule, Record
from backend.app.models.schemas import EligibilityResult, RuleResult

logger = logging.getLogger(__name__)


def _coerce_numeric(val: Any) -> float | None:
    """Try to coerce a value to a float."""
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def evaluate_rule(rule: EligibilityRule, profile: dict[str, Any]) -> RuleResult:
    """
    Evaluate a single eligibility rule against a user profile.

    Returns a RuleResult with status: MET, NOT_MET, or UNKNOWN.
    """
    field = rule.field
    operator = rule.operator
    rule_value = rule.value

    user_value = profile.get(field)

    # If the profile doesn't contain the field, result is UNKNOWN
    if user_value is None:
        return RuleResult(
            rule_id=rule.id,
            field=field,
            operator=operator,
            value=rule_value,
            status="UNKNOWN",
            description=rule.description or f"Profile missing field: {field}",
            user_value=None,
        )

    met = False

    try:
        if operator == "==":
            # String or numeric equality
            met = str(user_value).lower() == str(rule_value).lower()

        elif operator == "<=":
            uv = _coerce_numeric(user_value)
            rv = _coerce_numeric(rule_value)
            if uv is not None and rv is not None:
                met = uv <= rv
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN",
                    description=f"Cannot compare: {user_value} <= {rule_value}",
                    user_value=user_value,
                )

        elif operator == ">=":
            uv = _coerce_numeric(user_value)
            rv = _coerce_numeric(rule_value)
            if uv is not None and rv is not None:
                met = uv >= rv
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN",
                    description=f"Cannot compare: {user_value} >= {rule_value}",
                    user_value=user_value,
                )

        elif operator == "<":
            uv = _coerce_numeric(user_value)
            rv = _coerce_numeric(rule_value)
            if uv is not None and rv is not None:
                met = uv < rv
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN",
                    description=f"Cannot compare: {user_value} < {rule_value}",
                    user_value=user_value,
                )

        elif operator == ">":
            uv = _coerce_numeric(user_value)
            rv = _coerce_numeric(rule_value)
            if uv is not None and rv is not None:
                met = uv > rv
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN",
                    description=f"Cannot compare: {user_value} > {rule_value}",
                    user_value=user_value,
                )

        elif operator == "in":
            # User value should be in the list (rule_value is a list)
            if isinstance(rule_value, list):
                uv_lower = str(user_value).lower()
                met = uv_lower in [str(v).lower() for v in rule_value]
            else:
                met = str(user_value).lower() == str(rule_value).lower()

        elif operator == "not_in":
            if isinstance(rule_value, list):
                uv_lower = str(user_value).lower()
                met = uv_lower not in [str(v).lower() for v in rule_value]
            else:
                met = str(user_value).lower() != str(rule_value).lower()

        elif operator == "between":
            # rule_value should be [min, max]
            uv = _coerce_numeric(user_value)
            if uv is not None and isinstance(rule_value, list) and len(rule_value) == 2:
                low = _coerce_numeric(rule_value[0])
                high = _coerce_numeric(rule_value[1])
                if low is not None and high is not None:
                    met = low <= uv <= high
                else:
                    return RuleResult(
                        rule_id=rule.id, field=field, operator=operator,
                        value=rule_value, status="UNKNOWN",
                        description=f"Cannot compare range for {field}",
                        user_value=user_value,
                    )
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN",
                    description=f"Invalid between value for {field}",
                    user_value=user_value,
                )

        elif operator == "contains":
            # Check if user_value (a list or string) contains rule_value
            if isinstance(user_value, list):
                met = str(rule_value).lower() in [str(v).lower() for v in user_value]
            else:
                met = str(rule_value).lower() in str(user_value).lower()

        else:
            logger.warning("Unknown operator: %s", operator)
            return RuleResult(
                rule_id=rule.id, field=field, operator=operator,
                value=rule_value, status="UNKNOWN",
                description=f"Unknown operator: {operator}",
                user_value=user_value,
            )

    except Exception as e:
        logger.error("Error evaluating rule %s: %s", rule.id, e)
        return RuleResult(
            rule_id=rule.id, field=field, operator=operator,
            value=rule_value, status="UNKNOWN",
            description=f"Evaluation error: {e}",
            user_value=user_value,
        )

    return RuleResult(
        rule_id=rule.id,
        field=field,
        operator=operator,
        value=rule_value,
        status="MET" if met else "NOT_MET",
        description=rule.description,
        user_value=user_value,
    )


def evaluate_eligibility(record_id: str, profile: dict[str, Any], db: Session) -> EligibilityResult:
    """
    Evaluate all eligibility rules for a record against a user profile.

    Logic:
    - Document rules (kind='document') never block eligibility.
    - Any profile rule NOT_MET → "Not eligible based on known criteria"
    - All profile rules MET → "Potentially eligible - further verification required"
    - Otherwise → "Insufficient information - provide more details"
    """
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        return EligibilityResult(
            record_id=record_id,
            record_name="Unknown",
            overall_status="error",
            message="Record not found",
        )

    rules = db.query(EligibilityRule).filter(EligibilityRule.record_id == record_id).all()

    if not rules:
        return EligibilityResult(
            record_id=record_id,
            record_name=record.name,
            overall_status="insufficient_info",
            message="No eligibility rules defined. Check the official portal for eligibility criteria.",
            category=record.category,
            verification_status=record.verification_status,
        )

    rule_results: list[RuleResult] = []
    profile_met = 0
    profile_not_met = 0
    profile_unknown = 0
    profile_total = 0

    for rule in rules:
        result = evaluate_rule(rule, profile)
        rule_results.append(result)

        # Only profile rules affect eligibility determination
        if rule.kind == "profile":
            profile_total += 1
            if result.status == "MET":
                profile_met += 1
            elif result.status == "NOT_MET":
                profile_not_met += 1
            else:
                profile_unknown += 1

    # Determine overall status
    if profile_not_met > 0:
        overall_status = "not_eligible"
        message = "Not eligible based on known criteria. Some eligibility conditions are not met."
    elif profile_total > 0 and profile_met == profile_total:
        overall_status = "eligible"
        message = "Potentially eligible - further verification required on the official portal."
    elif profile_unknown > 0:
        overall_status = "insufficient_info"
        message = "Insufficient information - please provide more profile details for a complete assessment."
    else:
        overall_status = "insufficient_info"
        message = "No profile-level eligibility rules to evaluate."

    return EligibilityResult(
        record_id=record_id,
        record_name=record.name,
        overall_status=overall_status,
        message=message,
        rule_results=rule_results,
        category=record.category,
        verification_status=record.verification_status,
    )
