"""Independent coverage counts, boundary integrity, disclosure and failure fixtures."""

import copy
import hashlib
import json
from importlib.resources import files

import pandas as pd
import pytest
from test_stakeholder_product import app, text

from agrisight import coverage_reporting as adapter
from agrisight import geographic_coverage as model


def fixture():
    data = {"version": "1.0", "total": 1850, "states": [
        {"code": i, "name": name, "households": 50} for i, name in enumerate(model.STATE_NAMES, 1)]}
    geometry = {"type": "Polygon", "coordinates": [[[3, 5], [3, 6], [4, 6], [4, 5], [3, 5]]]}
    boundaries = {"features": [{"type": "Feature", "properties": {"code": s["code"], "name": s["name"]},
                                "geometry": geometry} for s in data["states"]]}
    return data, boundaries


def test_manually_counted_coverage_and_empty():
    result = model.calculate(pd.DataFrame({"hhid": ["a", "b", "c"], "state_id": [1, 1, 14]}))
    assert result["total"] == 3
    assert result["states"][0]["households"] == 2
    assert result["states"][13] == {"code": 14, "name": "FCT", "households": 1}
    assert sum(s["households"] for s in result["states"]) == 3
    assert model.calculate(pd.DataFrame(columns=["hhid", "state_id"]))["total"] == 0


@pytest.mark.parametrize("households,states", [([1, 1], [1, 2]), ([None], [1]),
    ([1], [None]), ([1], [0]), ([1], [38]), ([1], [True]), ([1], ["1"])])
def test_invalid_source_keys_codes_abort(households, states):
    with pytest.raises((ValueError, TypeError)):
        model.calculate(pd.DataFrame({"hhid": households, "state_id": states}))


@pytest.mark.parametrize("which", ("total", "code", "name", "count", "boundary", "length"))
def test_projection_rejects_inconsistent_geography(which):
    data, boundaries = fixture()
    if which == "total":
        data["total"] += 1
    elif which == "code":
        data["states"][0]["code"] = 2
    elif which == "name":
        data["states"][0]["name"] = "UNKNOWN"
    elif which == "count":
        data["states"][0]["households"] = True
    elif which == "boundary":
        boundaries["features"][0]["properties"]["name"] = "UNKNOWN"
    else:
        boundaries["features"].pop()
    with pytest.raises(ValueError):
        adapter.project(data, boundaries, 1850)


def test_suppression_withholds_complementary_counts_everywhere():
    data, boundaries = fixture()
    data["states"][0]["households"] = 29
    data["total"] -= 21
    result = adapter.project(data, boundaries, data["total"])
    assert result["suppressed"]
    assert all(s["households"] is None for s in result["states"])
    assert all(f["properties"]["households"] is None for f in result["features"])
    assert "total" not in result
    data["states"][0]["households"] = 30
    data["total"] += 1
    assert not adapter.project(data, boundaries, data["total"])["suppressed"]


def test_packaged_geometry_complete_and_no_household_locations():
    boundaries = json.loads(files("agrisight").joinpath("reporting/nigeria_adm1_v1.json").read_bytes())
    assert len(boundaries["features"]) == 37
    assert [f["properties"]["name"] for f in boundaries["features"]] == list(model.STATE_NAMES)
    assert boundaries["provenance"]["licence"] == "CC BY 4.0"
    assert all(set(f["properties"]) == {"code", "name"} for f in boundaries["features"])


def test_optional_loader_hash_failure_and_no_data(tmp_path):
    assert adapter.build_bundle(tmp_path, 1850) == {"status": "unavailable"}
    data, _ = fixture()
    raw = json.dumps(data).encode()
    path = tmp_path / "reports/private/geographic_gc1.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(raw)
    manifest = {"artifact": {"sha256": hashlib.sha256(raw).hexdigest(), "expected": {}},
                "boundary_sha256": "0"*64}
    assert adapter.build_bundle(tmp_path, 1850, manifest) == {"status": "unavailable"}


def test_available_suppressed_and_unavailable_map_pages(monkeypatch):
    data, boundaries = fixture()
    bundle = adapter.project(data, boundaries, 1850)
    monkeypatch.setattr(adapter, "build_bundle", lambda root, total: copy.deepcopy(bundle))
    at = app(monkeypatch)
    at.button(key="nav_1").click().run()
    assert not at.exception and "sample" in text(at)
    assert any(e.label == "Read the state coverage table" for e in at.expander)
    bundle["suppressed"] = True
    for f in bundle["features"]:
        f["properties"]["households"] = None
    at.run()
    assert not at.exception and "counts are withheld" in text(at)
    assert not any(e.label == "Read the state coverage table" for e in at.expander)
    bundle.clear()
    bundle["status"] = "unavailable"
    at.run()
    assert not at.exception and "coverage map is unavailable" in text(at)
    assert at.selectbox(key="activity").value == "all"
