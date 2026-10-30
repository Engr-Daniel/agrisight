"""Optional reviewed crop-roster projection with household-grain accounting."""

from importlib.resources import files
from pathlib import Path

from agrisight.reporting_adapter import count, equal, load_artifact, require, strict_json


def project(data: dict, households: int, plots: int, crop_yes: int) -> dict:
    require(data["version"] == "1.0")
    c = {k: count(data["counts"][k]) for k in (
        "household_records", "plot_records", "crop_rows", "temporary_rows", "excluded_permanent_rows",
        "unlabelled_permanent_rows", "represented_households", "household_crop_pairs",
        "crop_yes_households_without_temporary_record", "temporary_households_without_crop_yes")}
    require(c["household_records"] == households and c["plot_records"] == plots)
    require(c["temporary_rows"] + c["excluded_permanent_rows"] == c["crop_rows"])
    require(c["unlabelled_permanent_rows"] <= c["excluded_permanent_rows"])
    n, pairs = c["represented_households"], c["household_crop_pairs"]
    require(n <= households and n <= pairs <= c["temporary_rows"])
    require(c["temporary_households_without_crop_yes"] <= n)
    require(c["crop_yes_households_without_temporary_record"] <= crop_yes)
    require(n - c["temporary_households_without_crop_yes"] + c["crop_yes_households_without_temporary_record"] == crop_yes)
    mean = pairs/n if n else None
    equal(data["mean_categories"], mean)
    labels = strict_json(files("agrisight").joinpath("reporting/crop_labels_v1.json").read_bytes())
    portfolio, seen = [], set()
    for row in data["portfolio"]:
        code = row["code"]
        require(type(code) is int and str(code) in labels and code not in seen)
        require(row["label"] == labels[str(code)])
        seen.add(code)
        value = count(row["households"])
        require(0 < value <= n)
        equal(row["share"], value/n if n else None)
        portfolio.append({"code": code, "label": row["label"], "households": value, "share": value/n})
    require(sum(r["households"] for r in portfolio) == pairs)
    require((len(portfolio) == 0) == (n == 0))
    require(len(data["diversity"]) == 5)
    diversity = []
    for row, category in zip(data["diversity"], ("1", "2", "3", "4", "5+"), strict=True):
        require(row["categories"] == category)
        value = count(row["households"])
        equal(row["share"], value/n if n else None)
        diversity.append({"categories": category, "households": value, "share": value/n if n else None})
    require(sum(r["households"] for r in diversity) == n)
    lower = sum((i+1)*r["households"] for i, r in enumerate(diversity))
    upper = lower + max(len(portfolio)-5, 0)*diversity[-1]["households"]
    require(lower <= pairs <= upper and pairs <= n*len(portfolio))
    return {"counts": c, "mean_categories": mean, "portfolio": portfolio, "diversity": diversity}


def build_bundle(root: Path, households: int, plots: int, crop_yes: int, manifest: dict | None = None) -> dict:
    try:
        manifest = manifest or strict_json(files("agrisight").joinpath("reporting/crop_manifest_v1.json").read_bytes())
        require(manifest["purpose"] in ("REVIEWED LOCAL EVIDENCE", "TEST FIXTURE"))
        data, _ = load_artifact(root, "crop_portfolio_cp1.json", manifest["artifact"])
        return {"status": "available", "origin": manifest["purpose"], **project(data, households, plots, crop_yes)}
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return {"status": "unavailable"}
