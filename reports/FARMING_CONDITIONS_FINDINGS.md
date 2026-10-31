# FC1: farming conditions, harvest difficulties, destinations and input records

Actual authorized NASS 2023 release; unweighted sample descriptions. The first
FC1 run reconciled every published category and eligibility count independently
in Python and SQLite. These results describe historical released records, not
national estimates, unique farmers, current conditions or programme impacts.

## Land arrangements and travel

All273887 main-season plot records have valid tenure/transport responses.
Ownership by a household member is recorded for228823 (83.55%); rented25378
(9.27%); other682; free family land10472; free community land6027; other free-use
land2505. Free-use categories are not counted as household ownership or legal
title. This composition can guide follow-up about differing arrangements, not
establish tenure security.

Travel time excludes5835 on-dwelling plots as expected skips. All268052 eligible
off-dwelling plots have valid travel responses: less than30 minutes121826
(45.45%);30 minutes–1 hour84211 (31.42%);1–2 hours45997 (17.16%);2–3 hours12490
(4.66%); more than3 hours3528 (1.32%). No travel entries were found outside this
eligible subset. These bands describe dwelling-to-plot journeys; the last is open
ended, so no average minutes or travel-to-market conclusion is reported.

## Harvest difficulties and loss reporting

The480393 crop-plot records include380464 temporary and99929 excluded permanent
records. All temporary records have exactly one observed harvest-response branch;
zero are unassigned or ambiguous. This is checked response coverage, not a new
vegetable classification inferred from crop names.

| Recorded branch | Harvest-any denominator | No harvest | No-harvest share |
|---|---:|---:|---:|
| Non-vegetable |335870|15300|4.56%|
| Vegetable |44594|1445|3.24%|

Among15300 non-vegetable no-harvest records,6014 select too much rain/flood,
4298 not harvest season,1316 too little rain/drought and1172 deferred harvest.
Among1445 vegetable no-harvest records,452 select too much rain/flood,260 not
harvest season and205 pest/disease. Every reason has its own valid0/1-response
denominator; all no-harvest reason fields are complete in these subsets. Reasons
can overlap. Timing responses mean no harvest must not be relabelled crop failure;
reported weather reasons are not causal attribution.

Shock questions apply only where some harvest was reported but harvest was not
complete. Non-vegetable:6537 eligible,5663 valid,874 missing;1651 yes (29.15% of
valid responses). Vegetable:1568 eligible,1328 valid,240 missing;272 yes (20.48%).
There are no shock answers outside the defined eligible branch subsets. These
missing responses remain visible rather than silently counting as no. Shock
reasons use only eligible shock-yes records, not all crop records.

The separate harvested household–crop destination roster has334133 records;
38447 (11.51%) report any losses during/after harvest, including post-harvest
activities, transport and storage. This is not the percentage of output lost or
a post-harvest-only loss rate. Stage-specific quantities/causes remain excluded
because the questionnaire permits quantity/percentage alternatives and released
stage labels contain inconsistencies. No loss tonnage or area damaged is inferred.

## Sales and retained storage

Sales, storage and broad-loss questions each have334133 valid destination rows,
with zero missing or invalid responses. Sales since harvest are reported in207427
(62.08%); unprocessed crop in storage at interview in129184 (38.66%). Counts are
household–crop records; a household can appear for multiple crops.

| Sales reported | Storage reported | Records |
|---|---|---:|
| Yes | Yes |81820|
| Yes | No |125607|
| No | Yes |47364|
| No | No |79342|

All334133 have valid paired responses; none are excluded from this overlap.
Sales and storage coexist in81820 records; the two percentages must not be treated
as exclusive destinations or output allocations. Crop detail displays42 categories
with at least30 valid responses per field, omitting1 smaller category. The default
comparison uses the10 crops with the most destination records, not highest rates.
These findings can inform crop-specific marketing/storage questions, but do not
measure profitability, market access or adequate storage capacity.

## Recorded inputs and information gaps

The321103 household–input records span21 input types:305694 positive finite
quantities,0 zero,15409 missing (4.80%),0 invalid negative/nonfinite values.
Solid manure accounts for13316 missing quantities out of68325 recorded rows
(19.49% of that input's rows). This is the largest missing count, not necessarily
the largest missing percentage. Vegetable material/compost has799 missing out
of7069 records. Urea has198 missing of62570 and NPK210 of59634.

This identifies a measurement follow-up, not low input use or an access gap.
The questionnaire auto-populates input types and permits mixed quantity units;
the release has no matching unit field. No quantity sums, averages, comparisons
between types or input-adoption percentages are presented. Absent rows do not
prove non-use; missing quantity does not mean zero.

## Visual and interpretation choices

Tenure uses a ring to show mutually exclusive composition. Travel uses ordered
dots, preserving band order without inventing midpoint minutes. Harvest reason
dots compare overlapping responses without implying a composition. Sales/storage
uses paired dots and a separate2×2 overlap heatmap. Input completeness uses a
matrix with a common0–100% within-type scale, making missing/zero/invalid states
explicit. Values appear in hover tooltips, with exact tables and accessible
denominators alongside. No line chart invents a trend and no new map implies
geographic prevalence.

See [contract](../docs/FARMING_CONDITIONS_CONTRACT.md) and delivery evidence in
[review](../docs/FARMING_CONDITIONS_REVIEW.md). Raw data and aggregate JSON remain
ignored. Existing source permission and M6-04 publication/disclosure gates remain.
