# M3-05 local workload benchmark findings

Observed 2026-10-29. **SYNTHETIC DEMONSTRATION DATA.** M3-05 complete for the specified local batch experiment. No live registration, survey population, service capacity or production-readiness claim.

## Scope and decision

Retain the simple local architecture. Bounded-key workloads up to100000 events completed in this experiment; this does not establish a universal capacity limit. Token collisions, not event count alone, govern pair growth. The benchmark wrapper rejects candidates above250000 before materialization. This is an experimental safeguard, not a validated production budget; direct calls to the M3-04 detector remain unguarded.

Timed work is full observation/truth validation plus normalized candidate counting, budget enforcement and B1 matching/quality detection. Generation, imports, hashing, fresh-process startup, independent SQL correctness checks, serialization and disk I/O are excluded. Results are not end-to-end pipeline latency. No ingestion service, operational SQL database or dashboard was benchmarked.

The [prospective protocol](../docs/experiments/M3_05_PROTOCOL.md) fixed sizes, seeds, mutation/block construction, repetition counts and methods before execution. Inputs repeat namespaced copies of the existing Mixed generator, truncating the final block to exact event count and shuffling observations. Cross-block keys cannot collide. This is controlled bounded-group scaling, not a realistic identity distribution or new accuracy holdout.

## Environment and conditions

Windows10 AMD64; Python3.11.9; SQLite3.45.1;4 logical processors; processor descriptor `Intel64 Family 6 Model 78 Stepping 3, GenuineIntel`. Full CPU marketing model and installed RAM were not established: the hardware metadata probe returned empty/null fields. Do not infer RAM from the machine name or model. Memory below is traced Python allocation, not a hardware-RAM measurement.

This was a shared development-machine run. Package build/installation and regression tests overlapped part of the benchmark; other background load was not controlled. Fixed ascending-size ordering can also introduce cache/thermal/load effects. Results are retained as observed, with no outlier deletion, retry or selection of a cleaner/faster series. They should not be used for isolated cross-machine or method performance comparisons.

Each case had one excluded warm-up and five sequential fresh-process timing repetitions. Successful cases also had three separate fresh-process tracemalloc runs. No timeout, unexpected worker exception, count/hash mismatch or SQL/Python disagreement occurred. The large collision case produced its expected budget rejection on warm-up and all five repetitions; it was not treated as a successful throughput result.

## Counts and measurements

Times are seconds. SD is sample standard deviation of five timing runs. Memory is median peak traced Python allocation in MiB, measured only after input generation/hashing; existing inputs, interpreter baseline and untraced/native allocations are excluded. Tracing elapsed times are never used for timing summaries. Counts are observations, not inferred from nominal percentages.

| Case | Events | Distinct people | Intended roles | Candidate pairs | Time median | Time min-max | Time SD | Traced peak median MiB |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| bounded groups | 1000 | 790 | 899 | 174 | 0.012149 | 0.009611-0.014687 | 0.001995 | 0.305819 |
| bounded groups | 10000 | 7191 | 8597 | 2331 | 0.183252 | 0.123142-0.279172 | 0.059215 | 2.924650 |
| bounded groups | 55000 | 39363 | 47181 | 12976 | 1.070623 | 0.956838-1.113672 | 0.061647 | 16.646795 |
| bounded groups | 100000 | 71521 | 85761 | 23637 | 2.018746 | 1.674232-2.568167 | 0.359622 | 31.802288 |
| collision | 300 | 300 | 300 | 44850 | 0.042601 | 0.034637-0.062766 | 0.011156 | 8.799498 |
| collision: rejected | 1000 | 1000 | 1000 | 499500 | - | - | - | - |

The55000-event workload contains39363 true people and47181 intended roles. The additional7819 events repeat existing intended roles. This is not the illustrative50000-farmer/5000-processor mix and not55000 distinct people or intended roles; the evaluated requirement is55000 submission-event entries.

The300-event collision case has300 distinct people but44850 matching candidate pairs, all false-positive same-person and duplicate-role pairs. Its cost reflects explicit pair materialization. The1000-event collision case would have499500 pairs, exceeding the fixed250000 budget; the wrapper rejects before calling the detector. No unguarded large-collision allocation or out-of-memory test was performed, and no rejected-case timing/memory result is fabricated.

## Every measured repetition

One timing list per successful case contains all five values, in execution order. The separate memory list contains all three peaks. Identical traced peaks reflect deterministic allocations here, not identical RSS or a guarantee of stable total RAM use.

| Events | Collision | Timing repetitions (seconds) | Memory peaks (MiB) |
|---:|---|---|---|
| 1000 | False | 0.014687300, 0.012148500, 0.009611500, 0.012626500, 0.010377100 | 0.305818558, 0.305818558, 0.305818558 |
| 10000 | False | 0.193989400, 0.123142100, 0.149639000, 0.183252000, 0.279172300 | 2.924650192, 2.924650192, 2.924650192 |
| 55000 | False | 1.082628900, 1.070622900, 1.018539200, 1.113672000, 0.956837600 | 16.646795273, 16.646795273, 16.646795273 |
| 100000 | False | 2.018746400, 1.674232300, 1.943625200, 2.396386400, 2.568167500 | 31.802288055, 31.802288055, 31.802288055 |
| 300 | True | 0.052506700, 0.040080100, 0.042601300, 0.062766300, 0.034637400 | 8.799497604, 8.799497604, 8.799497604 |
| 1000 | True | budget rejection in all5 | not run (expected rejection) |

Raw full-precision worker values, warm-ups, statuses, input/truth hashes and per-scenario/per-rule accuracy metrics remain under ignored `reports/private/m3_05_benchmark.json`. All30 timing-stage repetitions are retained (25 successful batches and5 expected rejections), plus6 warm-ups and15 separate successful memory runs. The parent timeout was120 seconds per worker; none timed out.

## Correctness and reproduction

Before measurements, each successful input passed the existing M3-04 Python/SQLite accuracy evaluator. Independent SQL counts also agreed on event/person/intended-role counts. Each warm-up/timed/memory worker regenerated the same canonical observation/truth hashes and identical prediction/quality hash as its reference. Six of six case records verified, including expected rejection. No large all-negative pair universe was enumerated.

An installed-wheel55000-event smoke run reproduced all input/truth/prediction hashes, counts and success status. Its elapsed time is intentionally not compared for exact equality. This is package smoke reproduction plus intra-suite repeats, not a second full benchmark on independent hardware. The wheel contains the new module and no restricted survey inputs. All123 tests passed in working and installed-wheel environments, including19 benchmark cases; Ruff passed. No new remote CI/Linux result is claimed.

Benchmark and detector source, protocol and lock hashes remained unchanged through the run and package checks:

- benchmark: `6ebf24da535b73ec341e0952ce1c6b6f8e5e681e824354f398be4db19ea22971`.
- detector: `19210828bf5b041fcc6b8fc4b2ec732d80a1e7e24305ef8b6f17e631f4cd9a78`.
- protocol: `cb6d4c0eff278a0a686d7aa8ffb6e385f2ede19f423e8e37ba1f336bf5237c23`.
- lock: `113aff71a432584d77b77c2272b72f413ef1ed3f7fb1c8931cead83bee0b148b`.

| Events | Collision | Observations SHA256 | Truth SHA256 | Predictions SHA256 |
|---:|---|---|---|---|
| 1000 | False | `5d40ebb0069d474ae218aaa10ddfca06390f88d51a57b22823340f4811912605` | `bc74c7e6bffa4d1a8c40e3dec246fc2bebed4656805c6a19845a342d0864924e` | `f5afaebe5c39b097b01dc48e85aaf00f0059bfd42be49fc6daaa96b420269948` |
| 10000 | False | `253b3af8333078bda97e0abb11e7c71c45e418b498e47484300bf86dca7c9e02` | `fddd8831a4f618ac0a87959c5012165870e0633fac2255a9200acb2b39fa62f6` | `dc9daff6ca0fda1d73c007e749926cb6e8a0bdbbd3a8fd3a1d55beb332432dcc` |
| 55000 | False | `530dd9035e4af73f134de7d57133330a0ad7ac1561b7c2b02063296b84737d92` | `07abd425bf69b05484522f3106eca944932225f3f8964b6a3b33e95154b96c5c` | `2a647340479943a4a720978e90f151743168e2ced41cdb9b4ead7c80d82c1054` |
| 100000 | False | `9cae77285dcfedd3271124a2e0ee9d0945b8aa364b7c07050809a24cc00934b9` | `c09216272cfffdd92f006f2f2421dbe5740190734bfd7fd7ceebccd46c08b00f` | `d71e619c1d31dd3873d9981280780bb7f53fa16625e844254e0691186f2738cc` |
| 300 | True | `ba3462cace89d2c38f827f33ad0a472b27fa80aca8d0f9383dd9a2c2c169caba` | `c4020b1eebc9d4abb4eae376e3138dd035afeac1e0021bb9ab5116f6f5473e62` | `7a01070a794a273356abebe90090f6c9e03e476d68ebf7aee4588b38e6f76c89` |
| 1000 | True | `195432b250849d8112cba41a0cd7c6e82ee886d30585bfc65092c1727aa238b7` | `eec94f3bdfc13b86a760753676a21fe73282b4f867d383323510a96b2108a34a` | not materialized |

## Reproduce and interpret

Use the unchanged dependency lock and run from the checkout root:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_workload_benchmark.py -q
.\.venv\Scripts\python.exe -m agrisight.workload_benchmark --output reports/private/m3_05_benchmark.json
```

See [development setup](../docs/DEVELOPMENT.md) for package installation and smoke checks. Measurements will vary with hardware/load; counts and hashes should reconcile under the observed locked environment. Keep different runs in separate files rather than overwriting evidence when investigating performance.

The local batch measurements support continuing with minimal tools for the next reporting increment, with limited accuracy and collision growth visible. They do not resolve M3-04's identity errors: a fast false match remains a false match. No correction, automatic merge, population inference, data publication or deployment follows from these results. [M3 review](../docs/M3_REVIEW.md) records the combined milestone scope and next handoff.
