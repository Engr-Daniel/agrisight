# M0-02 — Measurable acceptance and evaluation design
Status: proposal, not executed or owner approved.

> Historical acceptance proposal, partly exercised by the M0 fixtures; see [M0 review](M0_REVIEW.md) for actual dispositions. M0 remains complete as a foundation. Current empirical questions and E1/E2/E3 exit criteria are in the [charter](PROJECT_CHARTER.md) and [investigation plan](M1_EXPERIMENT_PLAN.md). The gates below do not imply that every proposed system control is implemented.

## Outcomes versus tests
| ID | Claim to test | Evidence and acceptance |
|---|---|---|
| A01 | Registration grain is consistent | Fixture with overlapping farmer/processor roles satisfies person counts and category counts independently |
| A02 | Source origins never silently mix | Provenance field + tests reject mixing survey sample and synthetic registry in population totals |
| A03 | KPIs are unambiguous | Each priority KPI has grain, numerator, denominator, exclusions, time definition, provenance and example fixture |
| A04 | Transformations reconcile | Curated SQL and independent Python/DuckDB checks equal expected fixture outputs exactly for integer counts; tolerances defined for floating estimates |
| A05 | Quality errors can be detected | Injected labelled missing/invalid/duplicate records; confusion matrix, false positives, precision/recall reported with confidence context |
| A06 | Dashboards expose limitations | Synthetic/public label, refresh timestamp, filters, denominators and missingness are accessible on each relevant view |
| A07 | Sensitive geography is protected | No precise actual household/farm point is committed or shown; small-cell suppression rules defined and tested before publication |
| A08 | Synthetic generation is reproducible | Same seed/config/schema generates identical aggregates and labelled injected defects |
| A09 | Performance is reproducible | 55k synthetic role entries benchmarked on recorded hardware with dataset size, repeat count, latency percentiles, query plan |
| A10 | Deployment and CI are reproducible | Clean checkout, environment creation, tests, lint and private demo verified with commands/logs |

**Important:** Thresholds for acceptable quality, performance and spatial suppression must be selected after examining baseline data and use cases. Setting arbitrary thresholds now would create a misleading claim of scientific rigor.

## Metric design convention
Every metric must specify: ID, business purpose, data family (survey vs synthetic), grain, date reference, filters, formula, status mapping, null/NA treatment, reconciliation query, intended display and disclosures.

## Evaluation split
- **Synthetic data:** known ground truth for engineering correctness and quality algorithm experiments, not evidence of real-world prevalence.
- **Public survey data:** statistically defensible analysis using the published sample design, variable documentation and survey weights, only after confirming proper handling.
- **Performance tests:** claim only observed results in controlled environment, not population coverage or field outcomes.

## Decision gate
M0 can close only when architecture/metric/source decisions are reviewed and evidence is logged in M0_REVIEW.md. This document does not authorize progression by itself.
