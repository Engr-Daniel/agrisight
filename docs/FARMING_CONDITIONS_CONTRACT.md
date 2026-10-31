# FC1 farming conditions and crop destinations — contract v1.0

Specified 2026-10-31 before new analytical execution. Source is the previously
authorized, SHA256-frozen NASS archive. This increment answers four agreed
questions; it does not introduce population estimates or causal claims.

## Shared rules

Use unique released household IDs, household–plot keys, household–plot–crop
keys, household–harvested-crop keys and household–input keys at their respective
grains. Reject missing/duplicate keys and orphan parent references. No join of
harvest destinations to plots. Read only allow-listed fields. Reject changed
field/value labels. Numeric codes only; preserve ordinary/tagged missing values.
No identities or coordinates in outputs. Independent SQLite queries must agree
with Python counts, eligibility and exclusions before any artifact is written.

Unweighted descriptions of the observed release; no national estimates,
confidence intervals, trends or inference about current conditions. Household
main-season/year strings must match the existing checked baseline. Plot/crop
scope is the released main-season modules, April–October 2022. Destination
questions refer to harvested temporary crops: sales since harvest, storage at
interview, losses during/after harvest including transport/storage. Input module
is the questionnaire's agricultural rainy season; do not silently assert its
quantities have verified units merely because the released label says Kg.

## Land tenure, transport and travel

`3_Plot_mainSeason.dta`: s02_q04 tenure (released categories 1–6), s02_q05
transport (1–6), s02_q06 ordered travel bands (1–5). Preserve separate free-use
tenure categories; free use is not ownership. All roster plot types remain.
Tenure/transport shares divide by field-valid plot responses. Travel is eligible
only where transport is 1–5. On-dwelling code6 skips travel (questionnaire p13);
missing/invalid transport has unknown eligibility. Count missing/invalid eligible
travel separately; report travel entries outside the eligible subset as quality
exceptions without including them. No midpoint, average minutes or market-access
claim: the last band is open ended and travel is dwelling-to-plot.

## Harvest difficulties

`4_Crop_mainSeason.dta`: temporary type1 only; permanent type2 excluded.
Non-vegetable branch uses s01a_q07 (harvest any), s01a_q08__* (no-harvest reasons),
s01a_q11 (completed), s01a_q16 (unharvested area due to shocks), s01a_q17__*.
Vegetable counterparts are s01h_q08, s01h_q09__*, s01h_q16, s01h_q21, s01h_q22__*.
Questionnaire pp20–26 checked: branch assignment is not supplied as a reliable
explicit vegetable flag. Consequently describe branch-recorded responses only:
exactly one harvest-any branch present identifies the observed branch; neither
is unassigned, both is ambiguous and excluded. Publish both coverage counts.
Do not infer vegetable identity solely from names or count branch-absent fields
as ordinary missingness. Any-harvest yes/no uses valid1/2 branch responses.
No-harvest reasons apply only to branch harvest-any=no. Shock question applies
only to harvest-any=yes and completed=no; report skipped/outside-subset entries.
Shock reasons require that eligible shock answer=yes. Each 0/1 reason has its
own valid-response denominator with missing/invalid exclusions. Reasons overlap;
not-harvest-season and deferred harvest are not crop failure. No loss tonnage,
area lost, weather causation or combined vegetable/non-vegetable prevalence.

## Sales, storage and broad loss reports

`5_Harvest_mainSeason.dta`: s01b_harvestedCrops__id, s01b_q02 sales, s01b_q20
storage, s01b_q11 broad losses. Each1/2 field's denominator is valid responses
within this released harvested household–crop roster. Validate crop codes against
this module's released labels and temporary parent household–crop pairs.
Report roster scope separately from crop-plot difficulty records. Sales and
storage may overlap: a complete-response2×2 table uses only records valid for
both, with exclusions. Per-crop field summaries require at least30 valid
responses for display; omitted categories are not zero. No output share sold,
profitability, storage capacity or measured post-harvest-only loss rate.
Stage-specific quantity/reason branches are excluded because quantities may
alternatively be percentages and released labels have inconsistencies. The
broad, unambiguous loss indicator is the supported loss finding in this increment.

## Recorded inputs and quantity completeness

`9_Input_use_mainSeason.dta`: s03c_inputType__id1–21, s03c_q01 quantity.
Validate household parents. Per input type, classify quantity as positive finite,
zero, missing or invalid (negative/nonfinite); denominator is recorded rows of
that type, never all farmers. Preserve missing versus zero. Questionnaire p39
auto-populates inputs from crop responses and offers mixed units; the release
contains no corresponding quantity unit field. Show record coverage and quantity
status only, no totals, averages or comparisons of quantity magnitudes, adoption,
affordability or access rates. Absent rows do not establish non-use.

## Delivery and visuals

New private FC1 aggregate and separate reviewed manifest; preserve earlier
artifacts. Fail closed if absent/changed/inconsistent or fixture totals mismatch.
Project allow-listed aggregate fields only. Tenure composition, ordered travel
dot distribution, harvest/reason dot plots, paired sales/storage dots and overlap
matrix, and input completeness heatmap answer different questions. Exact tables,
denominators, exclusions and interpretations accompany charts. Figures appear
on hover, not permanent mark labels. No line chart implies a time series. No new
geography. Full licence/disclosure/release review remains M6-04, not completed
by adding aggregate local charts.

Acceptance: manually counted positive/negative/edge fixtures, independent
SQL/Python agreement on actual authorized data, deterministic installed-package
reproduction, optional-adapter tamper/missing behavior, regression/lint checks,
actual desktop/narrow browser checks, and documented results. Unsupported
extensions remain explicitly gated rather than labelled complete.
