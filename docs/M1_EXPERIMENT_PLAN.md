# M1 — Real Agricultural Data: empirical experiment protocol
**Status:** planned, not executed. **Date:** 2026-10-28.

## Scientific question (E1)
**What is the observed structure, completeness, and internal consistency of the accessible NASS 2023 agricultural survey data, and which variables are appropriate for later decision-support analyses?**

This is an empirical **data profiling / data-quality baseline** experiment, not an impact evaluation or inferential model-comparison study.

## Primary source
Nigeria NBS National Agricultural Sample Survey 2023: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
Candidate secondary contextual source (not merged indiscriminately): Nigeria GHS Panel 2023–2024: https://microdata.nigerianstat.gov.ng/index.php/catalog/82

## Work sequence
1. **Source verification:** record catalog ID, actual file version, questionnaires, methods, data dictionary, sampling geography and legal access/redistribution conditions.
2. **Secure acquisition:** if terms permit, download authorised files only to ignored local data storage. Record SHA256 and download date. Do not place confidential/restricted raw records in repo or CI artifacts.
3. **Unit-of-analysis map:** identify respondent/household/plot/crop/enterprise grains, primary keys, multi-row joins, strata, PSU and weights. Never assume `n` rows equals `n` farmers.
4. **E1 baseline:** inspect dimensions, column types, distinct identifiers, missingness (including coded missing values), categorical distributions, range consistency, join cardinality and duplicate key candidates.
5. **Evaluation:** pre-specify validation rules from questionnaires/codebooks; distinguish genuine invalid values from legitimate skip logic, refusals, non-applicability and unknown responses. Cross-check at least three summary measures in independent code/SQL.
6. **Evidence report:** tables/figures with citations, source hashes, scripts/environment, quality findings and clearly scoped uncertainty. No geographic granularity unsupported by source design.

## Deliverables
- `docs/data_sources/NASS_2023_CARD.md` including licensed access and variables (created during inspection).
- `docs/experiments/E1_PROTOCOL.md` (finalized after codebook review).
- Notebooks/scripts for reproducible descriptive profiling with tests.
- `reports/E1_REAL_DATA_PROFILING.md` with verified findings and limits.
- A documented decision on suitable measures for subsequent BI work.

## Do not claim yet
No survey microdata, weights or released variable codebooks have been verified and downloaded for analysis in this project; no E1 results or figures exist.

## Supporting synthetic track
A separate generator may later inject known errors and create 55k **synthetic actor-role entries** for scalability/deduplication evaluation. Never treat these as real survey data, do not synthesize population findings from them, and never combine them with real-sample totals.
