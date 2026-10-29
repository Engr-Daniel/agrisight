# E1.1 — Household / main-season plot suitability

Specified: 2026-10-29, before record-level results. Scope is deliberately narrower than full M1.

## Input and provenance

Use the immutable owner-supplied archive recorded in [inventory](../data_sources/NASS_2023_INVENTORY.md). Verify SHA256 against that record before reading. Read only `1_households.dta` and `3_Plot_mainSeason.dta` from the ZIP; no unrestricted extraction, row export or raw-value logging. Select documented fields explicitly; missing required columns fail rather than silently substituting.

## Units, rules and denominators

- Household candidate key: `hhid`. Plot candidate key: (`hhid`, `s02_plotRoster__id`). Test blank/null components and uniqueness separately. These are observations, not registration roles or distinct persons.
- Record row totals, complete distinct keys, duplicate excess among complete keys, and rows missing any key component. Exclude missing components from distinct/duplicate denominators; retain them in total rows. Never delete or merge records.
- Irrigation infrastructure field: `s02_q07`, questionnaire section 2 question 7, codes 1=yes and 2=no. Classify each plot into yes/no/missing/other; preserve Stata tagged missing values as missing, not no. Categories must exhaust plot rows.
- Quality completeness denominator is all loaded plot rows; valid response numerator is yes + no. Do not interpret the resulting proportion as population prevalence or infrastructure use/access.
- Check plot-to-household coverage using complete household IDs. Null/blank IDs are counted separately, not silently considered matches. An orphan is a plot with a present household ID absent from household records.
- Check `final_weight` for missing, nonfinite and nonpositive entries; these counts are descriptive, not evidence of correct sampling-weight applicability. No weighting, population estimate, map, CI or causal claim in E1.1.
- Schema/label inspection is restricted to required fields. Individual IDs, raw rows, coordinates, rare geographic cells and arbitrary free text are excluded from output.

## Independent reconciliation

Pandas aggregations are independently checked against in-memory SQLite for row totals, complete distinct household/plot keys, complete-key duplicate excess, irrigation categories and orphan plots. Normalize blank/null IDs consistently; preserve identifier types, and reject unexpected mixed/nonnumeric code types rather than fabricating a mapping. Exact integer equality is required; mismatch aborts report creation. SQLite tables remain ephemeral and are not saved.

## Acceptance and reporting

Positive, negative and empty-input tests cover overlapping households/plots, duplicate keys, missing IDs, invalid responses, tagged missing, orphan records and unsafe output paths. Run targeted tests plus foundation regression/lint. Reinstall the increment's pinned dependencies in a second fresh Python 3.11 environment and reproduce summary results.

All machine outputs go under ignored `reports/private/`. Only manually reviewed aggregate counts, provenance, methods and limitations may enter tracked reports; no automatic publication. Retain remaining M1 gates for access/release clarification, survey design, reference periods, source-specific missing codes, wider modules and owner review. An E1.1 pass does not close M1 or approve E2.

## Tool choice

Pandas 2.3.3 reads Stata 115 directly and preserves numeric codes when categorical conversion is disabled. Installed reader signatures and real-file execution verify the selected API; the [official Stata options documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_stata.html) explains categorical/missing handling. SQLite is standard-library independent SQL; no persistent database is required. Pandera remains the future source-schema option but adds no need for this bounded rule set; no additional framework or CI workflow is introduced. Lock this increment's runtime, test and build dependencies, not the future stack.
