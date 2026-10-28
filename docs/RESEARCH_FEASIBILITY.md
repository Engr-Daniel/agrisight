# Research questions and source feasibility

Date: 2026-10-28. **Initial documentation evidence recorded; downloaded-file feasibility is not established.** A first E1 profiling target is proposed, not a finalized population indicator. No microdata findings exist. See the [source card](data_sources/NASS_2023_CARD.md) for citations, questionnaire provenance and unresolved gates.

## Dataset decision

Inspect NASS 2023 first. GHS Panel 2023–24 is a genuine alternative, not automatically a supplementary dataset. Select GHS if documented evidence shows it better supports the chosen question. Use one source for the first complete analysis; record a switch rationale rather than merging incompatible samples.

Starting catalogues for inspection (not evidence of file permissions or verified variables):

- NASS: https://microdata.nigerianstat.gov.ng/index.php/catalog/173
- GHS NBS: https://microdata.nigerianstat.gov.ng/index.php/catalog/82
- GHS World Bank: https://microdata.worldbank.org/catalog/6410

Compare question fit, variables, access conditions, unit/keys, weight and variance-design support, reference periods, geography and implementation complexity. Verify actual release version at acquisition.

## Provisional questions

| ID | Question | Required concepts, not verified variable names | Current disposition |
|---|---|---|---|
| RQ1 | How does participation in selected agricultural activities vary across statistically supported geographic domains? | Activity participation, eligible universe, domain, appropriate weight/design | Needs narrowing: household activity fields documented; supported domains/design unresolved |
| RQ2 | How does access to selected agricultural inputs or services differ across defined farming groups? | Access/use distinction, groups, eligibility, period, weight/design | Needs narrowing: infrastructure presence and input quantity are not equivalent to access |
| RQ3 | How sensitive are those findings to missing data, eligibility rules and reasonable analytical assumptions? | Missing/skip codes, exclusions, defensible alternative definitions, E2 estimates | Deferred until E1 and an E2 baseline exist |

## Variable-to-question evidence matrix

Add rows for each required variable and relationship during documentation inspection. A catalogue description alone does not establish feasibility.

| Question | Source/release | File/module | Exact variable + label | Unit/key and joins | Universe/skip/missing codes | Period/domain | Weight and variance design | Evidence page/section | Decision |
|---|---|---|---|---|---|---|---|---|---|
| RQ1 | NASS mirrored release; actual download pending | 1_households / F14 | s00_q15a/b, s00_q16/17/18; zone_id | Candidate hhid; uniqueness untested | Season-specific activities; full codes pending | Reference fields documented; domains unresolved | final_weight listed; applicability and variance design pending | Source card: F14; questionnaire administrative activity questions | Needs narrowing |
| RQ2 | Same | 3_Plot_mainSeason / F16 | s02_q07; 1=yes, 2=no | Candidate hhid + s02_plotRoster__id | Plot roster; missingness untested | Main season; period reconciliation pending | Household weight listed on plots; estimand/design unresolved | Source card: F16/V1112; questionnaire p.13 | Needs narrowing; proposed first E1 target |
| RQ2 | Same | 9_Input_use_mainSeason / F22 | s03c_inputType__id; s03c_q01 | Household/input rows; candidate keys untested | Type roster depends on previous responses | Rainy season questionnaire; units need review | final_weight listed; not a complete estimation contract | Source card: F22; questionnaire p.39 | Deferred for use/access indicator |
| RQ3 | Not yet selected | Depends on baseline | Codes/exclusions to be specified | Depends on selected unit | Missing is not no | Depends on E2 | Depends on E2 | Source card: remaining gates | Deferred |

Final dispositions: **supported**, **needs narrowing**, **deferred**, **unsupported**. Explain each decision and blocker. If neither source supports a question, revise or defer it; do not invent fields or substitute synthetic observations.

## First-indicator selection gate

Record selected question, source/release and exact variables; target population; observation unit and keys; numerator/denominator; eligibility; period/domain; missingness/exclusions; applicable weight; uncertainty method and design variables; access conditions; independent cross-check and tolerances. If design support is insufficient, restrict output to labelled sample descriptions or defer population inference.

Do not infer causes from descriptive associations, treat unknown responses as non-use, interpret repeated household IDs across crop rows as duplicates, or infer local estimate precision from geographic coverage alone.
