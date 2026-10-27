"""Dependency-free coverage of comparison case construction."""
from agrisight.framework_comparison import cases


def test_expected_scenarios():
    assert set(cases()) == {
        "valid", "empty_person_id", "empty_role_id", "invalid_kind",
        "invalid_status", "invalid_boolean", "duplicate_role_id",
    }


def test_source_cases_are_isolated():
    scenarios = cases()
    scenarios["invalid_kind"][0]["role_id"] = "MUTATED"
    assert scenarios["valid"][0]["role_id"] == "R1"


def test_valid_case_allows_multiple_roles_per_person():
    valid = cases()["valid"]
    assert valid[0]["person_id"] == valid[1]["person_id"]
    assert valid[0]["role_id"] != valid[1]["role_id"]
