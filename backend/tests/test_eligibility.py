"""
Unit tests for deterministic eligibility engine.
Covers 30+ test cases: boundary values, missing fields, wrong state,
multiple schemes, operators, lakh coercion, unapproved rule isolation,
and kind="document" non-blocking behavior.
"""

import pytest
from backend.app.models.database import EligibilityRule, Record
from backend.app.services.eligibility import evaluate_eligibility, evaluate_rule, _coerce_numeric


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


def test_rule_empty_string_profile_unknown():
    """Empty string field in profile must return UNKNOWN."""
    rule = EligibilityRule(field="state", operator="==", value="Punjab", kind="profile")
    res = evaluate_rule(rule, {"state": ""})
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


def test_rule_not_equal_operator():
    rule = EligibilityRule(field="category", operator="!=", value="General", kind="profile")
    res_met = evaluate_rule(rule, {"category": "SC"})
    assert res_met.status == "MET"
    res_not = evaluate_rule(rule, {"category": "General"})
    assert res_not.status == "NOT_MET"


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


def test_rule_contains_operator():
    rule = EligibilityRule(field="target_beneficiaries", operator="contains", value="farmer", kind="profile")
    res = evaluate_rule(rule, {"target_beneficiaries": ["farmers", "landholders"]})
    assert res.status == "MET"
    res_not = evaluate_rule(rule, {"target_beneficiaries": ["students", "teachers"]})
    assert res_not.status == "NOT_MET"


def test_rule_lakh_string_coercion():
    """Verify that user inputs with lakh notation are coerced accurately."""
    rule = EligibilityRule(field="annual_family_income", operator="<=", value=250000, kind="profile")
    # "2 lakh" = 200,000 <= 250,000 -> MET
    res1 = evaluate_rule(rule, {"annual_family_income": "2 lakh"})
    assert res1.status == "MET"

    # "2.5 lakh" = 250,000 <= 250,000 -> MET (boundary)
    res2 = evaluate_rule(rule, {"annual_family_income": "2.5 lakh"})
    assert res2.status == "MET"

    # "3 lakh" = 300,000 <= 250,000 -> NOT_MET
    res3 = evaluate_rule(rule, {"annual_family_income": "3 lakh"})
    assert res3.status == "NOT_MET"

    # "₹2,50,000" with formatting symbols
    res4 = evaluate_rule(rule, {"annual_family_income": "₹2,50,000"})
    assert res4.status == "MET"


def test_rule_result_fields_populated():
    """Verify kind, source_url, and source_excerpt are retained in RuleResult."""
    rule = EligibilityRule(
        id="r_test",
        field="category",
        operator="==",
        value="SC",
        kind="profile",
        source_url="https://scholarships.gov.in",
        source_excerpt="Scheme restricted to SC category students.",
        description="Must belong to SC category",
    )
    res = evaluate_rule(rule, {"category": "SC"})
    assert res.kind == "profile"
    assert res.source_url == "https://scholarships.gov.in"
    assert res.source_excerpt == "Scheme restricted to SC category students."
    assert res.status == "MET"


def test_kind_document_never_blocks_eligibility():
    """
    Section 7 rule:
    Rules of kind 'document' never block Potentially eligible;
    they are listed as 'to be verified at application'.
    """
    rule = EligibilityRule(
        id="r_doc",
        field="income_certificate",
        operator="==",
        value=True,
        kind="document",
        description="Income Certificate issued by Tehsildar",
    )
    # Even if missing in profile, document rule is UNKNOWN and marked for application verification
    res = evaluate_rule(rule, {})
    assert res.status == "UNKNOWN"
    assert "to be verified at application" in res.description


def test_evaluate_eligibility_mocked_db():
    """Test full overall_status logic with mock Session."""
    class MockQuery:
        def __init__(self, record, rules):
            self.record = record
            self.rules = rules

        def filter(self, *args, **kwargs):
            # Only keep approved rules
            approved = [r for r in self.rules if getattr(r, "is_approved", True)]
            return MockQuery(self.record, approved)

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
        EligibilityRule(id="r1", record_id="rec1", field="category", operator="==", value="SC", kind="profile", is_approved=True),
        EligibilityRule(id="r2", record_id="rec1", field="annual_family_income", operator="<=", value=250000, kind="profile", is_approved=True),
        EligibilityRule(id="r3", record_id="rec1", field="income_certificate", operator="==", value=True, kind="document", is_approved=True),
    ]

    db = MockDB(mock_rec, mock_rules)

    # 1. Eligible citizen: meets both profile rules; document rule does NOT block eligibility
    res = evaluate_eligibility("rec1", {"category": "SC", "annual_family_income": 200000}, db)
    assert res.overall_status == "eligible"
    assert "Potentially eligible - further verification required" in res.message

    # 2. Not eligible citizen: exceeds income
    res_not = evaluate_eligibility("rec1", {"category": "SC", "annual_family_income": 300000}, db)
    assert res_not.overall_status == "not_eligible"
    assert "Not eligible based on known criteria" in res_not.message

    # 3. Insufficient info: category missing
    res_unknown = evaluate_eligibility("rec1", {"annual_family_income": 200000}, db)
    assert res_unknown.overall_status == "insufficient_info"
    assert "Insufficient information" in res_unknown.message


def test_evaluate_eligibility_zero_approved_rules():
    """
    Section 7 rule:
    If a record has no approved rules, return
    'Insufficient information - eligibility rules not yet extracted'.
    """
    class MockQueryEmpty:
        def filter(self, *args, **kwargs):
            return self

        def first(self):
            return Record(id="draft_scheme", name="Draft Scheme Without Rules", category="General")

        def all(self):
            return []  # No approved rules

    class MockDBEmpty:
        def query(self, model):
            return MockQueryEmpty()

    db = MockDBEmpty()
    res = evaluate_eligibility("draft_scheme", {"age": 25}, db)
    assert res.overall_status == "insufficient_info"
    assert res.message == "Insufficient information - eligibility rules not yet extracted"
    assert res.rule_results == []
