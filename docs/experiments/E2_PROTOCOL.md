# E2.1 — NASS-01 sample analytical workflow

Specified 2026-10-29 before indicator execution. Acceptance is the first M2 workflow agreed at M1 completion, not national inference or all candidate research questions.

## Question and pre-specified contract

What proportion of the released agricultural-household sample reports growing crops in the main season, among valid yes/no responses? Follow [NASS-01 v1.0](../NASS_INDICATOR_CONTRACT.md): one household per complete unique `hhid`, `s00_q15a` codes 1=yes/2=no, April–October 2022. Missing/other numeric codes are excluded from the valid-response denominator and reported separately. Missing/duplicate identifiers fail the run; they are not dropped. Zero eligible responses yield undefined/null, never 0%.

## Model and reconciliation

Use the frozen archive SHA256 and only `1_households.dta`. Verify the released period fields against the contract; fail on an unexpected period instead of silently relabelling. Keep raw source immutable and select only key, activity and reference fields. Never read unrelated household free text or publish identifiers.

Implement a versioned SQL model with constrained household staging, an eligibility view and a one-row indicator mart. Keep SQLite in memory. Compute the same counts/proportion independently in Python directly from original selected responses, not from SQL's categories. Canonical identifier/missing representation is shared and tested; disclose this preprocessing dependency. Require exact integer agreement and absolute tolerance 1e-12 for proportion/percentage. Do not round before reconciliation; round only display values.

JSON output must include versioned definition, source hash/member, source period, grain, numerator/denominator, missing/invalid/excluded counts, weight status, geographic scope, inference limitations, dependency/model provenance and reconciliation outcome. Output stays in ignored `reports/private/`; only reviewed aggregates enter the tracked findings report. No row-level model persisted.

## Verification and completion

Use known-truth synthetic cases for valid/missing/other responses, empty/all-ineligible denominator, missing/duplicate IDs, wrong response types, key constraints, row-order invariance, source/period/output guards and complete Stata-to-result execution. Run targeted and full tests/lint, then reproduce real JSON exactly in the existing clean pinned environment. Real source files never enter CI.

Completion requires observed indicator results, explicit denominator/exclusions/interpretation, independently checked analytical models, tested commands and technical review. Existing dependency lock suffices; no new package, CI workflow, database service or dashboard is justified for one source and one indicator.

## Boundaries

No weights are applied; no CI, significance, national/domain prevalence, causal inference or cross-season comparison. RQ2 service access and RQ3 sensitivity remain deferred to their gates. A “no” response is not evidence of no agricultural activity. This first result does not complete the project's broader agricultural research goals.
