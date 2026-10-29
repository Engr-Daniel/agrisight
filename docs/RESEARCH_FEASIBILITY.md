# Research questions and source feasibility

Updated: 2026-10-29. **M1 suitability decision finalized after E1.1/E1.2.** Selected indicator is [NASS-01](NASS_INDICATOR_CONTRACT.md), main-season participation in the observed sample; population-analysis feasibility remains unestablished. See [findings](../reports/E1_REAL_DATA_PROFILING.md), [design/period review](data_sources/NASS_DESIGN_AND_PERIOD_REVIEW.md) and [M1 review](M1_REVIEW.md).

## Dataset decision

Inspect NASS 2023 first. GHS Panel 2023–24 is a genuine alternative, not automatically a supplementary dataset. Select GHS if documented evidence shows it better supports the chosen question. Use one source for the first complete analysis; record a switch rationale rather than merging incompatible samples.

Final M1 decision: retain acquired NASS for the main-season sample workflow. GHS `sect11l1_plantingw5` documents `hhid`, `topic_cd`, `s11l1q1` and `s11l1q2`, making it a stronger conceptual alternative for advice/service questions; it has not been acquired or empirically validated. Do not merge sources or rename infrastructure presence as service access.

Starting catalogues for inspection (not evidence of file permissions or verified variables):

- NASS: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
- GHS NBS: https://microdata.nigerianstat.gov.ng/index.php/catalog/82
- GHS World Bank: https://microdata.worldbank.org/catalog/6410

Compare question fit, variables, access conditions, unit/keys, weight and variance-design support, reference periods, geography and implementation complexity. Verify actual release version at acquisition.

## Provisional questions

| ID | Question | Required concepts, not verified variable names | Current disposition |
|---|---|---|---|
| RQ1 | How does participation in selected agricultural activities vary across statistically supported geographic domains? | Activity participation, eligible universe, domain, appropriate weight/design | Narrowed to observed-sample main-season crop participation; population/geographic comparison deferred |
| RQ2 | How does access to selected agricultural inputs or services differ across defined farming groups? | Access/use distinction, groups, eligibility, period, weight/design | Needs narrowing: infrastructure presence and input quantity are not equivalent to access |
| RQ3 | How sensitive are those findings to missing data, eligibility rules and reasonable analytical assumptions? | Missing/skip codes, exclusions, defensible alternative definitions, E2 estimates | Deferred until E1 and an E2 baseline exist |

## Variable-to-question evidence matrix

Add rows for each required variable and relationship during documentation inspection. A catalogue description alone does not establish feasibility.

| Question | Source/release | File/module | Exact variable + label | Unit/key and joins | Universe/skip/missing codes | Period/domain | Weight and variance design | Evidence page/section | Decision |
|---|---|---|---|---|---|---|---|---|---|
| RQ1 | Owner-supplied NASS archive, frozen by hash | 1_households / F14 | s00_q15a/b, s00_q16/17/18 | hhid complete/unique; all five activity fields parsed | Codes 1/2 only; no missing/other in these fields | Main Apr–Oct 2022 supported; minor year conflict; no domain inference | final_weight positive/finite; usable variance design unidentified | E1.2 findings, report §2.13, NASS-01 contract | Narrowed to pooled main-season sample description |
| RQ2 | Same | 3_Plot_mainSeason / F16 | s02_q07; parsed values 1/2 only | Composite key complete/unique; no orphan HH IDs | No missing infrastructure codes; broader skips pending | Main season; period reconciliation pending | Household weight positive/finite on plots; estimand/design unresolved | E1.1 findings; F16/V1112; questionnaire p.13 | Supported for bounded quality profiling only; access question needs narrowing |
| RQ2 | Same | 9_Input_use_mainSeason / F22 | s03c_inputType__id; s03c_q01 | Household/type keys complete/unique; no orphan links | 15409 missing quantities; roster-dependent inclusion | Main season; harmonization provenance not fully established | No input quantity/access estimator approved | E1.2 findings; F22; questionnaire p.39 | Deferred for use/access indicator |
| RQ3 | Not yet selected | Depends on baseline | Codes/exclusions to be specified | Depends on selected unit | Missing is not no | Depends on E2 | Depends on E2 | Source card: remaining gates | Deferred |

Final dispositions: **supported**, **needs narrowing**, **deferred**, **unsupported**. Explain each decision and blocker. If neither source supports a question, revise or defer it; do not invent fields or substitute synthetic observations.

## First-indicator selection gate

Record selected question, source/release and exact variables; target population; observation unit and keys; numerator/denominator; eligibility; period/domain; missingness/exclusions; applicable weight; uncertainty method and design variables; access conditions; independent cross-check and tolerances. If design support is insufficient, restrict output to labelled sample descriptions or defer population inference.

Do not infer causes from descriptive associations, treat unknown responses as non-use, interpret repeated household IDs across crop rows as duplicates, or infer local estimate precision from geographic coverage alone.
