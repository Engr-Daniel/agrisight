# NASS-02 v1.0 — Median released main-season plot-area field

Specified 2026-10-29 after the units/eligibility gate and **before median/bounds execution**. Implements the conditional study in [E3 protocol](experiments/E3_PROTOCOL.md). This contract targets a released field, not independently verified physical/GPS area.

## Gate decision and evidence

The [official plot dictionary](https://microdata.worldbank.org/catalog/8194/data-dictionary/F16?file_name=3_Plot_mainSeason) and acquired file label `s02_q16a` as square metres; `areaAcresPlot` is labelled acres. Local questionnaire PDF pp.15–16 lists cultivated, temporarily fallow and kitchen-garden/backyard plot types, then asks the area question without a plot-type exclusion. It separates farmer estimation/units and GPS measurement, but released transformation/measurement lineage is not established.

Gate inspection on the frozen archive: 273887 complete/unique plot keys; no unknown/missing plot-status codes. The metre field has48 missing entries. The acre companion has no missing values but is zero on all48 and on209061 rows with positive metre fields. This does not by itself prove corruption (rounding/derivation is unknown), but prevents treating the companion as an interchangeable recovery source. No unit conversion or backfill is performed. Keep the measurement method as **unverified** and state results in released, labelled square-metre units only. Do not call them certified GPS areas or total farm size.

## Fixed target and eligibility

| Property | Contract |
|---|---|
| Source | Acquired NASS archive fixed by SHA256 in inventory; `3_Plot_mainSeason.dta` |
| Grain/key | One main-season plot; complete unique (`hhid`, `s02_plotRoster__id`) required |
| Eligible roster | All released rows with `s02_q15` in1,2,3, including fallow and kitchen gardens; unexpected/missing status aborts rather than changing sample |
| Outcome | Released `s02_q16a`, labelled square metres; not sum of plots per household |
| Known values | Numeric finite nonnegative areas; zero is a valid recorded value, not a generic null |
| Unknown values | Ordinary/tagged Stata missing; no documented structural exclusion for these records is established, so treat as unknown under the full-roster target |
| Invalid values | Negative/nonfinite/nonnumeric values abort the calculation; no clipping, deletion or reclassification to missing |
| Target | Median over the same full eligible roster, allowing each unknown area any nonnegative finite value |
| Reference | Median of known areas only, explicitly conditional on recorded areas and not assumed to equal the full-roster median |
| Median convention | Odd: middle order statistic; even: arithmetic mean of two middle order statistics |
| Bounds | Sharp lower bound from unknowns at0; upper endpoint from unknowns above all known areas; upper supremum may be unbounded, no maximum imposed |
| Empty roster | Median/bounds undefined; do not return0 |
| All areas missing | For a nonempty roster, lower0 and upper unbounded; known-only median undefined |
| Weight/design | Unweighted released-sample analysis; bounds are not sampling CIs or population bounds |
| Period/scope | Main season April–October2022, pooled released roster only; no geography/season comparisons |
| Reconciliation | Exact counts/ranks/status; numeric endpoints/median at abs tolerance1e-9 and relative tolerance1e-12 |

## Method and acceptance

Let N be total eligible plots, m unknowns, n=N-m known sorted values. For each full-roster middle rank r, lower endpoint is known rank r-m if r>m, otherwise0. Upper endpoint is known rank r if r<=n, otherwise unbounded. For even N average each pair of endpoints. Derive the known-only median using n's own middle ranks. No synthetic area value is written into the real observations.

Compute independently with Python sorting and SQLite window-ranked known areas; compare all outputs. Test odd/even, no missing, all missing, zero, unbounded endpoints, empty input, invalid/status/key failures and order invariance before executing real quantiles. Use the existing pinned environment and packaged SQL resource; no new infrastructure/dependency.

Output counts, missing count, middle ranks, known-only median, full-roster bounds, numerical width, bounded/unbounded/undefined status, source/contract/model provenance and scope. Machine JSON remains ignored under `reports/private/`; manually review report aggregates before any release. No rows, identifiers, coordinates, extremes or per-geography cells exported.

The completion criterion is reconciled missing-outcome sensitivity for this field, **not** a chosen “robust” threshold. Tight/zero width would address only these missing entries, not measurement error, derivation ambiguity, nonresponse, sample selection or population uncertainty. Area/yield/household-total measures outside this contract remain gated.
