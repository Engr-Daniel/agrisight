# NASS analytical input contract v1.0

Date: 2026-10-29. Applies to the owner-supplied ZIP fixed by SHA256 in [inventory](NASS_2023_INVENTORY.md), not arbitrary future NASS releases. Source fields retain their original names. Household and role/person registry concepts are not interchangeable.

| File / grain | Stable candidate key (verified on acquired file) | Selected fields / semantics |
|---|---|---|
| `1_households.dta`: released agricultural-household observation | `hhid` | `s00_q15a/b`, `s00_q16/17/18`: 1=yes, 2=no; `final_weight`: released sampling weight; reference strings separately documented |
| `3_Plot_mainSeason.dta`: household plot in main-season roster | `hhid`, `s02_plotRoster__id` | `s02_q07`: infrastructure 1/2; `s02_q08`: method 1–8 or99 when applicable; `s02_q09`: source 1–6 or99; `s02_q16a`: square-metre area |
| `10_Plots_drySeason.dta`: household plot in minor-season roster | `hhid`, `s02_plotRoster_ds__id` | `s02_q07_ds`: infrastructure 1/2; dry-calendar discrepancy unresolved |
| `9_Input_use_mainSeason.dta`: household/input-type observation | `hhid`, `s03c_inputType__id` | `s03c_q01`: quantity labelled kg in released file; full harmonization lineage not established, no quantity estimator approved |

## Types, nulls and keys

The E1.1 selected IDs, response and weight fields parse as float64; this is an observed physical representation, not permission to round identifiers. Numeric IDs are normalized consistently for ephemeral joins without disclosing them. Do not create new person identities from these keys. Check uniqueness/completeness before aggregation; future violations require investigation rather than blind deduplication. E1.2 confirms the input and dry-plot composite keys too.

Ordinary and tagged Stata missing values remain missing; blank IDs are missing. Unknown response codes remain a separate quality category. Zero is never a generic null replacement. Irrigation q7=no skips method/source questions; non-applicable blanks must not count as ordinary incompleteness. All source records remain immutable, with no automatic imputation or exclusions. A changed archive hash/schema requires a new/reviewed contract.

## Relationships and units

Household-to-plot and household-to-input are one-to-many, with household many-side coverage verified. Never count joined plot/input rows as households. Keep seasons separate, and do not infer a main/dry plot match from equal numerical plot IDs. Quantity counts describe input rows; they are not counts of input users. No sums are computed across survey and synthetic origins.

## Spatial and access assumptions

No coordinates or spatial transformations are used, so CRS/coordinate precision is not applicable to this increment. Geography labels alone do not establish estimate precision. Forestry `ea_name` remains excluded from analysis and release; no point/EA disclosure is approved. No row-level API, database access role or public endpoint exists. Local authorized analyst access only; raw inputs/derivatives and machine outputs are ignored by Git, aggregate reports manually reviewed. Actual source restrictions are in the source card, with public-release review still required.

## Analytical limits

Use only [NASS-01](../NASS_INDICATOR_CONTRACT.md) for the initial M2 sample indicator. Weight applicability, variance design, dry-period conflict and area/quantity exclusions are binding in the [design review](NASS_DESIGN_AND_PERIOD_REVIEW.md). No cleaning corrections have been made; future corrections must preserve raw inputs and record source hash, rule, transformation version and reason.

## Scoped NASS-02 extension ? 2026-10-29

The [NASS-02 contract](../NASS02_INDICATOR_CONTRACT.md) permits bounds for the released `s02_q16a` field as labelled, over all documented plot types. It does not certify GPS/physical measurement lineage or permit acres substitution, yields, farm totals or population inference. Other area/quantity gates remain active.
