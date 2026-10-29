# E1.1 — Initial NASS household / plot quality findings

Observed: 2026-10-29. **Real survey files; unweighted sample-quality results only.** E1.1 and the E1.2 extension support M1's first-workflow suitability review, not a census, impact evaluation, complete audit of all modules or population estimate. No respondent records or geographical cells are included.

## Inputs and method

Owner-supplied `NASS_anonymized_dataset.zip`, SHA256 `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02`; see [inventory](../docs/data_sources/NASS_2023_INVENTORY.md) and [access/source card](../docs/data_sources/NASS_2023_CARD.md). Read only `1_households.dta` and `3_Plot_mainSeason.dta`; raw archive unchanged. File schema has 254 and 27 columns respectively. Selected IDs, infrastructure code and weight fields are numeric float64, as parsed by Pandas 2.3.3. No row samples exported.

The [pre-specified protocol](../docs/experiments/E1_PROTOCOL.md) defines missing/key rules, categories, denominators and exclusions. `python -m agrisight.e1_profile` checks the archive hash and selected schema, then computes counts independently in Pandas and in-memory SQLite. The SQL uses separate distinct-key and grouped duplicate queries, not sums across joined crop rows. All 14 integer measures agree exactly. Identifier/code normalization is shared; synthetic tests verify its semantics independently, so this reconciliation is not wholly independent of preprocessing.

## Observed counts

| Measure | Count |
|---|---:|
| Household rows | 143,105 |
| Distinct complete household keys | 143,105 |
| Household rows with missing key | 0 |
| Household duplicate excess among complete keys | 0 |
| Main-season plot rows | 273,887 |
| Distinct complete household–plot keys | 273,887 |
| Plot rows with any missing key component | 0 |
| Plot duplicate excess among complete keys | 0 |
| Plot rows with missing household ID | 0 |
| Plot rows whose present household ID is absent from household file | 0 |
| Plot infrastructure response: yes (1) | 11,268 |
| Plot infrastructure response: no (2) | 262,619 |
| Plot infrastructure response: missing, including tagged Stata missing | 0 |
| Plot infrastructure response: other code | 0 |

Duplicate excess is complete-key row count minus distinct complete keys; it is not the number of duplicated groups or matched people. Irrigation categories exhaust all 273,887 plot rows. Complete documented responses therefore number 273,887 / 273,887 loaded plot rows. This is response validity/completeness within the file; it does not establish that all eligible plots were captured or answers are accurate.

`final_weight` is present and positive finite for all 143,105 household rows and 273,887 plot rows; no missing, infinite or nonpositive values were observed in that field. This validates a simple numeric property, not weight correctness, calibration, applicability to a chosen estimand or an uncertainty method.

## Meaning and limits

The selected files support an initial structurally consistent household-to-plot relationship. Different plots belonging to the same household are legitimate repeated household IDs, not duplicates. No destructive corrections or exclusions were applied to inputs.

The infrastructure variable asks about presence, not actual irrigation use, agricultural-service access or a programme outcome. No household/plot population proportion is inferred from the yes/no counts. No CI is calculated. Geographic support, variance design, season/reference-period reconciliation, wider missing/skip logic and other modules remain open. No person-level uniqueness claim is made.

The owner reports an NBS download; authenticated transaction, exact upstream release and additional terms are not independently verified. The archive's metadata match does not prove byte identity with a mirrored release. This report is a local project artifact; no external publication or transmission to NBS has occurred. Archive conditions require citation and supplying resulting publications; keep those obligations on the release checklist.

## Reproduction

Use the pinned environment and commands in [development setup](../docs/DEVELOPMENT.md). Machine JSON stays under ignored `reports/private/`; review aggregate outputs before any release. No restricted files are needed for synthetic CI tests.

Observed Windows/Python 3.11.9 verification: 33 tests passed and Ruff passed in both the working and fresh `.venv-e1-repro` environments; `pip check` found no broken requirements in the fresh environment. Complete JSON, including schema, counts and weight checks, matched exactly. GitHub/Linux CI has not been observed for this change. No benchmark claim is made.

## E1.2 extension findings

Pre-specified [extension protocol](../docs/experiments/E1_EXTENSION_PROTOCOL.md) covers five household activities, irrigation skip logic, plot area, dry-season keys and main-season input quantities. All 21 released schemas were scanned for candidate design metadata; only these four modules were read at record level. No other-module quality certification is implied.

| Household activity response | Yes | No | Missing/other |
|---|---:|---:|---:|
| Main-season crops (`s00_q15a`) | 132,859 | 10,246 | 0 |
| Minor-season crops (`s00_q15b`) | 18,992 | 124,113 | 0 |
| Livestock/poultry (`s00_q16`) | 99,389 | 43,716 | 0 |
| Fish farming (`s00_q17`) | 3,747 | 139,358 | 0 |
| Fish capture (`s00_q18`) | 6,607 | 136,498 | 0 |

Each row's denominator is all 143105 household records; activities overlap and must not be added as unique households. No proportions or population totals inferred here.

- Dry-season plots: 26524 complete/unique composite keys, zero duplicate excess, missing keys or orphan household IDs. Infrastructure responses 8349 yes, 18175 no, zero missing/other. All 14 integer key/response counts agree with SQLite. This does not resolve their calendar reference.
- Main-season irrigation: among yes responses, no missing/unknown method or source codes; among no responses, no populated method/source fields. Thus the questionnaire skip is consistent for these fields. Skipped questions are not counted as quality failures. Method code 8 is recognized from released labels even though the questionnaire version differs in its listed methods.
- Plot area: **48 missing**, 273839 positive, zero nonfinite/negative/zero entries. Denominator is 273887 loaded main-season plot rows. This flags area-based eligibility review; no records excluded or imputed.
- Main-season inputs: **321103 rows**, all complete/unique household–input-type keys and no orphan household IDs. Quantity: **15409 missing**, 305694 positive, zero nonfinite/negative/zero. Denominator is input rows, not all households, crops or users. Missing quantity is not assumed zero or invalid reporting, and absent input rows are not assumed non-use. No quantity totals are computed.

The extension counts are tested descriptive diagnostics; only the explicitly reconciled key/response measures claim independent SQL agreement. Source skip interpretation and normalization still require human review, not an automatic “all data valid” label.

## Suitability disposition

The [design/period review](../docs/data_sources/NASS_DESIGN_AND_PERIOD_REVIEW.md) records a material conflict: released dry-season reference is November 2021–March 2022; report section 2.13 says November 2022–March 2023. Main-season field and report agree on April–October 2022. Do not compare seasons until clarified. No usable household/plot variance-design contract was established; `ea_name` in forestry must not be used to invent household PSUs or exposed in outputs.

Retain NASS for the narrowed first indicator [NASS-01](../docs/NASS_INDICATOR_CONTRACT.md): main-season crop participation **within the observed sample**, without population inference. Exclude area/yield, input-quantity and cross-season comparisons from this first workflow. GHS remains an alternative if service-access analysis is selected later; its source is not pooled with NASS.

These limitations are substantive E1 results, not missing values silently repaired to pass a quality gate. See [M1 technical review](../docs/M1_REVIEW.md) for per-gate evidence and carry-forward restrictions.
