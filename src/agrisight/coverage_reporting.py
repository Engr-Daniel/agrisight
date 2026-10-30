"""Optional, fail-closed geographic coverage projection; no raw coordinates of respondents."""

import hashlib
from importlib.resources import files
from pathlib import Path

from agrisight.reporting_adapter import count, load_artifact, require, strict_json


def project(data: dict, boundaries: dict, total: int) -> dict:
    require(data["version"] == "1.0" and count(data["total"]) == total)
    states = data["states"]
    features = boundaries["features"]
    require(len(states) == len(features) == 37)
    require([s["code"] for s in states] == list(range(1, 38)))
    counts = [count(s["households"]) for s in states]
    require(sum(counts) == total)
    require(len({s["name"] for s in states}) == 37)
    suppressed = any(n < 30 for n in counts)
    safe_features, safe_states = [], []
    for state, feature in zip(states, features, strict=True):
        require(type(state["code"]) is int)
        require(feature["type"] == "Feature" and feature["geometry"]["type"] in ("Polygon", "MultiPolygon"))
        require(feature["properties"] == {"code": state["code"], "name": state["name"]})
        # If a small cell exists, withhold every regional count to prevent complementary reconstruction.
        safe = {"name": state["name"], "households": None if suppressed else state["households"]}
        safe_states.append(safe)
        safe_features.append({"type": "Feature", "geometry": feature["geometry"], "properties": safe})
    return {"status": "available", "suppressed": suppressed, "states": safe_states,
            "features": safe_features}


def build_bundle(root: Path, total: int, manifest: dict | None = None) -> dict:
    try:
        manifest = manifest or strict_json(files("agrisight").joinpath(
            "reporting/coverage_manifest_v1.json").read_bytes())
        data, _ = load_artifact(root, "geographic_gc1.json", manifest["artifact"])
        raw = files("agrisight").joinpath("reporting/nigeria_adm1_v1.json").read_bytes()
        require(hashlib.sha256(raw).hexdigest() == manifest["boundary_sha256"])
        require(data["provenance"]["boundary_sha256"] == manifest["boundary_sha256"])
        return project(data, strict_json(raw), total)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return {"status": "unavailable"}
