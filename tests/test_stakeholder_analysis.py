"""Manual counts and negative/edge fixtures for the stakeholder analysis contract."""

from pathlib import Path

import pandas as pd
import pytest

from agrisight import stakeholder_analysis as model


def frames():
    hh = pd.DataFrame({"hhid": [1, 2, 3, 4, 5], "s00_q15a": [1, 2, 1, None, 9],
                       "s00_q16": [1, 1, 2, 1, 2], "s00_q17": [2, 2, 1, 2, 2],
                       "s00_q18": [1, 2, 2, 2, 2]})
    pp = pd.DataFrame({"hhid": [1, 2, 3], "s02_plotRoster__id": [1, 1, 1],
                       "s02_q15": [1, 2, 3], "s02_q16a": [10, None, 0]})
    return hh, pp


def test_manual_activity_joint_and_plot_truth():
    result = model.calculate(*frames())
    crop = result["activities"][0]
    assert {k: crop[k] for k in ("yes", "no", "missing", "invalid", "denominator")} == {
        "yes": 2, "no": 1, "missing": 1, "invalid": 1, "denominator": 3}
    assert crop["share"] == 2/3
    assert [r["count"] for r in result["overlap"]["cells"]] == [1, 1, 1, 0]
    assert result["overlap"]["denominator"] == 3 and result["overlap"]["excluded"] == 2
    assert [r["count"] for r in result["plot_types"]] == [1, 1, 1]
    assert result["plots"] == {"total": 3, "missing_area": 1, "recorded_area": 2}


def test_empty_frames_and_no_valid_responses():
    hh, pp = frames()
    empty = model.calculate(hh.iloc[:0], pp.iloc[:0])
    assert all(r["share"] is None for r in empty["activities"])
    hh["s00_q15a"] = None
    result = model.calculate(hh, pp)
    assert result["activities"][0]["share"] is None
    assert result["overlap"]["denominator"] == 0 and result["overlap"]["excluded"] == 5


@pytest.mark.parametrize("which,column,value", [
    (0, "hhid", None), (0, "hhid", 2), (0, "s00_q16", True),
    (1, "hhid", 99), (1, "s02_q15", 4), (1, "s02_q15", True),
    (1, "s02_q16a", -1), (1, "s02_q16a", float("inf")), (1, "s02_q16a", "bad")])
def test_invalid_keys_codes_and_areas_abort(which, column, value):
    data = list(frames())
    data[which] = data[which].astype(object)
    data[which].loc[0, column] = value
    with pytest.raises((ValueError, TypeError)):
        model.calculate(*data)


def test_duplicate_plot_and_missing_schema_abort():
    hh, pp = frames()
    with pytest.raises(ValueError):
        model.calculate(hh, pd.concat([pp, pp.iloc[:1]]))
    with pytest.raises(ValueError):
        model.calculate(hh.drop(columns="s00_q17"), pp)


def test_sql_disagreement_is_not_silently_accepted(monkeypatch):
    original = model.sql_text()
    monkeypatch.setattr(model, "sql_text", lambda: original.replace("SUM(response='yes')", "0"))
    with pytest.raises(ValueError, match="reconciliation"):
        model.calculate(*frames())


def test_cli_input_hash_and_output_scope(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    archive = tmp_path/"input.zip"
    archive.write_bytes(b"wrong archive")
    with pytest.raises(ValueError, match="inside reports/private"):
        model.run(archive, Path("outside.json"))
    with pytest.raises(ValueError, match="Archive hash"):
        model.run(archive, Path("reports/private/result.json"))
