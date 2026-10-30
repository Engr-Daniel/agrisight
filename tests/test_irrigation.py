"""IR1 manual accounting, skip logic, reviewed adapter and stakeholder controls."""

import copy
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest
from test_stakeholder_product import app, text

from agrisight import irrigation as model
from agrisight import irrigation_reporting as adapter


def frames():
    hh = pd.DataFrame({"hhid": [1, 2, 3]})
    pp = pd.DataFrame({"hhid": [1, 1, 2, 2, 3, 3], "s02_plotRoster__id": [1, 2, 1, 2, 1, 2],
        "s02_q15": [1, 2, 3, 1, 2, 3], "s02_q07": [1, 1, 1, 2, None, 9],
        "s02_q08": [1, None, 42, None, None, None], "s02_q09": [1, 99, None, None, None, None]})
    return hh, pp


def data():
    return {"version": "1.0", **model.calculate(*frames())}


def test_manual_counts_denominators_and_exclusions():
    result = data()
    assert result["infrastructure"] == {"input_rows": 6, "yes": 3, "no": 1, "missing": 1,
                                        "invalid": 1, "denominator": 4, "share": 0.75}
    assert {k: result["method"][k] for k in ("eligible", "denominator", "missing", "invalid")} == {
        "eligible": 3, "denominator": 1, "missing": 1, "invalid": 1}
    assert result["method"]["categories"][0]["share"] == 1
    assert result["source"]["denominator"] == 2
    assert [r["count"] for r in result["source"]["categories"]] == [1, 0, 0, 0, 0, 0, 1]
    assert result["source"]["populated_outside_yes"] == 0
    assert adapter.project(result, 6)["infrastructure"]["share"] == 0.75


def test_empty_no_yes_and_undefined_not_zero():
    hh, pp = frames()
    result = model.calculate(hh.iloc[:0], pp.iloc[:0])
    assert result["infrastructure"]["share"] is None
    assert all(r["share"] is None for r in result["method"]["categories"])
    pp["s02_q07"], pp["s02_q08"], pp["s02_q09"] = 2, None, None
    result = model.calculate(hh, pp)
    assert result["infrastructure"]["share"] == 0
    assert result["source"]["eligible"] == 0 and result["source"]["outside_yes"] == 6
    assert result["source"]["populated_outside_yes"] == 0


@pytest.mark.parametrize("which,column,value", [
    (0, "hhid", None), (0, "hhid", 2), (1, "hhid", 99), (1, "s02_plotRoster__id", None),
    (1, "s02_q15", 9), (1, "s02_q15", True), (1, "s02_q07", True),
    (1, "s02_q08", True), (1, "s02_q09", "1")])
def test_invalid_records_abort(which, column, value):
    tables = [f.astype(object) for f in frames()]
    tables[which].loc[0, column] = value
    with pytest.raises((ValueError, TypeError)):
        model.calculate(*tables)


def test_duplicate_plot_missing_schema_and_sql_disagreement(monkeypatch):
    hh, pp = frames()
    with pytest.raises(ValueError):
        model.calculate(hh, pd.concat([pp, pp.iloc[:1]]))
    with pytest.raises(ValueError):
        model.calculate(hh, pp.drop(columns="s02_q08"))
    sql = model.sql_text()
    monkeypatch.setattr(model, "sql_text", lambda: sql.replace("COUNT(*)", "COUNT(*)+1"))
    with pytest.raises(ValueError, match="mismatch"):
        model.calculate(hh, pp)


def test_populated_skips_are_visible_and_hide_product():
    hh, pp = frames()
    pp.loc[3, "s02_q08"] = 2
    result = {"version": "1.0", **model.calculate(hh, pp)}
    assert result["method"]["populated_outside_yes"] == 1
    with pytest.raises(ValueError):
        adapter.project(result, 6)


@pytest.mark.parametrize("mutation", [
    lambda d: d["infrastructure"].update(yes=True),
    lambda d: d["infrastructure"].update(share=0.9),
    lambda d: d["method"].update(eligible=4),
    lambda d: d["source"].update(denominator=3),
    lambda d: d["method"]["categories"][0].update(count=9),
    lambda d: d["source"]["categories"][0].update(share=1),
    lambda d: d["method"]["categories"][0].update(code=True),
    lambda d: d["method"].update(outside_yes=0),
])
def test_adapter_rejects_inconsistent_counts_and_rates(mutation):
    result = data()
    mutation(result)
    with pytest.raises(ValueError):
        adapter.project(result, 6)


def test_hash_missing_file_total_and_allowlist(tmp_path):
    result = data()
    result["private"] = "do not expose"
    raw = json.dumps(result).encode()
    path = tmp_path / "reports/private/irrigation_ir1.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    manifest = {"purpose": "TEST FIXTURE", "artifact": {
        "sha256": hashlib.sha256(raw).hexdigest(), "expected": {"version": "1.0"}}}
    assert "private" not in adapter.build_bundle(tmp_path, 6, manifest)
    assert adapter.build_bundle(tmp_path, 5, manifest)["status"] == "unavailable"
    path.write_bytes(raw + b" ")
    assert adapter.build_bundle(tmp_path, 6, manifest)["status"] == "unavailable"
    path.unlink()
    assert adapter.build_bundle(tmp_path, 6, manifest)["status"] == "unavailable"


def test_cli_output_boundary_and_archive_identity(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    archive = tmp_path / "fake.zip"
    archive.write_bytes(b"not the archive")
    with pytest.raises(ValueError, match="Output"):
        model.run(archive, tmp_path / "outside.json")
    with pytest.raises(ValueError, match="archive"):
        model.run(archive, Path("reports/private/result.json"))


def ui_bundle():
    hh, pp = frames()
    pp = pp.iloc[:3].copy()
    pp["s02_q07"], pp["s02_q08"], pp["s02_q09"] = [1, 1, 2], [1, 8, None], [3, 1, None]
    return {"status": "available", "origin": "TEST FIXTURE",
            **adapter.project({"version": "1.0", **model.calculate(hh, pp)}, 3)}


def test_all_question_unit_transitions_and_optional_failure(monkeypatch):
    bundle = ui_bundle()
    monkeypatch.setattr(adapter, "build_bundle", lambda root, total: copy.deepcopy(bundle))
    at = app(monkeypatch)
    at.button(key="nav_1").click().run()
    assert not at.exception and at.selectbox(key="water_question").value == "Infrastructure presence"
    assert "66.67%" in text(at) and "not prove a plot is rain-fed" in text(at)
    for question in ("Infrastructure presence", "Irrigation methods", "Water sources"):
        at.selectbox(key="water_question").set_value(question).run()
        assert not at.exception
        metrics = {m.label: m.value for m in at.metric}
        assert metrics["Valid response denominator"] == ("3" if question == "Infrastructure presence" else "2")
        if question != "Infrastructure presence":
            assert "expected skips" in text(at)
        for unit in ("Plot counts", "Percentages"):
            at.radio(key="water_unit").set_value(unit).run()
            assert not at.exception
    bundle.clear()
    bundle["status"] = "unavailable"
    at.run()
    assert not at.exception and "irrigation evidence is unavailable" in text(at)
    assert at.selectbox(key="activity").value == "all"


def test_ui_zero_eligible_and_missing_applicable(monkeypatch):
    hh, pp = frames()
    pp = pp.iloc[:3].copy()
    pp["s02_q07"], pp["s02_q08"], pp["s02_q09"] = 1, None, None
    bundle = {"status": "available", "origin": "TEST FIXTURE",
              **adapter.project({"version": "1.0", **model.calculate(hh, pp)}, 3)}
    monkeypatch.setattr(adapter, "build_bundle", lambda root, total: bundle)
    at = app(monkeypatch)
    at.button(key="nav_1").click().run()
    at.selectbox(key="water_question").set_value("Irrigation methods").run()
    assert not at.exception and "undefined" in text(at)
    assert "3 missing" in text(at)
