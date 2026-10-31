"""Read-only SS1 projection; source combinations have complete-vector denominators."""

from importlib.resources import files
from pathlib import Path

from agrisight.reporting_adapter import count, equal, load_artifact, require, strict_json


def project(data: dict, household_total: int, crop_yes: int) -> dict:
    require(data["version"] == "1.0" and data["variety_status"] == "interpretation_not_verified")
    c = {k: count(data["counts"][k]) for k in ("household_records", "seed_rows", "eligible_records",
        "excluded_permanent_records", "represented_households", "crop_yes_without_temporary_seed_record",
        "temporary_seed_households_without_crop_yes")}
    n = c["eligible_records"]
    require(c["household_records"] == household_total)
    require(n + c["excluded_permanent_records"] == c["seed_rows"])
    require(c["represented_households"] <= min(n, household_total))
    require(c["temporary_seed_households_without_crop_yes"] <= c["represented_households"])
    require(c["crop_yes_without_temporary_seed_record"] <= crop_yes)
    require(c["represented_households"] - c["temporary_seed_households_without_crop_yes"] +
            c["crop_yes_without_temporary_seed_record"] == crop_yes)
    require(len(data["sources"]) == 5)
    sources = []
    for index, row in enumerate(data["sources"], 1):
        require(type(row["id"]) is int and row["id"] == index and type(row["label"]) is str)
        values = {k: count(row[k]) for k in ("yes", "no", "missing", "invalid", "denominator")}
        require(values["yes"] + values["no"] == values["denominator"])
        require(values["denominator"] + values["missing"] + values["invalid"] == n)
        share = values["yes"]/values["denominator"] if values["denominator"] else None
        equal(row["share"], share)
        sources.append({"id": index, "label": row["label"], "share": share, **values})
    raw = data["combinations"]
    complete, excluded = count(raw["denominator"]), count(raw["excluded"])
    require(complete + excluded == n)
    combos, seen = [], set()
    for row in raw["rows"]:
        mask, value = count(row["mask"]), count(row["records"])
        require(mask <= 31 and mask not in seen and value > 0)
        seen.add(mask)
        share = value/complete if complete else None
        equal(row["share"], share)
        combos.append({"mask": mask, "records": value, "share": share})
    require(sum(r["records"] for r in combos) == complete)
    for index, source in enumerate(sources):
        require(complete <= source["denominator"])
        for yes, key in ((True, "yes"), (False, "no")):
            joint = sum(r["records"] for r in combos if bool(r["mask"] & (1 << index)) == yes)
            require(joint <= source[key] <= joint + excluded)
    ordered = sorted(combos, key=lambda r: (-r["records"], r["mask"]))
    named = [r for r in ordered[:6] if r["records"] >= 30]
    residual = complete - sum(r["records"] for r in named)
    suppressed = complete < 30 or 0 < residual < 30
    published = [] if suppressed else list(named)
    if residual and not suppressed:
        published.append({"mask": None, "records": residual, "share": residual/complete})
    return {"counts": c, "sources": sources, "combinations": {
        "denominator": complete, "excluded": excluded, "rows": published, "suppressed": suppressed},
        "variety_status": "interpretation_not_verified"}


def build_bundle(root: Path, household_total: int, crop_yes: int, manifest: dict | None = None) -> dict:
    try:
        manifest = manifest or strict_json(files("agrisight").joinpath("reporting/seed_manifest_v1.json").read_bytes())
        require(manifest["purpose"] in ("REVIEWED LOCAL EVIDENCE", "TEST FIXTURE"))
        data, _ = load_artifact(root, "seed_sources_ss1.json", manifest["artifact"])
        return {"status": "available", "origin": manifest["purpose"], **project(data, household_total, crop_yes)}
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return {"status": "unavailable"}
