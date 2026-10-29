"""TEST FIXTURE aggregates only: no restricted source data or production fallback."""

import copy
import hashlib
import json
import statistics
import subprocess
import sys
from datetime import UTC, datetime

import pytest

from agrisight import reporting_adapter as adapter

NOW = datetime(2026, 10, 29, tzinfo=UTC)


def m(universe, tp=0, fp=0, fn=0):
    tn = universe-tp-fp-fn
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "universe": universe,
            "true_pairs_or_labels": tp+fn, "predicted_pairs_or_labels": tp+fp,
            "precision": tp/(tp+fp) if tp+fp else None,
            "recall": tp/(tp+fn) if tp+fn else None,
            "false_positive_rate": fp/(fp+tn) if fp+tn else None}


def metrics(n, collision=False):
    pairs = n*(n-1)//2
    return {"same_person": m(pairs, fp=pairs if collision else 0),
            "duplicate_role": m(pairs, fp=pairs if collision else 0),
            "quality": m(n*4), "quality_by_rule": {r: m(n) for r in adapter.RULES}}


def summarized(values):
    return {"values": values, "minimum": min(values), "median": statistics.median(values),
            "maximum": max(values), "sample_stdev": statistics.stdev(values)}


def fixture_data():
    first = {"indicator": "NASS-01", "contract_version": "1.0", "model_version": "1.0",
             "counts_and_rates": {"input_rows": 4, "numerator": 2, "denominator": 3,
                                  "no_count": 1, "missing_count": 1, "invalid_count": 0,
                                  "excluded_count": 1, "proportion": 2/3, "percentage": 200/3}}
    second = {"indicator": "NASS-02", "contract_version": "1.0", "model_version": "1.0",
              "estimates": {"total_plots": 3, "observed_areas": 2, "missing_areas": 1,
                            "middle_lower_rank": 2, "middle_upper_rank": 2,
                            "observed_only_median_m2": 4, "full_roster_lower_m2": 3,
                            "full_roster_upper_m2": 5, "width_m2": 2, "status": "bounded"}}
    runs = [{"seed": s, "configuration": c, "events": 3, "people": 3, "intended_roles": 3,
             "baselines": {b: {"metrics": metrics(3)} for b in ("B0", "B1")}}
            for s in (303, 404, 505) for c in adapter.CONFIGS]
    cases = []
    for n, collision in [(1000, False), (10000, False), (55000, False), (100000, False),
                          (300, True), (1000, True)]:
        rejected = collision and n == 1000
        status = "candidate_budget_exceeded" if rejected else "success"
        ref = {"events": n, "people": n, "intended_roles": n,
               "candidate_pairs": n*(n-1)//2 if collision else 0, "status": status,
               "observations_sha256": "0"*64, "truth_sha256": "1"*64}
        if not rejected:
            ref.update(prediction_sha256="2"*64, accuracy={"metrics": metrics(n, collision)})
        row = {k: v for k, v in ref.items() if k not in ("accuracy", "candidate_pairs")}
        row["validation"] = "pass"
        timings = [{**row, "seconds": v} for v in (1, 2, 3, 4, 5)]
        memories = [] if rejected else [{**row, "peak_traced_mib": v} for v in (10, 11, 12)]
        cases.append({"size": n, "collision": collision, "reference": ref, "verified": True,
                      "warmup": row, "timing_runs": timings, "memory_runs": memories,
                      "timing_seconds": None if rejected else summarized([1, 2, 3, 4, 5]),
                      "memory_peak_traced_mib": None if rejected else summarized([10, 11, 12])})
    return {"nass01.json": first, "nass02.json": second,
            "m3_04_evaluation.json": {"contract_version": "1.0", "runs": runs},
            "m3_05_benchmark.json": {"version": "1.0", "pair_budget": 250000, "cases": cases}}


def write_fixture(root, data):
    private = root/"reports/private"
    private.mkdir(parents=True, exist_ok=True)
    manifest = {"manifest_version": "1.0", "purpose": "TEST FIXTURE",
                "observed_date": "2026-10-29", "artifacts": {}}
    for name, obj in data.items():
        raw = (json.dumps(obj)+"\n").encode()
        (private/name).write_bytes(raw)
        manifest["artifacts"][name] = {"sha256": hashlib.sha256(raw).hexdigest(),
                                       "expected": {"contract_version": "1.0"}
                                       if name != "m3_05_benchmark.json" else {"version": "1.0"}}
    return manifest


def build(root, data):
    return adapter.build_bundle(root, write_fixture(root, data), NOW)


def test_known_truth_projection_and_source_separation(tmp_path):
    result = build(tmp_path, fixture_data())
    assert all(p["status"] == "available" for p in result["panels"].values())
    assert all(p["origin"] == "TEST FIXTURE" for p in result["panels"].values())
    assert result["built_at_utc"] == NOW.isoformat()
    survey = result["panels"]["survey"]["records"]
    assert survey[0]["counts"]["denominator"] == 3
    assert survey[0]["values"]["proportion"] == 2/3
    assert survey[1]["values"]["width_m2"] == 2
    assert len(result["panels"]["synthetic_quality"]["records"]) == 126
    benchmark = result["panels"]["synthetic_workload"]["records"]
    assert benchmark[2]["counts"]["events"] == 55000
    assert benchmark[2]["values"]["timing"]["median"] == 3
    assert benchmark[-1]["status"] == "candidate_budget_exceeded"
    assert benchmark[-1]["values"]["timing"] is None


@pytest.mark.parametrize("field,value", [("numerator", -1), ("denominator", True),
                                        ("no_count", 2), ("percentage", 7),
                                        ("proportion", None)])
def test_bad_survey_counts_rates_block_entire_survey_only(tmp_path, field, value):
    data = fixture_data()
    data["nass01.json"]["counts_and_rates"][field] = value
    result = build(tmp_path, data)
    assert result["panels"]["survey"]["status"] == "unavailable"
    assert result["panels"]["survey"]["records"] == []
    assert result["panels"]["synthetic_quality"]["status"] == "available"


def test_zero_denominator_is_null_not_zero(tmp_path):
    data = fixture_data()
    c = data["nass01.json"]["counts_and_rates"]
    c.update(input_rows=1, numerator=0, denominator=0, no_count=0, missing_count=1,
             invalid_count=0, excluded_count=1, proportion=None, percentage=None)
    row = build(tmp_path, data)["panels"]["survey"]["records"][0]
    assert row["status"] == "undefined" and row["values"]["percentage"] is None


@pytest.mark.parametrize("status", ["undefined", "unbounded"])
def test_area_empty_and_unbounded_distinct(tmp_path, status):
    data = fixture_data()
    e = data["nass02.json"]["estimates"]
    n = 0 if status == "undefined" else 1
    e.update(total_plots=n, observed_areas=0, missing_areas=n,
             middle_lower_rank=1 if n else None, middle_upper_rank=1 if n else None,
             observed_only_median_m2=None, full_roster_lower_m2=0 if n else None,
             full_roster_upper_m2=None, width_m2=None, status=status)
    row = build(tmp_path, data)["panels"]["survey"]["records"][1]
    assert row["status"] == status
    assert row["values"]["full_roster_upper_m2"] is None


@pytest.mark.parametrize("key,value", [("width_m2", 99), ("middle_lower_rank", True),
                                      ("full_roster_upper_m2", 1), ("status", "undefined"),
                                      ("observed_only_median_m2", None)])
def test_invalid_area_states(tmp_path, key, value):
    data = fixture_data()
    data["nass02.json"]["estimates"][key] = value
    assert build(tmp_path, data)["panels"]["survey"]["status"] == "unavailable"


def test_recorded_zero_is_valid_area(tmp_path):
    data = fixture_data()
    e = data["nass02.json"]["estimates"]
    e.update(total_plots=1, observed_areas=1, missing_areas=0, middle_lower_rank=1,
             middle_upper_rank=1, observed_only_median_m2=0, full_roster_lower_m2=0,
             full_roster_upper_m2=0, width_m2=0)
    row = build(tmp_path, data)["panels"]["survey"]["records"][1]
    assert row["status"] == "bounded" and row["values"]["full_roster_lower_m2"] == 0


@pytest.mark.parametrize("case", ["seed", "baseline", "counts", "rate", "rules", "boolean"])
def test_quality_rejects_wrong_cells_and_arithmetic(tmp_path, case):
    data = fixture_data()
    run = data["m3_04_evaluation.json"]["runs"][0]
    metric = run["baselines"]["B0"]["metrics"]["same_person"]
    if case == "seed":
        run["seed"] = 101
    elif case == "baseline":
        run["baselines"].pop("B1")
    elif case == "counts":
        metric["tp"] = 3
    elif case == "rate":
        metric["precision"] = 1
    elif case == "rules":
        run["baselines"]["B0"]["metrics"]["quality_by_rule"].pop("missing_name")
    else:
        metric["tn"] = True
    assert build(tmp_path, data)["panels"]["synthetic_quality"]["status"] == "unavailable"


@pytest.mark.parametrize("case", ["median", "repeat_count", "hash", "status", "verified",
                                  "collision_type", "rejection_as_zero"])
def test_benchmark_rejects_inconsistent_repeats_and_states(tmp_path, case):
    data = fixture_data()
    c = data["m3_05_benchmark.json"]["cases"][0]
    if case == "median":
        c["timing_seconds"]["median"] = 0
    elif case == "repeat_count":
        c["timing_runs"].pop()
    elif case == "hash":
        c["timing_runs"][0]["prediction_sha256"] = "3"*64
    elif case == "status":
        c["timing_runs"][0]["status"] = "timeout"
    elif case == "verified":
        c["verified"] = 1
    elif case == "collision_type":
        c["collision"] = 0
    else:
        data["m3_05_benchmark.json"]["cases"][-1]["timing_seconds"] = 0
    assert build(tmp_path, data)["panels"]["synthetic_workload"]["status"] == "unavailable"


@pytest.mark.parametrize("case", ["missing", "hash", "version", "json", "duplicate_key",
                                  "nonfinite", "overflow"])
def test_file_integrity_and_parse_failures(tmp_path, case):
    manifest = write_fixture(tmp_path, fixture_data())
    path = tmp_path/"reports/private/nass01.json"
    if case == "missing":
        path.unlink()
    elif case == "version":
        manifest["artifacts"]["nass01.json"]["expected"]["contract_version"] = "2.0"
    elif case == "hash":
        path.write_text('{}', encoding='utf-8')
    else:
        raw = {"json": b'{', "duplicate_key": b'{"a":1,"a":2}',
               "nonfinite": b'{"a":NaN}', "overflow": b'{"a":1e999}'}[case]
        path.write_bytes(raw)
        manifest["artifacts"]["nass01.json"]["sha256"] = hashlib.sha256(raw).hexdigest()
    result = adapter.build_bundle(tmp_path, manifest, NOW)
    assert result["panels"]["survey"]["status"] == "unavailable"
    assert result["panels"]["synthetic_workload"]["status"] == "available"


def test_unknown_input_fields_cannot_leak(tmp_path):
    data = fixture_data()
    for obj in data.values():
        obj["unreviewed_private_path"] = "DO-NOT-FORWARD"
    data["nass01.json"]["counts_and_rates"]["name_token"] = "DO-NOT-FORWARD"
    result = build(tmp_path, data)
    assert "DO-NOT-FORWARD" not in json.dumps(result)
    assert "unreviewed_private_path" not in json.dumps(result)


def test_no_stale_success_after_artifact_change(tmp_path):
    manifest = write_fixture(tmp_path, fixture_data())
    assert adapter.build_bundle(tmp_path, manifest, NOW)["panels"]["survey"]["status"] == "available"
    (tmp_path/"reports/private/nass02.json").write_text('{}', encoding='utf-8')
    assert adapter.build_bundle(tmp_path, manifest, NOW)["panels"]["survey"]["status"] == "unavailable"


def test_path_escape_even_with_matching_manifest(tmp_path, monkeypatch):
    manifest = write_fixture(tmp_path, fixture_data())
    original = adapter.Path.resolve
    target = tmp_path/"reports/private/nass01.json"

    def resolve(path, *args, **kwargs):
        if path == target:
            return tmp_path/"outside.json"
        return original(path, *args, **kwargs)

    monkeypatch.setattr(adapter.Path, "resolve", resolve)
    result = adapter.build_bundle(tmp_path, manifest, NOW)
    assert result["artifacts"]["nass01.json"]["status"] == "unavailable"


def test_manifest_and_timezone_failures(tmp_path):
    manifest = write_fixture(tmp_path, fixture_data())
    with pytest.raises(ValueError):
        adapter.build_bundle(tmp_path, manifest, datetime(2026, 10, 29))
    bad = copy.deepcopy(manifest)
    bad["purpose"] = "unknown"
    with pytest.raises(ValueError):
        adapter.build_bundle(tmp_path, bad, NOW)


@pytest.mark.parametrize("value", [True, None, "z"*64, "0"*63])
def test_hash_values_must_be_sha256_hex(value):
    with pytest.raises(ValueError):
        adapter.checksum(value)


def test_cli_cannot_overwrite_evidence_or_escape(tmp_path, monkeypatch):
    import sys

    monkeypatch.chdir(tmp_path)
    for name in ("reports/private/nass01.json", "outside.json"):
        monkeypatch.setattr(sys, "argv", ["reporting_adapter", "--output", name])
        with pytest.raises(ValueError):
            adapter.main()


def test_cli_failure_does_not_emit_paths_or_tracebacks(tmp_path):
    result = subprocess.run([sys.executable, "-m", "agrisight.reporting_adapter", "--output",
                             str(tmp_path/"outside.json")], capture_output=True, text=True,
                            check=False)
    assert result.returncode == 1
    assert "Reporting evidence unavailable" in result.stdout
    assert "Traceback" not in result.stdout+result.stderr
    assert str(tmp_path) not in result.stdout+result.stderr
