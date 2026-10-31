"""
Deterministic eligibility engine.

Evaluates structured rules against a citizen profile to determine eligibility
for government schemes and services without LLM hallucination.
"""

import logging
import re
from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.database import EligibilityRule, Record
from backend.app.models.schemas import EligibilityResult, RuleResult

logger = logging.getLogger(__name__)


def _coerce_numeric(val: Any) -> float | None:
    """
    Coerce a value to a float, handling numbers, strings with commas,
    currency signs, and lakh notations (e.g. '2.5 lakh' -> 250000).
    """
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)

    s = str(val).strip().lower()
    if not s:
        return None

    # Handle lakh notation: e.g. "2.5 lakh", "2 lakh", "2.5 lacs"
    lakh_match = re.search(r"^(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)$", s)
    if lakh_match:
        try:
            return float(lakh_match.group(1)) * 100000.0
        except ValueError:
            pass

    # Strip currency symbols and formatting commas
    cleaned = re.sub(r"[₹,rs\.\s]", "", s)
    # Check if cleaned is numeric
    try:
        return float(cleaned)
    except (TypeError, ValueError):
        # Fallback to direct float conversion of original string if possible
        try:
            return float(s)
        except (TypeError, ValueError):
            return None


def evaluate_rule(rule: EligibilityRule, profile: dict[str, Any]) -> RuleResult:
    """
    Evaluate a single eligibility rule against a user profile.

    Returns a RuleResult with status: MET, NOT_MET, or UNKNOWN.
    Rules of kind='document' are marked as to be verified at application.
    """
    field = rule.field
    operator = rule.operator
    rule_value = rule.value
    kind = rule.kind or "profile"
    source_url = rule.source_url
    source_excerpt = rule.source_excerpt
    desc = rule.description or f"Rule for {field}"

    user_value = profile.get(field)

    # Missing profile value
    if user_value is None or user_value == "":
        status = "UNKNOWN"
        if kind == "document":
            status = "UNKNOWN"
            desc = f"{desc} (to be verified at application)"
        return RuleResult(
            rule_id=rule.id,
            field=field,
            operator=operator,
            value=rule_value,
            status=status,
            kind=kind,
            source_url=source_url,
            source_excerpt=source_excerpt,
            description=desc,
            user_value=None,
        )

    # Document-kind rules: verify if present, otherwise mark for application verification
    if kind == "document":
        desc = f"{desc} (to be verified at application)"
        # If user explicitly indicated availability
        if isinstance(user_value, bool):
            status = "MET" if user_value else "UNKNOWN"
        elif isinstance(user_value, list):
            status = "MET" if any(str(v).lower() == str(rule_value).lower() for v in user_value) else "UNKNOWN"
        else:
            status = "MET" if str(user_value).lower() in ["true", "yes", "available", str(rule_value).lower()] else "UNKNOWN"

        return RuleResult(
            rule_id=rule.id,
            field=field,
            operator=operator,
            value=rule_value,
            status=status,
            kind=kind,
            source_url=source_url,
            source_excerpt=source_excerpt,
            description=desc,
            user_value=user_value,
        )

    # Profile-kind rules evaluation
    met = False
    try:
        if operator == "==":
            met = str(user_value).strip().lower() == str(rule_value).strip().lower()

        elif operator == "!=":
            met = str(user_value).strip().lower() != str(rule_value).strip().lower()

        elif operator == "<=":
            uv = _coerce_numeric(user_value)
            rv = _coerce_numeric(rule_value)
            if uv is not None and rv is not None:
                met = uv <= rv
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN", kind=kind,
                    source_url=source_url, source_excerpt=source_excerpt,
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
                    value=rule_value, status="UNKNOWN", kind=kind,
                    source_url=source_url, source_excerpt=source_excerpt,
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
                    value=rule_value, status="UNKNOWN", kind=kind,
                    source_url=source_url, source_excerpt=source_excerpt,
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
                    value=rule_value, status="UNKNOWN", kind=kind,
                    source_url=source_url, source_excerpt=source_excerpt,
                    description=f"Cannot compare: {user_value} > {rule_value}",
                    user_value=user_value,
                )

        elif operator == "in":
            if isinstance(rule_value, (list, tuple, set)):
                targets = [str(v).strip().lower() for v in rule_value]
                if isinstance(user_value, (list, tuple, set)):
                    met = any(str(u).strip().lower() in targets for u in user_value)
                else:
                    met = str(user_value).strip().lower() in targets
            else:
                met = str(user_value).strip().lower() == str(rule_value).strip().lower()

        elif operator == "not_in":
            if isinstance(rule_value, (list, tuple, set)):
                targets = [str(v).strip().lower() for v in rule_value]
                if isinstance(user_value, (list, tuple, set)):
                    met = not any(str(u).strip().lower() in targets for u in user_value)
                else:
                    met = str(user_value).strip().lower() not in targets
            else:
                met = str(user_value).strip().lower() != str(rule_value).strip().lower()

        elif operator == "between":
            uv = _coerce_numeric(user_value)
            low, high = None, None
            if isinstance(rule_value, (list, tuple)) and len(rule_value) >= 2:
                low = _coerce_numeric(rule_value[0])
                high = _coerce_numeric(rule_value[1])
            elif isinstance(rule_value, str) and ("-" in rule_value or "to" in rule_value):
                parts = re.split(r"[-–—]|(?:\bto\b)", rule_value)
                if len(parts) >= 2:
                    low = _coerce_numeric(parts[0])
                    high = _coerce_numeric(parts[1])

            if uv is not None and low is not None and high is not None:
                met = low <= uv <= high
            else:
                return RuleResult(
                    rule_id=rule.id, field=field, operator=operator,
                    value=rule_value, status="UNKNOWN", kind=kind,
                    source_url=source_url, source_excerpt=source_excerpt,
                    description=f"Invalid between range for {field}: {rule_value}",
                    user_value=user_value,
                )

        elif operator == "contains":
            rv = str(rule_value).strip().lower()
            if isinstance(user_value, (list, tuple, set)):
                met = any(rv in str(v).strip().lower() for v in user_value)
            else:
                met = rv in str(user_value).strip().lower()

        else:
            logger.warning("Unknown operator: %s", operator)
            return RuleResult(
                rule_id=rule.id, field=field, operator=operator,
                value=rule_value, status="UNKNOWN", kind=kind,
                source_url=source_url, source_excerpt=source_excerpt,
                description=f"Unknown operator: {operator}",
                user_value=user_value,
            )

    except Exception as e:
        logger.error("Error evaluating rule %s: %s", rule.id, e)
        return RuleResult(
            rule_id=rule.id, field=field, operator=operator,
            value=rule_value, status="UNKNOWN", kind=kind,
            source_url=source_url, source_excerpt=source_excerpt,
            description=f"Evaluation error: {e}",
            user_value=user_value,
        )

    return RuleResult(
        rule_id=rule.id,
        field=field,
        operator=operator,
        value=rule_value,
        status="MET" if met else "NOT_MET",
        kind=kind,
        source_url=source_url,
        source_excerpt=source_excerpt,
        description=desc,
        user_value=user_value,
    )


def evaluate_eligibility(record_id: str, profile: dict[str, Any], db: Session) -> EligibilityResult:
    """
    Evaluate all approved eligibility rules for a record against a user profile.

    Deterministic logic strictly adhering to BUILD_BRIEF Section 7:
    - Only approved rules are evaluated (is_approved == True).
    - If a record has no approved rules:
        return 'Insufficient information - eligibility rules not yet extracted'.
    - Rules of kind 'document' never block Potentially eligible;
        they are listed as 'to be verified at application'.
    - Overall result:
        any profile rule NOT_MET -> 'Not eligible based on known criteria'
        none NOT_MET and all profile rules MET -> 'Potentially eligible - further verification required'
        otherwise -> 'Insufficient information'
    """
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        return EligibilityResult(
            record_id=record_id,
            record_name="Unknown",
            overall_status="error",
            message="Record not found",
        )

    # Strictly evaluate only approved rules
    rules = (
        db.query(EligibilityRule)
        .filter(
            EligibilityRule.record_id == record_id,
            EligibilityRule.is_approved.is_(True),
        )
        .all()
    )

    if not rules:
        return EligibilityResult(
            record_id=record_id,
            record_name=record.name,
            overall_status="insufficient_info",
            message="Insufficient information - eligibility rules not yet extracted",
            rule_results=[],
            category=record.category,
            verification_status=record.verification_status or "demo",
        )

    rule_results: list[RuleResult] = []
    profile_total = 0
    profile_met = 0
    profile_not_met = 0
    profile_unknown = 0

    for rule in rules:
        result = evaluate_rule(rule, profile)
        rule_results.append(result)

        # Rules of kind "document" never block Potentially eligible
        if rule.kind == "document":
            continue

        profile_total += 1
        if result.status == "MET":
            profile_met += 1
        elif result.status == "NOT_MET":
            profile_not_met += 1
        else:
            profile_unknown += 1

    # Status calculation strictly according to Section 7
    if profile_not_met > 0:
        overall_status = "not_eligible"
        message = "Not eligible based on known criteria"
    elif profile_total > 0 and profile_met == profile_total:
        overall_status = "eligible"
        message = "Potentially eligible - further verification required"
    else:
        overall_status = "insufficient_info"
        message = "Insufficient information"

    return EligibilityResult(
        record_id=record_id,
        record_name=record.name,
        overall_status=overall_status,
        message=message,
        rule_results=rule_results,
        category=record.category,
        verification_status=record.verification_status or "demo",
    )
