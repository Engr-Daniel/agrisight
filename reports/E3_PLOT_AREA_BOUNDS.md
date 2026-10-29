# E3 — Missing-area bounds for the released main-season plot field

Observed 2026-10-29. NASS-02 contract/model v1.0. **Unweighted released-roster identification bounds, not population estimates or confidence intervals.** This completes the empirical area-bounds increment, not all M3 engineering work.

## Question and result

How much can the 48 missing values change the median of released `s02_q16a` over the fixed eligible main-season plot roster, allowing those unknown values to be nonnegative without imposing a maximum?

| Measure | Observed |
|---|---:|
| Eligible plot records | 273887 |
| Known area values | 273839 |
| Missing area values | 48 |
| Full-roster middle rank | 136944 |
| Known-only median | 6070.290058851242 |
| Full-roster lower bound | 6070.290058851242 |
| Full-roster upper bound | 6070.290058851242 |
| Bound width | 0 |

Values are in the field's released, labelled square-metre units; display median **6070.29**. These numerical digits reflect stored/computed values, not claimed physical measurement precision. The observed-only median is a different descriptive quantity from the target full-roster median; they happen to coincide in this dataset.

For N=273887 the middle rank is136944. Placing the 48 unknowns below known values makes the lower endpoint known-value rank136896; placing them above makes the upper endpoint known-value rank136944. Both ranks have the same stored value. Consequently every admissible nonnegative completion leaves this full-roster median at that value. No threshold was chosen to label the interval “robust,” and no unknown values were imputed into the source.

## Gate and interpretation limits

The acquired field and [official dictionary](https://microdata.worldbank.org/catalog/8194/data-dictionary/F16?file_name=3_Plot_mainSeason) label `s02_q16a` as plot area in square metres. Questionnaire PDF pp.15–16 covers cultivated/fallow/kitchen-garden plots and separates farmer estimates and GPS measurements; the released field's exact measurement/conversion lineage remains unverified. We explicitly chose the **released field** target under the [contract](../docs/NASS02_INDICATOR_CONTRACT.md), not certified GPS or true physical plot area.

All roster keys are complete/unique; all plot-status codes are documented1/2/3. Include all three plot types, not an outcome-selected subgroup. Known target areas are finite and positive; the contract would permit recorded0 and fail on negative/nonfinite or unsupported types. Missing values are treated as unknown under the full-roster completion model, not asserted to be missing at random or universally classified as interview errors.

The companion `areaAcresPlot` has no missing values but is0 on all48 missing-metre rows and209061 positive-metre rows. Its physical interpretation/rounding/derivation is unknown; this is **not** evidence justifying either blanket corruption claims or a backfill. The analysis does not convert from that field, substitute it, or set missing metre values to0. No hectare/acre estimate or conversion result is reported.

The zero-width interval addresses only the 48 unknown target-field values under the fixed roster/nonnegative support. It does not address error in known measurements, rounded/derived fields, omitted records, nonresponse, sample selection or population representativeness. It is not Nigeria's median farm size; it is not a household total. No weight, CI, significance test, geographic estimate or dry-season comparison is made. Future different sources or eligibility rules need new contracts.

## Method and checks

The [pre-specified E3 plan](../docs/experiments/E3_PROTOCOL.md) required a feasibility gate; [NASS-02 v1.0](../docs/NASS02_INDICATOR_CONTRACT.md) fixed eligibility, support, invalid-value handling, median convention and tolerances before quantile execution. Input is the frozen NASS ZIP with SHA256 `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02`, fixed member `3_Plot_mainSeason.dta`.

Python sorting and independent SQLite window ranks produce matching counts/ranks/status exactly and medians/endpoints within abs1e-9, rel1e-12. Validation/normalization are shared and separately tested, not claimed as independent source preprocessing. The [SQL model](../src/agrisight/sql/nass02.sql) retains NULL areas and enforces composite keys/nonnegative finite known areas. No raw records are saved, changed or exported.

Tests cover odd/even/no-missing/all-missing/empty/zero/unbounded cases, missing/duplicate keys, status/type/negative/nonfinite failures, tagged missing, row order, SQL constraints, large finite values, a full synthetic Stata-to-result run and exhaustive small completion fixtures. Source/output/label guards prevent silent changes. See MEMORY.md for actual verification and [development commands](../docs/DEVELOPMENT.md) for reproduction.

## Disposition

This is genuine same-target missing-outcome sensitivity, unlike changing the NASS-01 denominator's target group or manufacturing survey errors. It yields an informative invariance result for a limited question; do not overstate its reach.

M3's labelled synthetic duplicate/quality experiments and workload benchmarks remain open. Measurement/derivation clarification and population-design gates remain active. Nothing here authorizes public data release, reidentification, deployment or external report transmission. Source/access and publication obligations remain those in the NASS source card.
