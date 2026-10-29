# M2 technical review — first sample analytical workflow

Date: 2026-10-29. **M2 complete for the M1-approved NASS-01 workflow.** This is not completion of all agricultural research, a population-estimation approval, a stakeholder signature or public-release authorization.

## Acceptance evidence

| M2 requirement | Observed evidence |
|---|---|
| Implement selected indicator with explicit population/eligibility/period/missingness | NASS-01 contract and E2 protocol; complete unique household keys required; source period verified; numerator 132859 / denominator 143105; missing/invalid/excluded all0 |
| Define applicable weighting and uncertainty | Explicitly unweighted pooled sample description; no CI/significance/national/domain claim. M1's population/design restriction remains binding; not falsely resolved by this increment |
| Independent numerical reconciliation | Versioned SQL staging/eligibility/mart and independent Python arithmetic; seven integer fields exact, proportion/percentage within absolute tolerance 1e-12; preprocessing dependency disclosed |
| Deliver agricultural finding and analytical model | E2 findings report interprets 92.84% within the released sample and explains why it cannot be generalized; SQL/model contracts and lineage documented |
| Use PostgreSQL/dbt only when justified | Not introduced: one source/fact/indicator needs no persistent service or managed model graph. Existing SQLite/Python stack suffices; future introduction gates retained |
| Test and reproduce | 15 new synthetic cases; 52 total tests passed in working and packaged reproduction environments. Ruff passed. Wheel includes SQL/model, excludes raw data. Full real-result JSON matches exactly across editable and installed-wheel runs |

## What the engineering adds

A calculation alone would give one percentage. This increment provides a fail-closed source/period/key contract, a versioned analytical model, explicit missing/invalid accounting, independent SQL/Python checks, tested edge cases, package-resource verification, pinned runtime reuse and reproducible provenance. These make the result reviewable; they do not make it a national statistic.

## Remaining research and release gates

- Obtain and validate survey-design/weight applicability before population inference; suitable producer information may exist but has not been established here.
- Resolve dry-season period conflict before temporal comparison; no change to raw labels.
- Review area/quantity missingness and eligibility before corresponding measures; no imputation performed.
- RQ2 service access remains deferred; RQ3 sensitivity follows E2 and requires its own pre-specified choices. A constant clean field may offer limited missingness sensitivity; do not inject synthetic errors into real records or invent instability to make E3 interesting.
- Other activity/geographic comparisons require separately approved contracts and reconciliation; NASS-01's pooled scope does not authorize them.
- No dashboards, deployment, raw redistribution or external publication/report transmission. Release still requires source/disclosure review and owner authorization, including source citation/report-copy obligations.

## Reproduction references

- [E2 protocol](experiments/E2_PROTOCOL.md), [indicator contract](NASS_INDICATOR_CONTRACT.md), [model description](NASS01_MODEL.md).
- [E2 findings](../reports/E2_AGRICULTURAL_FINDINGS.md), [SQL model](../src/agrisight/sql/nass01.sql), [Python implementation](../src/agrisight/nass01.py), [synthetic tests](../tests/test_nass01.py).
- [Pinned setup and commands](DEVELOPMENT.md), MEMORY.md observed log. Exact JSON/ignored data are local; restricted inputs are not required in CI. No GitHub/Linux CI result is claimed for this new commit.
