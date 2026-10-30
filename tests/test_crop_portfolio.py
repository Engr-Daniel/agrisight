"""CP1 distinct-household counting, scoped metadata gaps and safe presentation."""

import copy
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest
from test_stakeholder_analysis import frames as core_frames
from test_stakeholder_product import app, text

from agrisight import crop_portfolio as model
from agrisight import crop_reporting as adapter


def frames():
    hh = pd.DataFrame({"hhid": [1, 2, 3, 4], "s00_q15a": [1, 1, 2, 1]})
    pp = pd.DataFrame({"hhid": [1, 1, 2, 3, 4], "s02_plotRoster__id": [1, 2, 1, 1, 1]})
    cc = pd.DataFrame({"hhid": [1, 1, 1, 2, 3, 4], "s02_plotRoster__id": [1, 2, 2, 1, 1, 1],
                       "s03_cropRoster__id": [1080, 1080, 1010, 1110, 1020, 3140], "s03_cropsType": [1, 1, 1, 1, 1, 2]})
    return hh, pp, cc


def data():
    return {"version": "1.0", **model.calculate(*frames())}


def test_manual_truth_deduplicates_across_plots_not_raw_records():
    result = data()
    assert result["counts"] == {"household_records": 4, "plot_records": 5, "crop_rows": 6,
        "temporary_rows": 5, "excluded_permanent_rows": 1, "unlabelled_permanent_rows": 1,
        "represented_households": 3, "household_crop_pairs": 4,
        "crop_yes_households_without_temporary_record": 1, "temporary_households_without_crop_yes": 1}
    assert result["mean_categories"] == 4/3
    assert {r["code"]: r["households"] for r in result["portfolio"]} == {1010: 1, 1020: 1, 1080: 1, 1110: 1}
    assert [r["households"] for r in result["diversity"]] == [2, 1, 0, 0, 0]
    assert adapter.project(result, 4, 5, 3)["counts"]["represented_households"] == 3


def test_empty_and_permanent_only_are_not_zero_diversity_households():
    hh, pp, cc = frames()
    result = model.calculate(hh.iloc[:0], pp.iloc[:0], cc.iloc[:0])
    assert result["mean_categories"] is None and not result["portfolio"]
    assert all(r["share"] is None for r in result["diversity"])
    cc["s03_cropsType"] = 2
    result = model.calculate(hh, pp, cc)
    assert result["counts"]["represented_households"] == 0
    assert result["counts"]["crop_yes_households_without_temporary_record"] == 3


@pytest.mark.parametrize("which,column,value", [
    (0, "hhid", None), (0, "hhid", 2), (1, "hhid", 99), (2, "s02_plotRoster__id", 99),
    (2, "s03_cropRoster__id", None), (2, "s03_cropRoster__id", True), (2, "s03_cropRoster__id", 3140),
    (2, "s03_cropRoster__id", 1.5), (2, "s03_cropsType", None), (2, "s03_cropsType", True),
    (2, "s03_cropsType", 3)])
def test_invalid_keys_codes_types_abort(which, column, value):
    tables = [f.astype(object) for f in frames()]
    tables[which].loc[0, column] = value
    with pytest.raises((ValueError, TypeError)):
        model.calculate(*tables)


def test_duplicate_raw_key_missing_schema_and_sql_disagreement(monkeypatch):
    hh, pp, cc = frames()
    with pytest.raises(ValueError):
        model.calculate(hh, pp, pd.concat([cc, cc.iloc[:1]]))
    with pytest.raises(ValueError):
        model.calculate(hh, pp, cc.drop(columns="s03_cropsType"))
    sql = model.sql_text()
    monkeypatch.setattr(model, "sql_text", lambda: sql.replace("COUNT(*)", "COUNT(*)+1"))
    with pytest.raises(ValueError, match="disagreement"):
        model.calculate(hh, pp, cc)


@pytest.mark.parametrize("mutation", [
    lambda d: d["counts"].update(represented_households=True),
    lambda d: d["counts"].update(temporary_rows=99),
    lambda d: d["counts"].update(temporary_households_without_crop_yes=0),
    lambda d: d["portfolio"][0].update(households=99),
    lambda d: d["portfolio"][0].update(label="invented"),
    lambda d: d["portfolio"][0].update(share=0.9),
    lambda d: d["diversity"][0].update(households=9),
    lambda d: d["diversity"][0].update(categories="0"),
    lambda d: d.update(mean_categories=99),
])
def test_adapter_rejects_inconsistent_aggregates(mutation):
    result = data()
    mutation(result)
    with pytest.raises(ValueError):
        adapter.project(result, 4, 5, 3)


def test_five_plus_bin_limits_and_empty_projection():
    hh = pd.DataFrame({"hhid": [1], "s00_q15a": [1]})
    pp = pd.DataFrame({"hhid": [1], "s02_plotRoster__id": [1]})
    codes = list(model.crop_labels())[:6]
    cc = pd.DataFrame({"hhid": [1]*6, "s02_plotRoster__id": [1]*6, "s03_cropRoster__id": codes, "s03_cropsType": [1]*6})
    result = {"version": "1.0", **model.calculate(hh, pp, cc)}
    assert adapter.project(result, 1, 1, 1)["diversity"][-1]["households"] == 1
    assert result["mean_categories"] == 6
    result = {"version": "1.0", **model.calculate(hh.iloc[:0], pp.iloc[:0], cc.iloc[:0])}
    assert adapter.project(result, 0, 0, 0)["mean_categories"] is None


def test_loader_hash_failure_crosscheck_and_private_fields(tmp_path):
    result = data()
    result["private"] = "never expose"
    raw = json.dumps(result).encode()
    path = tmp_path / "reports/private/crop_portfolio_cp1.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    manifest = {"purpose": "TEST FIXTURE", "artifact": {"sha256": hashlib.sha256(raw).hexdigest(), "expected": {"version": "1.0"}}}
    assert "private" not in adapter.build_bundle(tmp_path, 4, 5, 3, manifest)
    assert adapter.build_bundle(tmp_path, 5, 5, 3, manifest)["status"] == "unavailable"
    path.write_bytes(raw + b" ")
    assert adapter.build_bundle(tmp_path, 4, 5, 3, manifest)["status"] == "unavailable"


def test_output_guard_and_archive_hash(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "fake.zip"
    path.write_bytes(b"fake")
    with pytest.raises(ValueError, match="Output"):
        model.run(path, tmp_path / "outside.json")
    with pytest.raises(ValueError, match="archive"):
        model.run(path, Path("reports/private/test.json"))


def test_ui_modes_units_coverage_warning_and_optional_failure(monkeypatch):
    hh, pp = core_frames()
    cc = pd.DataFrame({"hhid": [1, 1, 2, 3], "s02_plotRoster__id": [1, 1, 1, 1],
                       "s03_cropRoster__id": [1080, 1010, 1110, 9999], "s03_cropsType": [1, 1, 1, 2]})
    bundle = {"status": "available", "origin": "TEST FIXTURE",
              **adapter.project({"version": "1.0", **model.calculate(hh, pp, cc)}, 5, 3, 2)}
    monkeypatch.setattr(adapter, "build_bundle", lambda *args: copy.deepcopy(bundle))
    at = app(monkeypatch)
    at.button(key="nav_1").click().run()
    assert not at.exception and "coverage differs" in text(at)
    assert at.selectbox(key="crop_view").value == "Crop portfolio"
    for mode in ("Recorded diversity", "Crop portfolio"):
        at.selectbox(key="crop_view").set_value(mode).run()
        for unit in ("Household counts", "Percentages"):
            at.radio(key="crop_unit").set_value(unit).run()
            assert not at.exception
    bundle.clear()
    bundle["status"] = "unavailable"
    at.run()
    assert not at.exception and "crop portfolio evidence is unavailable" in text(at)
    assert at.selectbox(key="activity").value == "all"
