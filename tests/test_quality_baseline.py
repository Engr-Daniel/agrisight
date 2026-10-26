"""M0-05 validation-contract tests using only Python standard library."""
from agrisight.quality_baseline import example_inputs, validate_roles


def test_valid_data_has_no_issues():
    valid, _ = example_inputs()
    assert validate_roles(valid) == []


def test_invalid_fixture_has_expected_codes():
    _, invalid = example_inputs()
    issues = validate_roles(invalid)
    actual = {(issue.row, issue.field, issue.code) for issue in issues}
    assert actual == {
        (1, "role_id", "duplicate_role_id"),
        (1, "person_id", "missing_required"),
        (1, "kind", "invalid_category"),
        (1, "status", "invalid_category"),
        (1, "complete", "invalid_boolean"),
    }


def test_empty_rows_are_valid():
    assert validate_roles([]) == []


def test_missing_columns_are_flagged():
    issues = validate_roles([{}])
    assert {i.field for i in issues} == {"role_id", "person_id", "kind", "status", "complete"}


def test_does_not_change_original_submissions():
    _, rows = example_inputs()
    before = [r.copy() for r in rows]
    validate_roles(rows)
    assert rows == before
