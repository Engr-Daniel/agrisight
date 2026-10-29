"""SYNTHETIC DEMONSTRATION DATA: scoped local B1 batch benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import sqlite3
import statistics
import subprocess
import sys
import time
import tracemalloc
from collections import Counter
from dataclasses import asdict, replace
from pathlib import Path

from agrisight.synthetic_quality import (
    Observation,
    Truth,
    detect,
    digest,
    evaluate,
    generate,
    validate,
)

PAIR_BUDGET = 250000
SIZES = (1000, 10000, 55000, 100000)


def namespaced_token(value: str | None, block: int) -> str | None:
    if value is None:
        return None
    return value.replace("SYN-", f"SYN-B{block}-").replace("syn-", f"syn-b{block}-")


def workload(size: int, collision: bool = False) -> tuple[list[Observation], list[Truth]]:
    if type(size) is not int or size < 0:
        raise ValueError("Size must be a nonnegative integer")
    if collision:
        return ([Observation(f"SYN-EVENT-{i:06}", "SYN-SHARED", "SYN-CONTACT",
                             "farmer", "pending") for i in range(size)],
                [Truth(f"SYN-EVENT-{i:06}", f"p{i}", f"r{i}", "collision")
                 for i in range(size)])
    base, labels = generate(707, "Mixed")
    base.sort(key=lambda r: r.submission_id)
    lookup = {t.submission_id: t for t in labels}
    observations, truth = [], []
    block = 0
    while len(observations) < size:
        for row in base[:min(len(base), size-len(observations))]:
            sid = f"block-{block}-{row.submission_id}"

            observations.append(replace(row, submission_id=sid,
                                        name_token=namespaced_token(row.name_token, block),
                                        contact_token=namespaced_token(row.contact_token, block)))
            t = lookup[row.submission_id]
            truth.append(replace(t, submission_id=sid,
                                 true_person_id=f"block-{block}-{t.true_person_id}",
                                 true_role_id=f"block-{block}-{t.true_role_id}"))
        block += 1
    random.Random(808).shuffle(observations)
    return observations, truth


def candidate_count(observations: list[Observation]) -> int:
    groups = Counter()
    for row in observations:
        if row.name_token is not None and row.contact_token is not None:
            key = (row.name_token.strip().casefold(), row.contact_token.strip().casefold())
            if all(key):
                groups[key] += 1
    return sum(n*(n-1)//2 for n in groups.values())


def batch(observations: list[Observation], truth: list[Truth]) -> dict[str, set]:
    validate(observations, truth)
    if candidate_count(observations) > PAIR_BUDGET:
        raise ValueError("candidate_budget_exceeded")
    return detect(observations, "B1")


def input_manifest(observations: list[Observation], truth: list[Truth]) -> dict:
    return {"observations_sha256": digest(sorted([asdict(r) for r in observations],
                                                 key=lambda r: r["submission_id"])),
            "truth_sha256": digest(sorted([asdict(t) for t in truth],
                                          key=lambda t: t["submission_id"])),
            "events": len(observations), "people": len({t.true_person_id for t in truth}),
            "intended_roles": len({t.true_role_id for t in truth})}


def prediction_hash(predictions: dict[str, set]) -> str:
    return digest({name: sorted(pairs) for name, pairs in predictions.items()})


def reference(size: int, collision: bool) -> dict:
    observations, truth = workload(size, collision)
    manifest = input_manifest(observations, truth)
    count = candidate_count(observations)
    if count > PAIR_BUDGET:
        try:
            batch(observations, truth)
        except ValueError as exc:
            if str(exc) != "candidate_budget_exceeded":
                raise
        else:
            raise ValueError("Missing candidate guard")
        return {**manifest, "candidate_pairs": count, "status": "candidate_budget_exceeded"}
    result = evaluate(observations, truth, "B1")
    predictions = batch(observations, truth)
    with sqlite3.connect(":memory:") as db:
        db.execute("CREATE TABLE truth(id TEXT PRIMARY KEY,person TEXT,role TEXT)")
        db.executemany("INSERT INTO truth VALUES(?,?,?)",
                       [(t.submission_id, t.true_person_id, t.true_role_id) for t in truth])
        actual = db.execute("SELECT COUNT(*),COUNT(DISTINCT person),COUNT(DISTINCT role) "
                            "FROM truth").fetchone()
    if actual != tuple(manifest[k] for k in ("events", "people", "intended_roles")):
        raise ValueError("SQL count disagreement")
    return {**manifest, "candidate_pairs": count, "status": "success",
            "prediction_sha256": prediction_hash(predictions), "accuracy": result}


def worker(size: int, collision: bool, mode: str) -> dict:
    observations, truth = workload(size, collision)
    manifest = input_manifest(observations, truth)
    if mode == "memory":
        tracemalloc.start()
    started = time.perf_counter()
    try:
        predictions = batch(observations, truth)
    except ValueError as exc:
        if str(exc) != "candidate_budget_exceeded":
            raise
        return {**manifest, "status": "candidate_budget_exceeded"}
    elapsed = time.perf_counter()-started
    peak = tracemalloc.get_traced_memory()[1] if mode == "memory" else None
    if mode == "memory":
        tracemalloc.stop()
    return {**manifest, "status": "success", "prediction_sha256": prediction_hash(predictions),
            "seconds": elapsed if mode == "timing" else None,
            "peak_traced_mib": peak/(1024*1024) if peak is not None else None}


def invoke_worker(size: int, collision: bool, mode: str) -> dict:
    command = [sys.executable, "-m", "agrisight.workload_benchmark", "--worker",
               "--size", str(size), "--mode", mode]
    if collision:
        command.append("--collision")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    if result.returncode:
        # Avoid retaining filesystem paths or row-level values in aggregate diagnostics.
        return {"status": "worker_error", "returncode": result.returncode}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"status": "invalid_worker_output"}


def hardware() -> dict:
    info = {"os": platform.system(), "release": platform.release(),
            "architecture": platform.machine(), "processor": platform.processor(),
            "logical_processors": os.cpu_count(), "installed_ram_bytes": None,
            "python": platform.python_version(), "sqlite": sqlite3.sqlite_version}
    if os.name == "nt":
        command = ("$cpu = Get-CimInstance Win32_Processor; "
                   "$computer = Get-CimInstance Win32_ComputerSystem; "
                   "[pscustomobject]@{cpu_model=($cpu.Name -join ', '); "
                   "installed_ram_bytes=$computer.TotalPhysicalMemory} | ConvertTo-Json -Compress")
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", command],
                                    capture_output=True, text=True, timeout=20, check=True)
            info.update(json.loads(result.stdout))
        except (subprocess.SubprocessError, json.JSONDecodeError, OSError):
            info["cpu_model"] = "unknown"
    return info


def summarize(rows: list[dict], field: str) -> dict | None:
    values = [r[field] for r in rows if r.get("status") == "success"]
    if not values:
        return None
    return {"values": values, "minimum": min(values), "median": statistics.median(values),
            "maximum": max(values), "sample_stdev": statistics.stdev(values)
            if len(values) > 1 else None}


def run_suite() -> dict:
    cases = []
    for size, collision in [*((size, False) for size in SIZES), (300, True), (1000, True)]:
        expected = reference(size, collision)
        warmup = invoke_worker(size, collision, "timing")
        timings = [invoke_worker(size, collision, "timing") for _ in range(5)]
        memories = ([invoke_worker(size, collision, "memory") for _ in range(3)]
                    if expected["status"] == "success" else [])
        for row in [warmup, *timings, *memories]:
            if row.get("status") != expected["status"]:
                row["validation"] = "status_mismatch"
                continue
            keys = ("observations_sha256", "truth_sha256", "events", "people", "intended_roles")
            if expected["status"] == "success":
                keys += ("prediction_sha256",)
            row["validation"] = ("pass" if all(row.get(k) == expected[k] for k in keys)
                                 else "result_mismatch")
        successful = expected["status"] == "success"
        valid = all(r["validation"] == "pass" for r in [warmup, *timings, *memories])
        cases.append({"size": size, "collision": collision, "reference": expected,
                      "warmup": warmup, "timing_runs": timings, "memory_runs": memories,
                      "verified": valid,
                      "timing_seconds": summarize(timings, "seconds") if valid and successful else None,
                      "memory_peak_traced_mib": summarize(memories, "peak_traced_mib")
                      if valid and successful else None})
    import agrisight.synthetic_quality as quality

    sources = {"benchmark": Path(__file__), "detector": Path(quality.__file__),
               "protocol": Path("docs/experiments/M3_05_PROTOCOL.md"),
               "lock": Path("requirements/e1.lock")}
    return {"source": "SYNTHETIC DEMONSTRATION DATA", "version": "1.0",
            "pair_budget": PAIR_BUDGET, "environment": hardware(),
            "sha256": {key: hashlib.sha256(p.read_bytes()).hexdigest()
                       for key, p in sources.items()}, "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--size", type=int, default=1000)
    parser.add_argument("--collision", action="store_true")
    parser.add_argument("--mode", choices=("timing", "memory"), default="timing")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.size, args.collision, args.mode), allow_nan=False))
        return
    if args.output is None or not args.output.resolve().is_relative_to(
        Path.cwd().resolve()/"reports/private"
    ):
        raise ValueError("Output must be inside reports/private")
    result = run_suite()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print("Synthetic benchmark saved under ignored reports/private")
    if not all(case["verified"] for case in result["cases"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
