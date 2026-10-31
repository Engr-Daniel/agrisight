"""SS1 binary semantics, overlap, periods, disclosure and optional product controls."""

import copy
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest
from test_stakeholder_product import app, subject, text

from agrisight import seed_reporting as adapter
from agrisight import seed_sources as model


def frames():
    hh = pd.DataFrame({"hhid": [1, 2, 3], "s00_q15a": [1, 1, 2]})
    seeds = pd.DataFrame({"hhid": [1, 1, 2, 2, 3], "s04_cropRoster__id": [1080, 1010, 1110, 1100, 3140],
        "s04_cropsType": [1, 1, 1, 1, 2], "s04_reference": [model.PERIODS[1]]*4+[model.PERIODS[2]]})
    vectors = [(1, 0, 0, 0, 0), (1, 0, 1, 0, 0), (0, 0, 0, 0, 0), (1, None, 2, 0, 0), (1, 0, 0, 0, 0)]
    for i, field in enumerate(model.FIELDS):
        seeds[field] = [v[i] for v in vectors]
    return hh, seeds


def data():
    return {"version": "1.0", **model.calculate(*frames())}


def test_manual_zero_one_overlap_and_complete_vector_denominators():
    result = data()
    assert result["counts"] == {"household_records": 3, "seed_rows": 5, "eligible_records": 4,
        "excluded_permanent_records": 1, "represented_households": 2,
        "crop_yes_without_temporary_seed_record": 0, "temporary_seed_households_without_crop_yes": 0}
    assert result["sources"][0]["share"] == 0.75
    assert result["sources"][2]["invalid"] == 1 and result["sources"][2]["denominator"] == 3
    assert result["sources"][1]["missing"] == 1
    assert result["combinations"]["denominator"] == 3 and result["combinations"]["excluded"] == 1
    assert [r["mask"] for r in result["combinations"]["rows"]] == [0, 1, 5]
    assert adapter.project(result, 3, 2)["combinations"]["suppressed"]
    assert result["variety_status"] == "interpretation_not_verified"


def test_empty_and_missing_responses_are_not_zero():
    hh, seeds = frames()
    empty = model.calculate(hh.iloc[:0], seeds.iloc[:0])
    assert all(s["share"] is None for s in empty["sources"])
    seeds[model.FIELDS[0]] = None
    result = model.calculate(hh, seeds)
    assert result["sources"][0]["share"] is None
    assert result["combinations"]["denominator"] == 0


@pytest.mark.parametrize("which,column,value", [
    (0, "hhid", None), (0, "hhid", 2), (1, "hhid", 99), (1, "s04_cropRoster__id", None),
    (1, "s04_cropRoster__id", True), (1, "s04_cropRoster__id", 999), (1, "s04_cropRoster__id", float("inf")),
    (1, "s04_cropsType", 3), (1, "s04_cropsType", True), (1, "s04_reference", model.PERIODS[2]),
    (1, "s04_q03a__1", True), (1, "s04_q03a__2", "0")])
def test_invalid_keys_codes_types_periods_abort(which, column, value):
    tables = [t.astype(object) for t in frames()]
    tables[which].loc[0, column] = value
    with pytest.raises((ValueError, TypeError)):
        model.calculate(*tables)


def test_duplicate_key_schema_and_independent_sql(monkeypatch):
    hh, seeds = frames()
    with pytest.raises(ValueError):
        model.calculate(hh, pd.concat([seeds, seeds.iloc[:1]]))
    with pytest.raises(ValueError):
        model.calculate(hh, seeds.drop(columns=model.FIELDS[0]))
    sql = model.sql_text()
    monkeypatch.setattr(model, "sql_text", lambda: sql.replace("COUNT(*)", "COUNT(*)+1"))
    with pytest.raises(ValueError, match="disagreement"):
        model.calculate(hh, seeds)


@pytest.mark.parametrize("mutation", [
    lambda d: d["counts"].update(eligible_records=True),
    lambda d: d["sources"][0].update(no=99),
    lambda d: d["sources"][0].update(share=0.5),
    lambda d: d["sources"][0].update(id=True),
    lambda d: d["combinations"].update(excluded=0),
    lambda d: d["combinations"]["rows"][0].update(mask=32),
    lambda d: d["combinations"]["rows"][0].update(mask=8),
    lambda d: d["combinations"]["rows"][0].update(records=99),
    lambda d: d.update(variety_status="certified"),
])
def test_adapter_rejects_inconsistent_counts_and_claims(mutation):
    result = data()
    mutation(result)
    with pytest.raises(ValueError):
        adapter.project(result, 3, 2)


def test_public_combination_pooling_and_complementary_protection():
    result = data()
    # Replicate aggregate truth40 times: three named groups, no small residual.
    for key in result["counts"]:
        if key != "household_records":
            result["counts"][key] *= 40
    result["counts"]["household_records"] = 120
    for source in result["sources"]:
        for key in ("yes", "no", "missing", "invalid", "denominator"):
            source[key] *= 40
    for key in ("denominator", "excluded"):
        result["combinations"][key] *= 40
    for row in result["combinations"]["rows"]:
        row["records"] *= 40
    projected = adapter.project(result, 120, 80)
    assert not projected["combinations"]["suppressed"]
    assert len(projected["combinations"]["rows"]) == 3
    # Small cells cannot pass as exact mask/count rows.
    small = adapter.project(data(), 3, 2)
    assert small["combinations"]["rows"] == []


def test_loader_hash_crosscheck_and_private_fields(tmp_path):
    result = data()
    result["private"] = "do not expose"
    raw = json.dumps(result).encode()
    path = tmp_path / "reports/private/seed_sources_ss1.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    manifest = {"purpose": "TEST FIXTURE", "artifact": {"sha256": hashlib.sha256(raw).hexdigest(), "expected": {"version": "1.0"}}}
    assert "private" not in adapter.build_bundle(tmp_path, 3, 2, manifest)
    assert adapter.build_bundle(tmp_path, 4, 2, manifest)["status"] == "unavailable"
    path.write_bytes(raw+b" ")
    assert adapter.build_bundle(tmp_path, 3, 2, manifest)["status"] == "unavailable"


@pytest.mark.parametrize("rare_count,suppressed", [(3, True), (30, False)])
def test_rare_residual_never_reveals_exact_mask_count(rare_count, suppressed):
    masks = [mask for mask in range(1, 7) for _ in range(30)] + [8]*rare_count
    hh = pd.DataFrame({"hhid": range(len(masks)), "s00_q15a": 1})
    seeds = pd.DataFrame({"hhid": range(len(masks)), "s04_cropRoster__id": 1080,
                         "s04_cropsType": 1, "s04_reference": model.PERIODS[1]})
    for i, field in enumerate(model.FIELDS):
        seeds[field] = [int(bool(mask & (1 << i))) for mask in masks]
    result = {"version": "1.0", **model.calculate(hh, seeds)}
    projected = adapter.project(result, len(masks), len(masks))["combinations"]
    assert projected["suppressed"] == suppressed
    if suppressed:
        assert not projected["rows"]
    else:
        assert sum(r["records"] for r in projected["rows"]) == len(masks)


def test_cli_path_and_archive_guard(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    p = tmp_path / "fake.zip"
    p.write_bytes(b"fake")
    with pytest.raises(ValueError, match="Output"):
        model.run(p, tmp_path / "outside.json")
    with pytest.raises(ValueError, match="archive"):
        model.run(p, Path("reports/private/test.json"))


def test_ui_modes_units_undefined_variety_gate_and_failure(monkeypatch):
    bundle = {"status": "available", "origin": "TEST FIXTURE", **adapter.project(data(), 3, 2)}
    monkeypatch.setattr(adapter, "build_bundle", lambda *args: copy.deepcopy(bundle))
    at = subject(app(monkeypatch), "Seed sources")
    assert not at.exception and "Variety and certification percentages are not shown" in text(at)
    assert "Sources can overlap" in text(at)
    for view in ("Source combinations", "Sources"):
        at.selectbox(key="seed_view").set_value(view).run()
        for unit in ("Record counts", "Percentages"):
            at.radio(key="seed_unit").set_value(unit).run()
            assert not at.exception
    assert "denominators differ" in text(at)
    bundle.clear()
    bundle["status"] = "unavailable"
    at.run()
    assert not at.exception and "seed-source evidence is unavailable" in text(at)
    at.pills(key="subject").set_value("Activities").run()
    assert at.selectbox(key="activity").value == "all"
