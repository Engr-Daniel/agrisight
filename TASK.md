# TASK.md — AgriSight roadmap

Updated: 2026-10-28. Checkboxes record observed evidence, not planned outputs.

## M0 — Engineering research foundation (COMPLETE)

- [x] Stakeholder decision hypotheses, architecture options and provenance/privacy rules.
- [x] Seven synthetic-registration KPI contracts and independent Python/SQL fixture tests.
- [x] Seven-case Pandera/GX comparison; historical CI: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776119
- [x] Pandera-first working decision for initial Python validation.

M0 is a design baseline, not empirical findings, completed user validation or production readiness. Preserve the [historical review](docs/M0_REVIEW.md); no need to reopen M0.

## Review alignment — targeted correction

- [x] Align current purpose, roadmap and architecture with empirical intelligence plus trustworthy delivery; record [rationale/trade-offs](docs/REVIEW_ALIGNMENT.md).
- [x] Record provisional RQ1–RQ3, E1/E2/E3 outputs and [source selection matrix](docs/RESEARCH_FEASIBILITY.md); GHS remains an alternative.
- [x] Verify raw-data Git protection and foundation environment checks; Python 3.11.9, 19 tests passed and Ruff passed locally. Commands and limitations in MEMORY.md.
- [ ] Select and lock actual M1 analytical dependencies after file/method requirements are known; reproduce a clean install. No wholesale stack change or new CI infrastructure.

## M1 — Source feasibility, acquisition and E1 (IN PROGRESS)

- [ ] M1-01: inspect NASS questionnaires, codebooks and design documentation against candidate questions; assess GHS where it offers a better fit.
  Progress: relevant questionnaire sections and mirrored household/plot/input dictionaries inspected; [source card](docs/data_sources/NASS_2023_CARD.md) records initial findings and provenance. Full access, design and variable audit remain open.
- [ ] M1-02: populate exact-variable/file feasibility evidence; record access/redistribution terms, study version and decision rationale. Mark each question supported, needs narrowing, deferred or unsupported. Select one source and first feasible indicator.
- [ ] M1-03: acquire only permitted microdata in ignored local storage; record hashes, filenames, release and download date. Never commit restricted inputs.
- [ ] M1-04: confirm units/keys, join cardinality, strata/PSU/weights or other variance-design requirements, geography, reference periods and coded missingness. Finalize the indicator contract/protocol.
- [ ] M1-05: execute E1 profiling on actual authorized records: schema, rows, missingness, duplicate-key candidates and rule findings. Cross-check at least three summaries independently.
- [ ] M1-06: review exclusions and unusual values against documentation; distinguish sample descriptions from population estimates. Do not silently delete outliers or treat skipped questions as defects.
- [ ] M1-07: deliver tested scripts, observed environment/commands, suitability report and limitations; close M1 only with evidence.

**Exit:** supported source/question mapping, verified permissions and provenance, analytical definitions, reproducible profiling and reviewed findings. See [E1–E3 plan](docs/M1_EXPERIMENT_PLAN.md).

## M2 — E2 agricultural findings and analytics engineering (PLANNED)

- [ ] Compute selected RQ1/RQ2 indicators with documented population, eligibility, denominator, period, missingness, applicable weights and verified uncertainty methods.
- [ ] Independently reconcile results using SQL/Python, with tolerances for estimates; report supported geographic scope and sample counts.
- [ ] Deliver reproducible agricultural findings. Introduce PostgreSQL/dbt only when persistence/model complexity justifies them, with contracts and tests.

## M3 — E3 robustness and separate engineering studies (PLANNED)

- [ ] Pre-specify and evaluate reasonable missingness, eligibility and definition alternatives for RQ3; report stability and limitations without causal claims.
- [ ] Separately implement labelled synthetic ground truth for defect/duplicate precision, recall and false positives.
- [ ] Benchmark documented workload sizes, including 55k role entries, with hardware/repeats and observed results. Never present simulated counts as agricultural findings.

## M4 — Evidence-backed reporting (PLANNED)

- [ ] Choose Power BI or Streamlit initially; build interactive reporting from checked findings. Add the second only for a distinct purpose.
- [ ] Reconcile filters/denominators, expose provenance and uncertainty, and test licensed geography/disclosure safeguards before maps or drill-down.

## M5 — Advanced analytics (OPTIONAL)

- [ ] Evaluate advanced statistics or evidence-grounded AI only for a justified need with baseline comparisons and appropriate tests.

## M6 — Publication and reproducibility (PLANNED)

- [ ] Independent clean reproduction, existing CI checks, measured performance and learning documentation.
- [ ] Licence/privacy/disclosure review and explicit owner authorization before public release or deployment.

**Immediate next:** verify authenticated NBS terms/file inventory and reconcile release/design documentation. Plot irrigation-infrastructure response quality is the proposed E1 starting target, not a completed result or finalized population indicator. No need for another architecture redesign.
