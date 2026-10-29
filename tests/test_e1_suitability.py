"""Known-truth extension cases; no restricted input needed."""

import pytest

pd = pytest.importorskip("pandas")

from agrisight.e1_suitability import input_checks, numeric_summary, skip_checks


def test_skip_logic_distinguishes_nonapplicable_from_missing():
    frame = pd.DataFrame({"s02_q07": [1, 1, 2, 2], "s02_q08": [1, None, None, 2],
                          "s02_q09": [99, 88, None, None]})
    assert skip_checks(frame) == {
        "s02_q08_missing_when_yes": 1, "s02_q08_other_when_yes": 0,
        "s02_q08_populated_when_no": 1, "s02_q09_missing_when_yes": 0,
        "s02_q09_other_when_yes": 1, "s02_q09_populated_when_no": 0,
    }


def test_numeric_quantity_categories_are_exhaustive():
    assert numeric_summary(pd.Series([None, float("inf"), -1, 0, 2])) == {
        "missing": 1, "nonfinite": 1, "negative": 1, "zero": 1, "positive": 1,
    }


def test_input_grain_is_household_and_type_not_person():
    hh = pd.DataFrame({"hhid": ["A"]})
    frame = pd.DataFrame({"hhid": ["A", "A", "B", None],
                          "s03c_inputType__id": [1, 1, 1, 2],
                          "s03c_q01": [2, 0, -1, None]})
    result = input_checks(frame, hh)
    assert result["rows"] == 4
    assert result["duplicate_excess"] == 1
    assert result["missing_key_rows"] == 1
    assert result["orphan_household_rows"] == 1
    assert result["distinct_complete_keys"] == 2


def test_empty_quantities_and_wrong_types():
    assert set(numeric_summary(pd.Series([], dtype=float)).values()) == {0}
    with pytest.raises(TypeError, match="numeric"):
        numeric_summary(pd.Series(["unknown"]))
