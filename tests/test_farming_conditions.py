"""Manually counted FC1 branches, denominators, nulls, tampering and UI controls."""

import copy
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from agrisight import conditions_reporting as adapter
from agrisight import farming_conditions as model


def frames():
    reference = model.metadata()
    hh = pd.DataFrame({"hhid": [1, 2, 3]})
    pp = pd.DataFrame({"hhid": [1, 1, 2, 3], "s02_plotRoster__id": [1, 2, 1, 1],
        "s02_q04": [1, 4, 2, 99], "s02_q05": [1, 6, None, 2], "s02_q06": [1, 5, 2, None]})
    rows = [(1, 1, 1080, 1), (1, 2, 1010, 1), (2, 1, 2260, 1), (3, 1, 2120, 1),
            (3, 1, 1070, 1), (2, 1, 3040, 2)]
    cc = pd.DataFrame([{**dict.fromkeys(reference[model.MODULES[1]]["labels"]),
        **dict(zip(("hhid", "s02_plotRoster__id", "s03_cropRoster__id", "s03_cropsType"), r, strict=True))} for r in rows], dtype=object)
    for prefix in ("s01a_q08__", "s01a_q17__", "s01h_q09__", "s01h_q22__"):
        for col in cc.columns:
            if col.startswith(prefix):
                cc[col] = 0
    cc.loc[0, ["s01a_q07", "s01a_q08__1"]] = [2, 1]
    cc.loc[1, ["s01a_q07", "s01a_q11", "s01a_q16", "s01a_q17__9"]] = [1, 2, 1, 1]
    cc.loc[2, ["s01h_q08", "s01h_q16", "s01h_q21"]] = [1, 1, 1]
    cc.loc[4, ["s01a_q07", "s01h_q08"]] = [1, 1]
    harvest = pd.DataFrame({"hhid": [1, 2, 3], "s01b_harvestedCrops__id": [1010, 2260, 2120],
        "s01b_q02": [1, 2, None], "s01b_q20": [1, 1, 2], "s01b_q11": [2, 1, 99]})
    inputs = pd.DataFrame({"hhid": [1, 2, 3, 3], "s03c_inputType__id": [1, 1, 1, 7], "s03c_q01": [10, 0, None, -3]})
    return hh, pp, cc, harvest, inputs


def data():
    return {"version": "1.0", **model.calculate(*frames())}


def test_manual_land_eligibility_and_exceptions():
    result = data()
    assert result["counts"] == {"households": 3, "plots": 4, "crops": 6, "harvest": 3, "inputs": 4}
    land = result["land"]
    assert land["tenure"]["valid"] == 3 and land["tenure"]["invalid"] == 1
    assert land["tenure"]["rows"][3]["share"] == 1/3
    assert land["travel"]["eligible"] == 2 and land["travel"]["valid"] == 1
    assert land["travel"]["missing"] == 1
    assert land["on_dwelling"] == land["unknown_transport"] == 1
    assert land["outside_travel_answers"] == 2


def test_manual_harvest_branch_skips_reasons_and_unknowns():
    d = data()["difficulties"]
    assert (d["temporary_records"], d["excluded_permanent"], d["unassigned"], d["ambiguous"]) == (5, 1, 1, 1)
    a, v = d["branches"]
    assert a["harvest"]["eligible"] == 2 and a["harvest"]["rows"][1]["share"] == .5
    assert a["no_harvest_reasons"][0]["eligible"] == 1
    assert a["no_harvest_reasons"][0]["rows"][1]["share"] == 1
    assert a["shock_reasons"][8]["rows"][1]["count"] == 1
    assert a["shocks"]["eligible"] == 1
    assert v["shocks"]["eligible"] == 0 and v["shocks"]["rows"][0]["share"] is None
    assert v["outside_shock_answers"] == 1


def test_manual_destinations_overlap_quantity_status_and_projection():
    result = data()
    d = result["destinations"]
    assert d["sales"]["rows"][0]["share"] == .5
    assert d["storage"]["rows"][0]["share"] == 2/3
    assert d["losses"]["invalid"] == 1
    assert d["overlap"] == {"valid": 2, "excluded": 1, "cells": [
        {"sales": 1, "storage": 1, "count": 1}, {"sales": 1, "storage": 2, "count": 0},
        {"sales": 2, "storage": 1, "count": 1}, {"sales": 2, "storage": 2, "count": 0}]}
    assert [s["count"] for s in result["inputs"][0]["statuses"]] == [1, 1, 1, 0]
    assert result["inputs"][1]["statuses"][3]["count"] == 1
    result["raw_identity"] = "must not forward"
    projected = adapter.project(result, 3, 4)
    assert "raw_identity" not in projected
    assert not projected["destinations"]["crops"] and projected["destinations"]["omitted_crop_categories"] == 3


def test_empty_and_all_missing_quantities_and_tagged_missing():
    from pandas.io.stata import StataMissingValue
    tables = frames()
    result = model.calculate(*(f.iloc[:0] for f in tables))
    assert result["land"]["tenure"]["rows"][0]["share"] is None
    adapter.project({"version": "1.0", **result}, 0, 0)
    tables[-1]["s03c_q01"] = StataMissingValue(101)
    assert sum(r["statuses"][2]["count"] for r in model.calculate(*tables)["inputs"]) == 4


@pytest.mark.parametrize("which,column,value", [(0, "hhid", None), (1, "hhid", 99),
    (2, "s02_plotRoster__id", 99), (2, "s03_cropsType", 3), (2, "s03_cropRoster__id", 12345),
    (3, "s01b_harvestedCrops__id", 1110), (4, "s03c_inputType__id", 99),
    (1, "s02_q04", True), (4, "s03c_q01", "3")])
def test_invalid_parents_codes_and_response_types(which, column, value):
    tables = [f.astype(object) for f in frames()]
    tables[which].loc[0, column] = value
    with pytest.raises((ValueError, TypeError)):
        model.calculate(*tables)


def test_duplicates_missing_schema_and_independent_sql(monkeypatch):
    tables = list(frames())
    tables[3] = pd.concat([tables[3], tables[3].iloc[:1]])
    with pytest.raises(ValueError):
        model.calculate(*tables)
    tables = list(frames())
    tables[1] = tables[1].drop(columns="s02_q04")
    with pytest.raises(ValueError):
        model.calculate(*tables)
    sql = model.sql_text()
    monkeypatch.setattr(model, "sql_text", lambda: sql.replace("WHERE s01b_q02 IN", "WHERE 0 AND s01b_q02 IN"))
    with pytest.raises(ValueError, match="disagreement"):
        model.calculate(*frames())


@pytest.mark.parametrize("mutation", [
    lambda d: d["counts"].update(households=True),
    lambda d: d["land"]["travel"].update(eligible=99),
    lambda d: d["land"]["tenure"]["rows"][0].update(share=.99),
    lambda d: d["land"].update(on_dwelling=9),
    lambda d: d["difficulties"].update(unassigned=0),
    lambda d: d["difficulties"]["branches"][0]["shocks"].update(valid=99),
    lambda d: d["destinations"]["overlap"]["cells"][0].update(count=3),
    lambda d: d["destinations"]["crops"][0].update(code=True),
    lambda d: d["inputs"][0]["statuses"][0].update(count=99),
    lambda d: d["inputs"][0].update(label="Unknown label"),
])
def test_projection_rejects_inconsistent_aggregates(mutation):
    result = data()
    mutation(result)
    with pytest.raises(ValueError):
        adapter.project(result, 3, 4)


def test_pinned_optional_loader_missing_tampering_origin_and_totals(tmp_path):
    raw = json.dumps(data()).encode()
    path = tmp_path/"reports/private/farming_conditions_fc1.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    manifest = {"purpose": "TEST FIXTURE", "artifact": {"sha256": hashlib.sha256(raw).hexdigest(), "expected": {"version": "1.0"}}}
    assert adapter.build_bundle(tmp_path, 3, 4, "TEST FIXTURE", manifest)["status"] == "available"
    assert adapter.build_bundle(tmp_path, 3, 4, "REVIEWED LOCAL EVIDENCE", manifest)["status"] == "unavailable"
    assert adapter.build_bundle(tmp_path, 4, 4, "TEST FIXTURE", manifest)["status"] == "unavailable"
    path.write_bytes(raw+b" ")
    assert adapter.build_bundle(tmp_path, 3, 4, "TEST FIXTURE", manifest)["status"] == "unavailable"
    path.unlink()
    assert adapter.build_bundle(tmp_path, 3, 4, "TEST FIXTURE", manifest)["status"] == "unavailable"


def test_all_controls_and_chart_specs(monkeypatch):
    from agrisight import conditions_presentation as ui
    bundle = {"status": "available", "origin": "TEST FIXTURE", **adapter.project(data(), 3, 4)}
    monkeypatch.setattr(adapter, "build_bundle", lambda *args: copy.deepcopy(bundle))
    code = "from agrisight import conditions_presentation as ui, conditions_reporting as adapter\nui.show(adapter.build_bundle(None,0,0,''))"
    at = AppTest.from_string(code, default_timeout=25).run()
    assert not at.exception and len(at.tabs) == 4
    for selection in ("Travel time", "Transport", "Tenure"):
        at.selectbox(key="fc_land").set_value(selection).run()
        assert not at.exception
    for branch in ("vegetable", "nonvegetable"):
        at.selectbox(key="fc_branch").set_value(branch).run()
        for question in ("No-harvest reasons", "Unharvested area due to shocks", "Shock reasons", "Harvest reported"):
            at.selectbox(key="fc_difficulty").set_value(question).run()
            assert not at.exception
    for mode in ("Sales and storage overlap", "Broad loss reports", "Crop comparison"):
        at.selectbox(key="fc_destination").set_value(mode).run()
        assert not at.exception
    at.radio(key="fc_unit").set_value("Record counts").run()
    assert not at.exception
    assert ui.dots([{"label": "A", "count": 1, "share": .5, "valid": 2, "series": ""}]).to_dict()["mark"]["type"] == "point"
    monkeypatch.setattr(adapter, "build_bundle", lambda *args: {"status": "unavailable"})
    at.run()
    assert not at.exception and not at.tabs


def test_infinite_quantity_invalid_and_invalid_reason_not_no():
    tables = list(frames())
    tables[-1].loc[0, "s03c_q01"] = float("inf")
    tables[2].loc[0, "s01a_q08__1"] = 2
    result = model.calculate(*tables)
    assert result["inputs"][0]["statuses"][3]["count"] == 1
    reason = result["difficulties"]["branches"][0]["no_harvest_reasons"][0]
    assert reason["invalid"] == 1 and reason["rows"][1]["share"] is None


def test_fractional_transport_is_unknown_eligibility_not_travel():
    tables = list(frames())
    tables[1].loc[0, "s02_q05"] = 1.5
    result = model.calculate(*tables)
    assert result["land"]["travel"]["eligible"] == 1
    assert result["land"]["unknown_transport"] == 2


def test_packaged_resources_exist():
    from importlib.resources import files
    assert files("agrisight").joinpath("sql/farming_conditions.sql").is_file()
    assert Path(__file__).parents[1].joinpath("docs/FARMING_CONDITIONS_CONTRACT.md").is_file()
    for resource in ("reporting/conditions_labels_v1.json", "reporting/conditions_manifest_v1.json", "sql/farming_conditions.sql"):
        assert b"\r" not in files("agrisight").joinpath(resource).read_bytes()


def test_crop_detail_threshold_and_marginal_accounting():
    tables = []
    for frame in frames():
        tables.append(pd.concat([frame.assign(hhid=frame.hhid+i*10) for i in range(30)], ignore_index=True))
    result = {"version": "1.0", **model.calculate(*tables)}
    projected = adapter.project(result, 90, 120)
    assert len(projected["destinations"]["crops"]) == 2
    assert projected["destinations"]["omitted_crop_categories"] == 1
    result["destinations"]["overlap"]["cells"][0]["count"] += 1
    result["destinations"]["overlap"]["cells"][2]["count"] -= 1
    with pytest.raises(ValueError):
        adapter.project(result, 90, 120)


def test_shortened_input_labels_keep_all_twenty_one_types_distinct():
    from agrisight.conditions_presentation import input_cells
    labels = model.metadata()[model.MODULES[3]]["value_labels"]["s03c_inputType__id"]
    records = [{"code": int(code), "label": label, "records": 1,
                "statuses": [{"label": "Positive", "count": 1, "share": 1}]} for code, label in labels.items()]
    cells = input_cells(records)
    assert len({r["Input"] for r in cells}) == 21
    assert {r["Input"] for r in cells if r["Input"].startswith("Other ")} == {"Other organic fertilizer", "Other pesticides"}
    assert all("Input type" in r for r in cells)
