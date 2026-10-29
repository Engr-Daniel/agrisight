"""Synthetic cases only; CI never requires or publishes real survey files."""

import io
import zipfile

import pytest

pd = pytest.importorskip("pandas", reason="Install the e1 extra to run analytical tests")
StataMissingValue = pd.io.stata.StataMissingValue

from agrisight.e1_profile import (
    HOUSEHOLD_COLUMNS,
    identifier,
    profile_frames,
    read_selected,
    response,
    run,
)


def frames():
    households = pd.DataFrame({"hhid": ["A", "A", "B", None],
                               "final_weight": [1, 0, float("inf"), None]})
    plots = pd.DataFrame({"hhid": ["A", "A", "B", "C", None],
                         "s02_plotRoster__id": [1, 1, 1, 2, 3],
                         "s02_q07": [1, 2, None, 9, 1],
                         "final_weight": [1, 2, -1, 0, None]})
    return households, plots


def test_known_truth_and_sql_reconciliation():
    hh, pp = frames()
    original = pp.copy(deep=True)
    result = profile_frames(hh, pp)
    assert result["counts"] == {
        "household_rows": 4, "household_missing_key_rows": 1,
        "household_distinct_complete_keys": 2, "household_duplicate_excess": 1,
        "plot_rows": 5, "plot_missing_key_rows": 1, "plot_distinct_complete_keys": 3,
        "plot_duplicate_excess": 1, "plot_missing_household_id_rows": 1,
        "orphan_plot_rows": 1, "irrigation_yes": 2, "irrigation_no": 1,
        "irrigation_missing": 1, "irrigation_other": 1,
    }
    assert result["household_weights"] == {
        "missing": 1, "nonfinite": 1, "nonpositive": 1, "positive_finite": 1,
    }
    pd.testing.assert_frame_equal(pp, original)


def test_empty_input_has_zero_counts():
    hh, pp = frames()
    assert set(profile_frames(hh.iloc[:0], pp.iloc[:0])["counts"].values()) == {0}


def test_blank_keys_and_composite_plot_grain():
    hh, pp = frames()
    hh = hh.iloc[:2].copy()
    hh["hhid"] = ["A", "B"]
    pp = pp.iloc[:2].copy()
    pp["hhid"] = ["A", "B"]
    assert profile_frames(hh, pp)["counts"]["plot_distinct_complete_keys"] == 2
    pp.loc[0, "s02_plotRoster__id"] = None
    pp.loc[1, "hhid"] = " "
    assert profile_frames(hh, pp)["counts"]["plot_missing_key_rows"] == 2


def test_missing_schema_fails():
    hh, pp = frames()
    with pytest.raises(ValueError, match="Missing required"):
        profile_frames(hh, pp.drop(columns="s02_q07"))


@pytest.mark.parametrize("value", [None, float("nan"), StataMissingValue(101),
                                  StataMissingValue(102)])
def test_tagged_and_ordinary_missing(value):
    assert response(value) == "missing"
    assert identifier(value) is None


@pytest.mark.parametrize("value", [True, "1"])
def test_wrong_response_types_rejected(value):
    with pytest.raises(TypeError, match="numeric"):
        response(value)


def test_output_outside_private_area_fails_before_read(tmp_path):
    with pytest.raises(ValueError, match="reports/private"):
        run(tmp_path / "not-read.zip", tmp_path / "public.json")


def test_archive_hash_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    archive = tmp_path / "bad.zip"
    archive.write_bytes(b"not the acquired archive")
    with pytest.raises(ValueError, match="hash"):
        run(archive, tmp_path / "reports/private/check.json")


def test_identifiers_preserve_types_and_large_integer_precision():
    assert identifier(1) == identifier(1.0)
    assert identifier("1") != identifier(1)
    assert identifier(2**53) != identifier(2**53 + 1)


def test_stata_reader_selects_columns_without_exporting_records():
    data = pd.DataFrame({"hhid": [1.0, 2.0], "final_weight": [2.0, 3.0],
                         "excluded_text": ["synthetic only", "not exported"]})
    stata, compressed = io.BytesIO(), io.BytesIO()
    # Pandas writes 114/117/118/119; actual format-115 reading is exercised locally on NASS.
    data.to_stata(stata, write_index=False, version=114)
    with zipfile.ZipFile(compressed, "w") as archive:
        archive.writestr("1_households.dta", stata.getvalue())
    compressed.seek(0)
    with zipfile.ZipFile(compressed) as archive:
        selected, metadata = read_selected(archive, "1_households.dta", HOUSEHOLD_COLUMNS)
    assert list(selected.columns) == list(HOUSEHOLD_COLUMNS)
    assert metadata["variables_in_file"] == 3
    assert "excluded_text" not in metadata["selected_columns"]
