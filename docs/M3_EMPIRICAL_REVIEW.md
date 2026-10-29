# M3 empirical component review — NASS-02

Date: 2026-10-29. **Empirical E3 component complete under the released-field contract; full M3 remains in progress.** Synthetic quality/matching and scale tasks are unexecuted.

## Acceptance and scope

| Gate | Evidence/disposition |
|---|---|
| NASS-01 readiness | Limited exclusion-invariance audit recorded; not passed off as a substantive missing-data experiment |
| Area feasibility | File labels/dictionary/plot-type eligibility inspected; target label square metres confirmed; measurement lineage not certified. Companion zeros prohibit casual recovery. Proceed only with released-field claims, as permitted by E3's gate |
| Pre-specification | NASS-02 contract fixed all roster types1/2/3, nonnegative support, invalid/key failures, median convention and reconciliation before real quantile calculation |
| Same-target sensitivity | Unknown nonnegative completions bound the same full-roster median; known-only reference clearly distinct. No arbitrary cap, missing-at-random assumption, imputation, deletion or data corruption |
| Independent checks | Python sorting and SQL window ranks reconcile; manual known-truth and exhaustive small synthetic completions test the mathematics |
| Observed result | Full-roster median bounded at6070.290058851242 in released labelled m²; width0 due ties across bounding ranks; no broad measurement or population robustness claim |
| Reproducibility/privacy | Frozen raw archive, pinned dependency reuse, packaged SQL/model, private JSON and manually reviewed aggregates; verification commands/results in MEMORY.md |

## Decisions and remaining work

Keep full M3 open for M3-04 labelled synthetic quality/matching evaluation and M3-05 workload benchmarks. Design those experiments independently of the survey; no injected errors enter NASS. Benchmark results must be actually observed with input sizes, seed/config, hardware, repeat conditions and failure modes.

The meter/acres discrepancy is an outstanding measurement-lineage question, not repaired by a zero-width bound. Source-producer clarification or transformation documentation would be needed to claim more. Missing source design still gates population inference. Do not silently expand to yields, household farm-size totals, geographic prevalence or season comparisons.

Evidence: [contract](NASS02_INDICATOR_CONTRACT.md), [E3 plan](experiments/E3_PROTOCOL.md), [findings](../reports/E3_PLOT_AREA_BOUNDS.md), [runner](../src/agrisight/nass02.py), [SQL](../src/agrisight/sql/nass02.sql), [synthetic tests](../tests/test_nass02.py). This technical review is not stakeholder signature or public-release authorization.
