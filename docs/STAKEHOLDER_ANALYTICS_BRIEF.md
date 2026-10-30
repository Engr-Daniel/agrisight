# Stakeholder analytics — Phase 1

Specified before new indicator execution, 2026-10-30. Scenario: programme managers need to understand the activities represented in surveyed agricultural households, assess information quality and decide where further investigation is warranted. This is a proposed decision context, not an invented client or validated intervention.

| Question | Decision supported | Evidence / destination |
|---|---|---|
| Which activities are reported? | Select activity profiles for follow-up questions | Four household indicators and activity selector / Agricultural Insights |
| How do crop and livestock responses overlap? | Avoid treating overlapping activity counts as separate households | Joint four-cell household table / Agricultural Insights |
| Which plot types are represented? | Understand what the area roster includes | Three category counts / Agricultural Insights |
| Where are recorded values absent or invalid? | Prioritize source verification without silently changing data | Activity validity and plot-area missingness / Data Quality |
| What should managers consider next? | Separate supported next steps from questions requiring more evidence | Traceable observations, actions and cautions / Recommendations |

## Indicator contract SA1 v1.0

Frozen archive SHA256 remains a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02. Household grain is unique complete hhid in 1_households.dta. Four binary fields: s00_q15a (main-season crops), s00_q16 (livestock/poultry), s00_q17 (fish farming), s00_q18 (fish capture). Codes1/2 are yes/no; ordinary/tagged missing and other numeric codes are separate exclusions. Report input, yes, no, missing, invalid, valid denominator and share. Zero valid denominator is null. Reject duplicate/missing keys, nonnumeric/boolean codes or missing/duplicated columns, never coerce or deduplicate.

Periods differ: crops use released mainAgSeason April–October2022; other three fields explicitly refer to referenceAgYear2022/2023. Verify these period values and field labels before execution. Their bars are recorded responses with differing recall windows, not a same-season ranking or trend. Minor-season crops remain excluded because their calendar conflict is unresolved.

Overlap uses only households with valid crop AND livestock responses; four mutually exclusive yes/yes, yes/no, no/yes, no/no cells sum to the pairwise-valid denominator. Excluded incomplete/invalid pairs are reported. It is cross-window co-reporting, not simultaneous activity, causal dependence or a relationship between crops and livestock counts calculated from marginals.

Plot grain is complete unique (hhid,s02_plotRoster__id) in 3_Plot_mainSeason.dta; reject orphan households. Verify released q15 labels before mapping codes1/2/3 to cultivated/fallow/kitchen-garden categories. Unknown/missing types abort rather than changing eligibility. Count all eligible plot types; shares divide by the complete roster. Area missingness uses s02_q16a; missing is unknown, zero is recorded, nonnumeric/negative/nonfinite aborts. Completeness is recorded areas / eligible plots; no accuracy certification or imputation. Existing NASS-02 bounds remain unchanged.

All findings are unweighted observed-sample descriptions. No population uncertainty, domain estimate, geographic comparison or dry-season comparison is approved. Recommendations concern follow-up, clarification and data suitability; they do not prescribe programme targeting, budget allocation or infer unmet need from participation.

Implementation must reconcile all integer activity, overlap, plot-type and area-completeness counts independently using Python and SQLite (shared ID/null staging is disclosed). Freeze aggregate/source/model/SQL/contract/lock hashes. Reporting validates the reviewed artifact and arithmetic each interaction; missing/incompatible evidence becomes unavailable, never a fallback. Fixtures are explicitly labelled TEST FIXTURE. Retain old experiments and explorer as repository tools, outside product navigation. Test manual golden counts, duplicates/orphans, missing/invalid responses, zero denominators, period/label changes, tampering and navigation; reproduce installed-wheel actual outputs before dashboard use.
