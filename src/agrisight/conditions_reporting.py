"""Fail-closed FC1 aggregate validation and allow-listed stakeholder projection."""

from importlib.resources import files
from pathlib import Path

from agrisight.farming_conditions import BRANCHES, MODULES, metadata
from agrisight.reporting_adapter import count, equal, load_artifact, require, strict_json


def category(data: dict, labels: dict) -> dict:
    values = {k: count(data[k]) for k in ("eligible", "valid", "missing", "invalid")}
    require(values["eligible"] == values["valid"]+values["missing"]+values["invalid"])
    require(len(data["rows"]) == len(labels))
    rows = []
    for row, code in zip(data["rows"], sorted(map(int, labels)), strict=True):
        require(type(row["code"]) is int and row["code"] == code and row["label"] == labels[str(code)])
        n = count(row["count"])
        share = n/values["valid"] if values["valid"] else None
        equal(row["share"], share)
        rows.append({"code": code, "label": labels[str(code)], "count": n, "share": share})
    require(sum(r["count"] for r in rows) == values["valid"])
    return {**values, "rows": rows}


def project(data: dict, household_total: int, plot_total: int) -> dict:
    require(data["version"] == "1.0")
    ref = metadata()
    counts = {k: count(data["counts"][k]) for k in ("households", "plots", "crops", "harvest", "inputs")}
    require(counts["households"] == household_total and counts["plots"] == plot_total)

    def checked(value, module, field):
        return category(value, ref[module]["value_labels"][field])

    raw = data["land"]
    land = {name: checked(raw[name], MODULES[0], field) for name, field in
            (("tenure", "s02_q04"), ("transport", "s02_q05"), ("travel", "s02_q06"))}
    require(land["tenure"]["eligible"] == land["transport"]["eligible"] == plot_total)
    for key in ("on_dwelling", "unknown_transport", "outside_travel_answers"):
        land[key] = count(raw[key])
    require(land["on_dwelling"] == land["transport"]["rows"][-1]["count"])
    require(land["unknown_transport"] == land["transport"]["missing"]+land["transport"]["invalid"])
    require(land["travel"]["eligible"]+land["on_dwelling"]+land["unknown_transport"] == plot_total)
    require(land["outside_travel_answers"] <= land["on_dwelling"]+land["unknown_transport"])

    raw = data["difficulties"]
    difficulties = {k: count(raw[k]) for k in ("temporary_records", "excluded_permanent", "unassigned", "ambiguous")}
    require(difficulties["temporary_records"]+difficulties["excluded_permanent"] == counts["crops"])
    require(len(raw["branches"]) == 2)
    branches = []
    for value, (name, any_field, complete_field, shock_field, no_prefix, shock_prefix) in zip(raw["branches"], BRANCHES, strict=True):
        require(value["name"] == name)
        branch = {"name": name, "harvest": checked(value["harvest"], MODULES[1], any_field),
                  "completion": checked(value["completion"], MODULES[1], complete_field),
                  "shocks": checked(value["shocks"], MODULES[1], shock_field),
                  "outside_shock_answers": count(value["outside_shock_answers"])}
        require(branch["completion"]["eligible"] == branch["harvest"]["rows"][0]["count"])
        require(branch["shocks"]["eligible"] == branch["completion"]["rows"][1]["count"])
        require(branch["outside_shock_answers"] <= branch["harvest"]["eligible"]-branch["shocks"]["eligible"])
        for key, prefix, eligible in (("no_harvest_reasons", no_prefix, branch["harvest"]["rows"][1]["count"]),
                                     ("shock_reasons", shock_prefix, branch["shocks"]["rows"][0]["count"])):
            fields = [k for k in ref[MODULES[1]]["labels"] if k.startswith(prefix)]
            require(len(value[key]) == len(fields))
            branch[key] = []
            for reason, field in zip(value[key], fields, strict=True):
                label = ref[MODULES[1]]["labels"][field].split(":")[-1].strip()
                require(reason["field"] == field and reason["label"] == label)
                item = checked(reason, MODULES[1], field)
                require(item["eligible"] == eligible)
                branch[key].append({"field": field, "label": label, **item})
        branches.append(branch)
    require(sum(b["harvest"]["eligible"] for b in branches)+difficulties["unassigned"]+difficulties["ambiguous"] == difficulties["temporary_records"])
    difficulties["branches"] = branches

    fields = (("sales", "s01b_q02"), ("storage", "s01b_q20"), ("losses", "s01b_q11"))
    raw = data["destinations"]
    destinations = {name: checked(raw[name], MODULES[2], field) for name, field in fields}
    require(all(d["eligible"] == counts["harvest"] for d in destinations.values()))
    crops, seen = [], set()
    for crop in raw["crops"]:
        code = count(crop["code"])
        label = ref[MODULES[2]]["value_labels"]["s01b_harvestedCrops__id"].get(str(code))
        require(label is not None and crop["label"] == label and code not in seen)
        seen.add(code)
        row = {"code": code, "label": label, **{name: checked(crop[name], MODULES[2], field) for name, field in fields}}
        require(row["sales"]["eligible"] == row["storage"]["eligible"] == row["losses"]["eligible"] > 0)
        crops.append(row)
    for name, _ in fields:
        for key in ("eligible", "valid", "missing", "invalid"):
            require(sum(c[name][key] for c in crops) == destinations[name][key])
        for index in range(2):
            require(sum(c[name]["rows"][index]["count"] for c in crops) == destinations[name]["rows"][index]["count"])
    # Only adequately sized per-crop denominators enter the website projection.
    destinations["crops"] = [c for c in crops if all(c[n]["valid"] >= 30 for n, _ in fields)]
    destinations["omitted_crop_categories"] = len(crops)-len(destinations["crops"])
    joint = raw["overlap"]
    valid, excluded = count(joint["valid"]), count(joint["excluded"])
    require(valid+excluded == counts["harvest"] and len(joint["cells"]) == 4)
    cells = []
    for cell, (a, b) in zip(joint["cells"], ((1, 1), (1, 2), (2, 1), (2, 2)), strict=True):
        require(type(cell["sales"]) is int and type(cell["storage"]) is int and cell["sales"] == a and cell["storage"] == b)
        cells.append({"sales": a, "storage": b, "count": count(cell["count"])})
    require(sum(c["count"] for c in cells) == valid)
    for name in ("sales", "storage"):
        require(valid <= destinations[name]["valid"])
        for index in range(2):
            marginal = sum(c["count"] for c in cells if c[name] == index+1)
            require(marginal <= destinations[name]["rows"][index]["count"] <= marginal+excluded)
    destinations["overlap"] = {"valid": valid, "excluded": excluded, "cells": cells}

    inputs, seen = [], set()
    for row in data["inputs"]:
        code, n = count(row["code"]), count(row["records"])
        label = ref[MODULES[3]]["value_labels"]["s03c_inputType__id"].get(str(code))
        require(label is not None and row["label"] == label and code not in seen and n > 0)
        seen.add(code)
        require(len(row["statuses"]) == 4)
        statuses = []
        for value, status in zip(row["statuses"], ("Positive", "Zero", "Missing", "Invalid"), strict=True):
            require(value["label"] == status)
            number = count(value["count"])
            equal(value["share"], number/n)
            statuses.append({"label": status, "count": number, "share": number/n})
        require(sum(s["count"] for s in statuses) == n)
        inputs.append({"code": code, "label": label, "records": n, "statuses": statuses})
    require(sum(r["records"] for r in inputs) == counts["inputs"])
    return {"counts": counts, "land": land, "difficulties": difficulties, "destinations": destinations, "inputs": inputs}


def build_bundle(root: Path, household_total: int, plot_total: int, origin: str,
                 manifest: dict | None = None) -> dict:
    try:
        manifest = manifest or strict_json(files("agrisight").joinpath("reporting/conditions_manifest_v1.json").read_bytes())
        require(manifest["purpose"] == origin and origin in ("REVIEWED LOCAL EVIDENCE", "TEST FIXTURE"))
        data, _ = load_artifact(root, "farming_conditions_fc1.json", manifest["artifact"])
        return {"status": "available", "origin": origin, **project(data, household_total, plot_total)}
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return {"status": "unavailable"}
