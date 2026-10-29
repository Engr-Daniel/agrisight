"""Benchmark correctness and failure handling, without hardware speed assertions."""

import json
import subprocess

import pytest

from agrisight import workload_benchmark as benchmark
from agrisight.synthetic_quality import Observation, validate


@pytest.mark.parametrize("size", [0, 1, 1399, 1400, 1401, 2800])
def test_exact_event_counts_namespaces_and_determinism(size):
    observations, truth = benchmark.workload(size)
    assert len(observations) == len(truth) == size
    validate(observations, truth)
    assert (observations, truth) == benchmark.workload(size)
    if size == 2800:
        assert len({t.true_person_id for t in truth}) == 2000
        assert len({t.true_role_id for t in truth}) == 2400
        assert benchmark.candidate_count(observations) == 2*benchmark.candidate_count(
            benchmark.workload(1400)[0])


@pytest.mark.parametrize("size", [-1, True, 1.5])
def test_bad_size(size):
    with pytest.raises(ValueError):
        benchmark.workload(size)


def test_normalization_missing_keys_and_pair_count():
    rows = [Observation("a", " SYN-A ", "SYN-C", "farmer", "accepted"),
            Observation("b", "syn-a", "syn-c", "processor", "pending"),
            Observation("c", "SYN-A", None, "farmer", "rejected"),
            Observation("d", " ", "SYN-C", "farmer", "pending")]
    assert benchmark.candidate_count(rows) == 1


def test_guard_rejects_before_detector(monkeypatch):
    def forbidden(*args):
        raise AssertionError("Detector must not run")

    monkeypatch.setattr(benchmark, "detect", forbidden)
    with pytest.raises(ValueError, match="candidate_budget_exceeded"):
        benchmark.batch(*benchmark.workload(1000, collision=True))
    reference = benchmark.reference(1000, True)
    assert reference["candidate_pairs"] == 499500
    assert reference["status"] == "candidate_budget_exceeded"


def test_collision_known_truth_and_traced_measurement():
    reference = benchmark.reference(4, True)
    metric = reference["accuracy"]["metrics"]["duplicate_role"]
    assert (metric["tp"], metric["fp"], metric["fn"], metric["tn"]) == (0, 6, 0, 0)
    measured = benchmark.worker(4, True, "memory")
    assert measured["peak_traced_mib"] >= 0
    assert measured["seconds"] is None
    assert measured["prediction_sha256"] == reference["prediction_sha256"]
    assert benchmark.worker(4, True, "timing")["seconds"] >= 0


def test_budget_boundary(monkeypatch):
    monkeypatch.setattr(benchmark, "PAIR_BUDGET", 1)
    assert len(benchmark.batch(*benchmark.workload(2, True))["same_person"]) == 1
    with pytest.raises(ValueError, match="candidate_budget_exceeded"):
        benchmark.batch(*benchmark.workload(3, True))


def test_summarize_preserves_outlier_and_failure():
    rows = [{"status": "success", "seconds": v} for v in (1, 2, 30)]
    rows.append({"status": "timeout"})
    result = benchmark.summarize(rows, "seconds")
    assert result["values"] == [1, 2, 30]
    assert result["median"] == 2
    assert result["maximum"] == 30
    assert benchmark.summarize([{"status": "timeout"}], "seconds") is None


@pytest.mark.parametrize("failure", ["timeout", "error", "json", "success"])
def test_worker_process_handling(monkeypatch, failure):
    def run(*args, **kwargs):
        assert kwargs["timeout"] == 120
        if failure == "timeout":
            raise subprocess.TimeoutExpired("worker", 120)
        return subprocess.CompletedProcess([], 1 if failure == "error" else 0,
                                           "oops" if failure == "json"
                                           else json.dumps({"status": "success"}))

    monkeypatch.setattr(benchmark.subprocess, "run", run)
    result = benchmark.invoke_worker(4, True, "timing")
    expected = {"timeout": "timeout", "error": "worker_error", "json": "invalid_worker_output",
                "success": "success"}[failure]
    assert result["status"] == expected


def test_cli_output_guard(monkeypatch, tmp_path):
    import sys

    output = tmp_path / "outside.json"
    monkeypatch.setattr(sys, "argv", ["benchmark", "--output", str(output)])
    with pytest.raises(ValueError, match="reports/private"):
        benchmark.main()
    assert not output.exists()
