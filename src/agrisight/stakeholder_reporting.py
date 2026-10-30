"""Read-only product projection of reviewed survey aggregates."""

from importlib.resources import files
from pathlib import Path

from agrisight.reporting_adapter import (
    count,
    equal,
    load_artifact,
    manifest_resource,
    nass01,
    nass02,
    require,
    strict_json,
)


def project(data: dict) -> dict:
    """Validate accounting identities and expose only approved aggregate fields."""
    require(data["analysis_version"] == "1.0")
    activities = []
    ids = ("crops", "livestock", "fish_farming", "fish_capture")
    require(len(data["activities"]) == 4)
    for item, identifier in zip(data["activities"], ids, strict=True):
        require(item["id"] == identifier)
        values = {key: count(item[key]) for key in (
            "input_rows", "yes", "no", "missing", "invalid", "denominator")}
        require(values["yes"] + values["no"] == values["denominator"])
        require(values["denominator"] + values["missing"] + values["invalid"] ==
                values["input_rows"])
        share = values["yes"] / values["denominator"] if values["denominator"] else None
        equal(item["share"], share)
        require(type(item["label"]) is str and type(item["period"]) is str)
        activities.append(dict(id=identifier, label=item["label"], period=item["period"],
                               share=share, **values))
    total = activities[0]["input_rows"]
    require(all(a["input_rows"] == total for a in activities))
    overlap = data["overlap"]
    denominator, excluded = count(overlap["denominator"]), count(overlap["excluded"])
    require(denominator + excluded == total and len(overlap["cells"]) == 4)
    cells = []
    for cell, pair in zip(overlap["cells"],
                          (("yes", "yes"), ("yes", "no"), ("no", "yes"), ("no", "no")),
                          strict=True):
        require((cell["crops"], cell["livestock"]) == pair)
        cells.append({"crops": pair[0], "livestock": pair[1], "count": count(cell["count"])})
    require(sum(c["count"] for c in cells) == denominator)
    for index, key in enumerate(("crops", "livestock")):
        require(denominator <= activities[index]["denominator"])
        for response in ("yes", "no"):
            joint = sum(c["count"] for c in cells if c[key] == response)
            require(joint <= activities[index][response] <= joint + excluded)
    plots = {key: count(data["plots"][key]) for key in
             ("total", "missing_area", "recorded_area")}
    require(plots["total"] == plots["missing_area"] + plots["recorded_area"])
    require(len(data["plot_types"]) == 3)
    types = []
    for item, code in zip(data["plot_types"], (1, 2, 3), strict=True):
        require(type(item["code"]) is int and item["code"] == code)
        require(type(item["label"]) is str)
        types.append({"code": code, "label": item["label"], "count": count(item["count"])})
    require(sum(t["count"] for t in types) == plots["total"])
    return {"activities": activities, "overlap": {"denominator": denominator,
                "excluded": excluded, "cells": cells}, "plots": plots, "plot_types": types}


def build_bundle(root: Path, manifest: dict | None = None) -> dict:
    """Offline manifest overrides support fixtures, never a website input."""
    try:
        manifest = manifest or strict_json(files("agrisight").joinpath(
            "reporting/stakeholder_manifest_v1.json").read_bytes())
        require(manifest["purpose"] in ("REVIEWED LOCAL EVIDENCE", "TEST FIXTURE"))
        data, _ = load_artifact(root, "stakeholder_sa1.json", manifest["artifact"])
        result = project(data)
        if manifest["purpose"] != "TEST FIXTURE":
            old = manifest_resource()["artifacts"]
            crop = nass01(load_artifact(root, "nass01.json", old["nass01.json"])[0])
            area = nass02(load_artifact(root, "nass02.json", old["nass02.json"])[0])
            require(crop["counts"]["numerator"] == result["activities"][0]["yes"])
            require(crop["counts"]["input_rows"] == result["activities"][0]["input_rows"])
            require(area["counts"]["total_plots"] == result["plots"]["total"])
            require(area["counts"]["missing_areas"] == result["plots"]["missing_area"])
        return dict(status="available", origin=manifest["purpose"], **result)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return {"status": "unavailable"}
