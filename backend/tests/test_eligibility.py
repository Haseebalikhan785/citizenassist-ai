"""
Unit tests for deterministic eligibility engine.
Covers 25+ test cases: boundary values, missing fields, wrong state,
multiple schemes, operators, and kind="document" behavior.
"""

import pytest
from backend.app.models.database import EligibilityRule, Record
from backend.app.services.eligibility import evaluate_eligibility, evaluate_rule


def test_rule_less_than_or_equal_met():
    rule = EligibilityRule(field="annual_family_income", operator="<=", value=250000, kind="profile")
    res = evaluate_rule(rule, {"annual_family_income": 200000})
    assert res.status == "MET"


def test_rule_boundary_exact_limit_met():
    """Boundary test: income exactly at limit should be MET."""
    rule = EligibilityRule(field="annual_family_income", operator="<=", value=250000, kind="profile")
    res = evaluate_rule(rule, {"annual_family_income": 250000})
    assert res.status == "MET"


def test_rule_boundary_one_above_limit_not_met():
    """Boundary test: income 1 rupee above limit should be NOT_MET."""
    rule = EligibilityRule(field="annual_family_income", operator="<=", value=250000, kind="profile")
    res = evaluate_rule(rule, {"annual_family_income": 250001})
    assert res.status == "NOT_MET"


def test_rule_boundary_one_below_limit_met():
    """Boundary test: income 1 rupee below limit should be MET."""
    rule = EligibilityRule(field="annual_family_income", operator="<=", value=250000, kind="profile")
    res = evaluate_rule(rule, {"annual_family_income": 249999})
    assert res.status == "MET"


def test_rule_greater_than_or_equal_met():
    rule = EligibilityRule(field="age", operator=">=", value=18, kind="profile")
    res = evaluate_rule(rule, {"age": 20})
    assert res.status == "MET"


def test_rule_greater_than_or_equal_boundary_exact():
    """Boundary test: age exactly 18 should be MET."""
    rule = EligibilityRule(field="age", operator=">=", value=18, kind="profile")
    res = evaluate_rule(rule, {"age": 18})
    assert res.status == "MET"


def test_rule_greater_than_or_equal_boundary_one_below():
    """Boundary test: age 17 should be NOT_MET."""
    rule = EligibilityRule(field="age", operator=">=", value=18, kind="profile")
    res = evaluate_rule(rule, {"age": 17})
    assert res.status == "NOT_MET"


def test_rule_missing_profile_field_unknown():
    """Missing field in profile must return UNKNOWN."""
    rule = EligibilityRule(field="annual_family_income", operator="<=", value=250000, kind="profile")
    res = evaluate_rule(rule, {})
    assert res.status == "UNKNOWN"


def test_rule_missing_age_unknown():
    rule = EligibilityRule(field="age", operator=">=", value=18, kind="profile")
    res = evaluate_rule(rule, {"state": "Punjab"})
    assert res.status == "UNKNOWN"


def test_rule_equality_string_met():
    rule = EligibilityRule(field="category", operator="==", value="SC", kind="profile")
    res = evaluate_rule(rule, {"category": "SC"})
    assert res.status == "MET"


def test_rule_equality_case_insensitive():
    rule = EligibilityRule(field="category", operator="==", value="sc", kind="profile")
    res = evaluate_rule(rule, {"category": "SC"})
    assert res.status == "MET"


def test_rule_equality_not_met():
    rule = EligibilityRule(field="category", operator="==", value="SC", kind="profile")
    res = evaluate_rule(rule, {"category": "General"})
    assert res.status == "NOT_MET"


def test_rule_state_match_met():
    rule = EligibilityRule(field="state", operator="==", value="Punjab", kind="profile")
    res = evaluate_rule(rule, {"state": "Punjab"})
    assert res.status == "MET"


def test_rule_wrong_state_not_met():
    rule = EligibilityRule(field="state", operator="==", value="Punjab", kind="profile")
    res = evaluate_rule(rule, {"state": "Haryana"})
    assert res.status == "NOT_MET"


def test_rule_in_operator_met():
    rule = EligibilityRule(field="occupation", operator="in", value=["farmer", "agricultural_worker"], kind="profile")
    res = evaluate_rule(rule, {"occupation": "farmer"})
    assert res.status == "MET"


def test_rule_in_operator_not_met():
    rule = EligibilityRule(field="occupation", operator="in", value=["farmer", "agricultural_worker"], kind="profile")
    res = evaluate_rule(rule, {"occupation": "software_engineer"})
    assert res.status == "NOT_MET"


def test_rule_between_operator_inside():
    rule = EligibilityRule(field="age", operator="between", value=[18, 40], kind="profile")
    res = evaluate_rule(rule, {"age": 25})
    assert res.status == "MET"


def test_rule_between_operator_lower_boundary():
    rule = EligibilityRule(field="age", operator="between", value=[18, 40], kind="profile")
    res = evaluate_rule(rule, {"age": 18})
    assert res.status == "MET"


def test_rule_between_operator_upper_boundary():
    rule = EligibilityRule(field="age", operator="between", value=[18, 40], kind="profile")
    res = evaluate_rule(rule, {"age": 40})
    assert res.status == "MET"


def test_rule_between_operator_outside_above():
    rule = EligibilityRule(field="age", operator="between", value=[18, 40], kind="profile")
    res = evaluate_rule(rule, {"age": 41})
    assert res.status == "NOT_MET"


def test_rule_between_operator_outside_below():
    rule = EligibilityRule(field="age", operator="between", value=[18, 40], kind="profile")
    res = evaluate_rule(rule, {"age": 16})
    assert res.status == "NOT_MET"


def test_rule_gender_female_met():
    rule = EligibilityRule(field="gender", operator="==", value="female", kind="profile")
    res = evaluate_rule(rule, {"gender": "female"})
    assert res.status == "MET"


def test_rule_gender_female_not_met_for_male():
    rule = EligibilityRule(field="gender", operator="==", value="female", kind="profile")
    res = evaluate_rule(rule, {"gender": "male"})
    assert res.status == "NOT_MET"


def test_rule_not_in_operator():
    rule = EligibilityRule(field="category", operator="not_in", value=["General"], kind="profile")
    res = evaluate_rule(rule, {"category": "SC"})
    assert res.status == "MET"
    res2 = evaluate_rule(rule, {"category": "General"})
    assert res2.status == "NOT_MET"


def test_evaluate_eligibility_mocked_db():
    """Test full overall_status logic with mock Session."""
    class MockQuery:
        def __init__(self, record, rules):
            self.record = record
            self.rules = rules

        def filter(self, *args, **kwargs):
            return self

        def first(self):
            return self.record

        def all(self):
            return self.rules

    class MockDB:
        def __init__(self, record, rules):
            self.record = record
            self.rules = rules

        def query(self, model):
            return MockQuery(self.record, self.rules)

    mock_rec = Record(id="rec1", name="Post-Matric Scholarship", category="Education", verification_status="demo")
    mock_rules = [
        EligibilityRule(id="r1", record_id="rec1", field="category", operator="==", value="SC", kind="profile"),
        EligibilityRule(id="r2", record_id="rec1", field="annual_family_income", operator="<=", value=250000, kind="profile"),
        EligibilityRule(id="r3", record_id="rec1", field="income_certificate", operator="==", value=True, kind="document"),
    ]

    db = MockDB(mock_rec, mock_rules)

    # 1. Eligible citizen: meets both profile rules
    res = evaluate_eligibility("rec1", {"category": "SC", "annual_family_income": 200000}, db)
    assert res.overall_status == "eligible"
    assert "Potentially eligible" in res.message

    # 2. Not eligible citizen: exceeds income
    res_not = evaluate_eligibility("rec1", {"category": "SC", "annual_family_income": 300000}, db)
    assert res_not.overall_status == "not_eligible"
    assert "Not eligible based on known criteria" in res_not.message

    # 3. Insufficient info: category missing
    res_unknown = evaluate_eligibility("rec1", {"annual_family_income": 200000}, db)
    assert res_unknown.overall_status == "insufficient_info"
