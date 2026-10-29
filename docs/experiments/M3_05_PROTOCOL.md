# M3-05 workload benchmark protocol v1.0

Specified 2026-10-29 before benchmark implementation/execution. **SYNTHETIC DEMONSTRATION DATA.** This evaluates a local batch, not a live registry, service SLA or population finding.

## Fixed work and inputs

Benchmark validation plus normalized B1 matching/quality detection from M3-04, including a new preflight candidate-budget check. Include full observation/truth validation, normalized key group counting, pair-budget rejection and `detect(..., 'B1')`. Exclude generation, hashing, imports, process startup, independent accuracy evaluation, JSON serialization and disk I/O. Report this scope beside all timings; it is not end-to-end ingestion/SQL/dashboard latency.

Use exact submission-event sizes1000,10000,55000,100000. Build each from deterministic copies of `generate(707, 'Mixed')` (1400 events), with block namespaces applied to all event/truth IDs and both observable tokens. Preserve token case/whitespace and nulls. Token namespaces prevent unintended cross-block collisions. Sort base events by submission ID; truncate only the final block to reach N, retaining exactly corresponding truth. Shuffle final observations with seed808. This is a deliberately bounded-group scaling workload, not a realistic joint distribution or a new accuracy holdout. People/intended-role counts must be observed, not equated to event counts; clipped blocks can change ratios.

Two diagnostic workloads:300 events with identical synthetic tokens, distinct people/intended farmer roles (44850 false-positive candidate pairs), and1000 such events (499500 candidates), which must be rejected by a250000 same-person candidate-pair budget. Count normalized groups before materializing pairs. This guard prevents the deliberately excessive workload in this benchmark; the underlying M3-04 detector is unchanged and remains unguarded when called directly. The budget is an experimental resource policy, not an empirically established safe production limit.

## Measurements

Use standard-library subprocess workers, one fresh process per repetition. For each workload run one excluded warm-up, then five measured repetitions in fixed ascending-size order, with collision diagnostics last. Same seed/input every repetition. Fresh processes isolate Python state, but filesystem/CPU caches are not cleared, and fixed ordering can introduce thermal/load effects. No tuning after seeing times; unsuccessful repetitions remain failures.

Timing workers use `time.perf_counter` immediately around the fixed work with normal garbage collection. Separate memory workers (three fresh repetitions per successful workload, no timing interpretation) start `tracemalloc` only after generation and hashing. Report peak traced Python allocation in MiB, excluding existing input allocations, interpreter baseline and untraced native/SQLite memory. This is not process RSS or total RAM; do not claim otherwise. Profiling changes performance, so never use its elapsed times in timing summaries. No third-party profiler/dependency is required.

Parent timeout120 seconds per worker; retain timeout, exception, candidate-budget rejection and output/accuracy mismatch as explicit statuses, not slow successes. Do not silently retry or drop an outlier. If a workload cannot complete, report its failure and remaining supported sizes. Record hardware CPU/model, logical processors, installed RAM, OS, Python/SQLite versions and module/protocol/lock hashes without user names, machine hostname, network IDs or full home paths. Hardware probes may return unknown; never invent values.

## Correctness and reporting

Before measurements, independently evaluate B1 against truth using the existing Python/SQLite M3-04 evaluator on each successful workload. Reconcile event/person/role counts in SQL, record canonical input/truth hashes and metrics, then require identical prediction/quality hashes from every warm-up, timed and memory run. The large collision workload is expected to reject before pair materialization; verify its combinatorial candidate count and rejection, not a fabricated accuracy result. Keep worker-level raw measurements/statuses under ignored reports/private, plus reviewed aggregate report in Git.

Summarize all five successful times (minimum, median, maximum and sample standard deviation); report individual values. Memory summary gives three peaks and their median/range. No confidence interval, throughput SLA, real-world identity accuracy or universal maximum capacity follows. Complete M3-05 only after tests, actual worker runs, correctness reconciliation, repeat evidence and packaged smoke reproduction; hardware-dependent times need not reproduce bit-for-bit. Preserve all original M3-04 contracts/results. Full M3 completion is scoped to these empirical and synthetic experiments, not production readiness or public-release permission.
