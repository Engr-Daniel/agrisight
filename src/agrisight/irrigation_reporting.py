"""Independently optional, reviewed aggregate Water Management projection."""

from importlib.resources import files
from pathlib import Path

from agrisight.reporting_adapter import count, equal, load_artifact, require, strict_json


def project(data: dict, plot_total: int) -> dict:
    require(data["version"] == "1.0")
    raw = data["infrastructure"]
    presence = {k: count(raw[k]) for k in ("input_rows", "yes", "no", "missing", "invalid", "denominator")}
    require(presence["input_rows"] == plot_total)
    require(presence["yes"] + presence["no"] == presence["denominator"])
    require(presence["denominator"] + presence["missing"] + presence["invalid"] == plot_total)
    presence["share"] = presence["yes"]/presence["denominator"] if presence["denominator"] else None
    equal(raw["share"], presence["share"])
    result = {"infrastructure": presence}
    for name, codes in (("method", (*range(1, 9), 99)), ("source", (*range(1, 7), 99))):
        raw = data[name]
        values = {k: count(raw[k]) for k in ("eligible", "denominator", "missing", "invalid",
                                             "outside_yes", "populated_outside_yes")}
        require(values["eligible"] == presence["yes"])
        require(values["eligible"] == values["denominator"] + values["missing"] + values["invalid"])
        require(values["outside_yes"] + values["eligible"] == plot_total)
        require(values["populated_outside_yes"] == 0)
        require(len(raw["categories"]) == len(codes))
        categories = []
        for item, code in zip(raw["categories"], codes, strict=True):
            require(type(item["code"]) is int and item["code"] == code)
            require(type(item["label"]) is str)
            n = count(item["count"])
            share = n/values["denominator"] if values["denominator"] else None
            equal(item["share"], share)
            categories.append({"code": code, "label": item["label"], "count": n, "share": share})
        require(sum(c["count"] for c in categories) == values["denominator"])
        result[name] = {**values, "categories": categories}
    return result


def build_bundle(root: Path, plot_total: int, manifest: dict | None = None) -> dict:
    try:
        manifest = manifest or strict_json(files("agrisight").joinpath(
            "reporting/irrigation_manifest_v1.json").read_bytes())
        require(manifest["purpose"] in ("REVIEWED LOCAL EVIDENCE", "TEST FIXTURE"))
        data, _ = load_artifact(root, "irrigation_ir1.json", manifest["artifact"])
        return {"status": "available", "origin": manifest["purpose"], **project(data, plot_total)}
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return {"status": "unavailable"}
