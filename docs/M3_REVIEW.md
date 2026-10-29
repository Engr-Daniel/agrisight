# M3 technical review

Observed 2026-10-29. **M3 complete within its specified empirical and synthetic experiment scope.** This is an internal technical review, not stakeholder acceptance, external replication or production certification.

| Component | Evidence | Limit |
|---|---|---|
| NASS-01 readiness | No response exclusions in frozen sample; limited invariance audit | Not broad sensitivity or inference |
| NASS-02 missing-area bounds | Same full-roster median endpoints6070.290058851242 in released labelled units | Measurement-lineage and population-design questions unresolved |
| Synthetic accuracy | Fixed baselines, hidden truth, manual fixtures, independent SQL counts and reserved seeds | B1 mixed duplicate recall50%; precision87.72-90.91%; no automatic identity resolution |
| Workload benchmark | Four event sizes including55000, five timing repeats, three separate traced-memory repeats, SQL accuracy checks and package smoke | Shared machine; bounded-group synthetic workloads; partial Python allocation, not RSS; no SLA |
| Collision failure mode |300-event candidate explosion observed;1000-event case rejected before499500 pairs materialize | Budget is an experimental wrapper policy; direct detector has no guard |

Evidence: [empirical review](M3_EMPIRICAL_REVIEW.md), [synthetic findings](../reports/M3_SYNTHETIC_QUALITY.md), [benchmark protocol](experiments/M3_05_PROTOCOL.md), [benchmark findings](../reports/M3_WORKLOAD_BENCHMARK.md), [benchmark source](../src/agrisight/workload_benchmark.py), [tests](../tests/test_workload_benchmark.py). MEMORY.md records actual commands and validation.

## Design decision and handoff

Keep the present Python/SQLite architecture. No benchmark evidence requires distributed execution, another service or an operational database. Correctness limits remain visible independently of speed: do not automatically merge matches, count cross-role identities as duplicate roles or treat synthetic truth as field enrollment.

Proceed next to M4 by selecting one initial reporting tool and fixing its reporting contract before implementation. Consider Streamlit for reuse of the current Python work or Power BI for a specific stakeholder/learning requirement; record that choice and pin any newly required dependencies. Use only checked aggregate findings, explicit denominators/provenance and clearly separate survey/synthetic views. Map and drill-down work remains gated by supported geography, permissions and disclosure checks. No automatic deployment is authorized.

The remaining scientific caveats do not disappear at milestone closure: physical area derivation, survey variance design, dry-season calendar conflict and service/quantity concepts remain unresolved. Avoid further narrow indicators solely to increase output count. M6 independent clean reproduction and owner-authorized publication are distinct future work; reuse of an existing reproduction environment and a packaged smoke run do not complete M6.
