"""Validate reviewed aggregate artifacts and project an allow-listed reporting bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from datetime import UTC, datetime
from importlib.resources import files
from pathlib import Path

NAMES = ("nass01.json", "nass02.json", "m3_04_evaluation.json", "m3_05_benchmark.json")
RULES = ("missing_name", "missing_contact", "name_whitespace", "contact_whitespace")
CONFIGS = ("Clean", "Exact-repeat", "Mixed")
METRIC_COUNTS = ("tp", "fp", "fn", "tn", "universe", "true_pairs_or_labels",
                 "predicted_pairs_or_labels")


def require(condition: bool) -> None:
    if not condition:
        raise ValueError("invalid_aggregate")


def count(value: object) -> int:
    require(type(value) is int and value >= 0)
    return value


def checksum(value: object) -> str:
    require(type(value) is str and len(value) == 64 and
            all(char in "0123456789abcdef" for char in value))
    return value


def number(value: object, nullable: bool = False) -> float | None:
    if value is None and nullable:
        return None
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0)
    return float(value)


def equal(a: object, b: object, tolerance: float = 1e-12) -> None:
    if a is None or b is None:
        require(a is b)
    else:
        number(a)
        number(b)
        require(math.isclose(a, b, abs_tol=tolerance, rel_tol=1e-12))


def strict_json(raw: bytes) -> dict:
    def pairs(items: list) -> dict:
        result = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result

    def constant(_: str) -> None:
        raise ValueError("invalid_json")

    result = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

    def finite(value: object) -> None:
        if isinstance(value, float):
            require(math.isfinite(value))
        elif isinstance(value, dict):
            for v in value.values():
                finite(v)
        elif isinstance(value, list):
            for v in value:
                finite(v)

    finite(result)
    require(isinstance(result, dict))
    return result


def manifest_resource() -> dict:
    return strict_json(files("agrisight").joinpath(
        "reporting/artifact_manifest_v2.json").read_bytes())


def record(identifier: str, selectors: dict, counts: dict, values: dict,
           units: dict, status: str = "defined") -> dict:
    return {"id": identifier, "selectors": selectors, "counts": counts,
            "values": values, "units": units, "status": status}


def nass01(data: dict) -> dict:
    c = data["counts_and_rates"]
    keys = ("input_rows", "numerator", "denominator", "no_count", "missing_count",
            "invalid_count", "excluded_count")
    counts = {k: count(c[k]) for k in keys}
    require(c["numerator"]+c["no_count"] == c["denominator"])
    require(c["missing_count"]+c["invalid_count"] == c["excluded_count"])
    require(c["denominator"]+c["excluded_count"] == c["input_rows"])
    proportion = c["numerator"]/c["denominator"] if c["denominator"] else None
    equal(c["proportion"], proportion)
    equal(c["percentage"], proportion*100 if proportion is not None else None)
    return record("NASS-01", {}, counts,
                  {"proportion": proportion, "percentage": c["percentage"]},
                  {"proportion": "fraction", "percentage": "percent"},
                  "defined" if proportion is not None else "undefined")


def nass02(data: dict) -> dict:
    e = data["estimates"]
    n, known, missing = (count(e[k]) for k in ("total_plots", "observed_areas", "missing_areas"))
    require(n == known+missing)
    r1, r2 = ((n+1)//2, (n+2)//2) if n else (None, None)
    for key, expected in (("middle_lower_rank", r1), ("middle_upper_rank", r2)):
        if expected is None:
            require(e[key] is None)
        else:
            require(count(e[key]) == expected)
    values = {k: number(e[k], nullable=True) for k in (
        "observed_only_median_m2", "full_roster_lower_m2", "full_roster_upper_m2", "width_m2")}
    reference, low, high, width = values.values()
    require((reference is None) == (known == 0))
    status = "undefined" if not n else "unbounded" if r2 > known else "bounded"
    require(e["status"] == status)
    if not n:
        require(all(v is None for v in values.values()))
    else:
        require(low is not None)
        if not known:
            equal(low, 0)
        if status == "unbounded":
            require(high is None and width is None)
        else:
            require(high is not None and low <= high)
            equal(width, high-low, 1e-9)
        if not missing:
            equal(low, reference, 1e-9)
            equal(high, reference, 1e-9)
    return record("NASS-02", {}, {k: e[k] for k in ("total_plots", "observed_areas",
                  "missing_areas", "middle_lower_rank", "middle_upper_rank")}, values,
                  {k: "released labelled square metres" for k in values}, status)


def metric(data: dict, universe: int) -> dict:
    result = {k: count(data[k]) for k in METRIC_COUNTS}
    tp, fp, fn, tn = (result[k] for k in ("tp", "fp", "fn", "tn"))
    require(result["universe"] == universe == tp+fp+fn+tn)
    require(result["true_pairs_or_labels"] == tp+fn)
    require(result["predicted_pairs_or_labels"] == tp+fp)
    for name, numerator, denominator in (("precision", tp, tp+fp), ("recall", tp, tp+fn),
                                          ("false_positive_rate", fp, fp+tn)):
        expected = numerator/denominator if denominator else None
        equal(data[name], expected)
        result[name] = expected
    return result


def dataset_counts(data: dict) -> dict:
    result = {k: count(data[k]) for k in ("events", "people", "intended_roles")}
    require(result["people"] <= result["intended_roles"] <= result["events"])
    require(result["intended_roles"] <= 2*result["people"])
    return result


def checked_metrics(metrics: dict, n: int) -> dict:
    output = {relation: metric(metrics[relation], n*(n-1)//2)
              for relation in ("same_person", "duplicate_role")}
    output["quality"] = metric(metrics["quality"], n*len(RULES))
    rules = {rule: metric(metrics["quality_by_rule"][rule], n) for rule in RULES}
    for key in METRIC_COUNTS:
        require(sum(r[key] for r in rules.values()) == output["quality"][key])
    output["quality_by_rule"] = rules
    require(output["duplicate_role"]["true_pairs_or_labels"] <=
            output["same_person"]["true_pairs_or_labels"])
    return output


def quality_records(data: dict) -> list[dict]:
    runs = data["runs"]
    expected = {(s, c) for s in (303, 404, 505) for c in CONFIGS}
    require(len(runs) == len(expected))
    require({(count(r["seed"]), r["configuration"]) for r in runs} == expected)
    output = []
    for run in runs:
        counts = dataset_counts(run)
        require(set(run["baselines"]) == {"B0", "B1"})
        previous = None
        for baseline in ("B0", "B1"):
            metrics = checked_metrics(run["baselines"][baseline]["metrics"], counts["events"])
            if previous is not None:
                for relation in ("same_person", "duplicate_role"):
                    require(metrics[relation]["true_pairs_or_labels"] ==
                            previous[relation]["true_pairs_or_labels"])
                require(metrics["quality"] == previous["quality"])
                require(metrics["quality_by_rule"] == previous["quality_by_rule"])
            previous = metrics
            cells = {k: metrics[k] for k in ("same_person", "duplicate_role", "quality")}
            cells.update(metrics["quality_by_rule"])
            for relation, m in cells.items():
                selectors = {"seed": run["seed"], "configuration": run["configuration"],
                             "baseline": baseline, "measure": relation}
                values = {k: m[k] for k in ("precision", "recall", "false_positive_rate")}
                output.append(record("synthetic_quality", selectors,
                                     {**counts, **{k: m[k] for k in METRIC_COUNTS}}, values,
                                     {k: "fraction" for k in values}))
    return output


def summary(rows: list, field: str) -> dict:
    values = [number(r[field]) for r in rows]
    return {"values": values, "minimum": min(values), "median": statistics.median(values),
            "maximum": max(values), "sample_stdev": statistics.stdev(values)}


def benchmark_records(data: dict) -> list[dict]:
    require(count(data["pair_budget"]) == 250000)
    cases = data["cases"]
    expected = {(n, False) for n in (1000, 10000, 55000, 100000)} | {(300, True), (1000, True)}
    require(len(cases) == len(expected))
    for case in cases:
        require(type(case["collision"]) is bool)
        count(case["size"])
    require({(c["size"], c["collision"]) for c in cases} == expected)
    records = []
    for case in cases:
        ref = case["reference"]
        counts = dataset_counts(ref)
        require(counts["events"] == case["size"] and case["verified"] is True)
        candidates = count(ref["candidate_pairs"])
        rejected = candidates > data["pair_budget"]
        require(rejected == (case["collision"] and case["size"] == 1000))
        if case["collision"]:
            require(candidates == case["size"]*(case["size"]-1)//2)
        status = "candidate_budget_exceeded" if rejected else "success"
        require(ref["status"] == status)
        require(len(case["timing_runs"]) == 5)
        require(len(case["memory_runs"]) == (0 if rejected else 3))
        for row in [case["warmup"], *case["timing_runs"], *case["memory_runs"]]:
            require(row["validation"] == "pass" and row["status"] == status)
            require(dataset_counts(row) == counts)
            for key in ("observations_sha256", "truth_sha256"):
                require(checksum(row[key]) == checksum(ref[key]))
            if not rejected:
                require(checksum(row["prediction_sha256"]) == checksum(ref["prediction_sha256"]))
        if rejected:
            require(case["timing_seconds"] is None and case["memory_peak_traced_mib"] is None)
            timing = memory = None
        else:
            metrics = checked_metrics(ref["accuracy"]["metrics"], counts["events"])
            require(metrics["same_person"]["predicted_pairs_or_labels"] == candidates)
            timing = summary(case["timing_runs"], "seconds")
            memory = summary(case["memory_runs"], "peak_traced_mib")
            for name, expected_summary in (("timing_seconds", timing),
                                            ("memory_peak_traced_mib", memory)):
                observed = case[name]
                require(len(observed["values"]) == len(expected_summary["values"]))
                for a, b in zip(observed["values"], expected_summary["values"]):
                    equal(a, b)
                for key in ("minimum", "median", "maximum", "sample_stdev"):
                    equal(observed[key], expected_summary[key])
        records.append(record("synthetic_workload", {"events": case["size"],
                              "collision": case["collision"]},
                              {**counts, "candidate_pairs": candidates, "pair_budget": 250000},
                              {"timing": timing, "traced_allocation": memory},
                              {"timing": "seconds", "traced_allocation": "MiB"}, status))
    return records


def load_artifact(root: Path, name: str, entry: dict) -> tuple[dict, str]:
    path = (root/"reports/private"/name).resolve()
    require(path.is_relative_to(root.resolve()/"reports/private"))
    raw = path.read_bytes()
    actual_checksum = hashlib.sha256(raw).hexdigest()
    require(actual_checksum == checksum(entry["sha256"]))
    data = strict_json(raw)
    for dotted, expected in entry["expected"].items():
        actual = data
        for part in dotted.split("."):
            actual = actual[part]
        require(actual == expected and type(actual) is type(expected))
        if dotted.endswith("_sha256") or dotted.startswith("sha256."):
            checksum(actual)
    return data, actual_checksum


def build_bundle(root: Path, manifest: dict | None = None,
                 built_at: datetime | None = None) -> dict:
    """Alternate manifests are for offline fixture tests, never a UI trust decision."""
    manifest = manifest_resource() if manifest is None else manifest
    require(manifest["manifest_version"] == "1.0")
    require(manifest["purpose"] in ("REVIEWED LOCAL EVIDENCE", "TEST FIXTURE"))
    require(set(manifest["artifacts"]) == set(NAMES))
    timestamp = built_at or datetime.now(UTC)
    require(timestamp.tzinfo is not None and timestamp.utcoffset() is not None)
    loaded, statuses = {}, {}
    for name in NAMES:
        try:
            loaded[name], checksum = load_artifact(root, name, manifest["artifacts"][name])
            statuses[name] = {"sha256": checksum, "status": "verified"}
        except (OSError, ValueError, KeyError, TypeError, OverflowError, RecursionError):
            statuses[name] = {"sha256": None, "status": "unavailable"}
    definitions = {
        "survey": (("nass01.json", "nass02.json"),
                   "NBS NASS released survey aggregates", "April-October 2022",
                   ["Unweighted pooled sample; no population confidence intervals.",
                    "Area measurement lineage unverified; bounds address missing values only."]),
        "synthetic_quality": (("m3_04_evaluation.json",), "SYNTHETIC DEMONSTRATION DATA",
                              "Fixed reserved seeds 303/404/505",
                              ["No field accuracy claim or automatic merging.",
                               "Pair and event-rule universes are distinct."]),
        "synthetic_workload": (("m3_05_benchmark.json",), "SYNTHETIC DEMONSTRATION DATA",
                               "Fixed seed707/808 local batch experiment",
                               ["Shared machine; generation/import/startup/hashing/SQL/I/O excluded.",
                                "Traced allocation excludes existing inputs/native memory; not RSS.",
                                "Bounded keys; not a production capacity guarantee."]),
    }
    panels = {}
    for key, (names, origin, period, limits) in definitions.items():
        panel = {"origin": "TEST FIXTURE" if manifest["purpose"] == "TEST FIXTURE" else origin,
                 "reference_period": period, "observed_date": manifest["observed_date"],
                 "limitations": limits, "status": "unavailable", "records": [], "provenance": {}}
        try:
            require(all(name in loaded for name in names))
            if key == "survey":
                records = [nass01(loaded[names[0]]), nass02(loaded[names[1]])]
            elif key == "synthetic_quality":
                records = quality_records(loaded[names[0]])
            else:
                records = benchmark_records(loaded[names[0]])
            panel.update(status="available", records=records,
                         provenance={name: manifest["artifacts"][name]["expected"]
                                     for name in names})
        except (ValueError, KeyError, TypeError, OverflowError, IndexError):
            panel["message"] = "Evidence unavailable. Revalidate the reviewed aggregate artifacts."
        panels[key] = panel
    return {"report_contract_version": "1.0", "built_at_utc": timestamp.astimezone(
        UTC).isoformat(), "artifacts": statuses, "panels": panels}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    require(args.output.resolve().is_relative_to(root/"reports/private"))
    require(args.output.resolve() not in {(root/"reports/private"/n).resolve() for n in NAMES})
    result = build_bundle(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print("Reporting bundle saved under ignored reports/private")
    if any(p["status"] != "available" for p in result["panels"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print("Reporting evidence unavailable. Verify the reviewed inputs and output location.")
        raise SystemExit(1) from None
