# KPI dictionary — M0 approved baseline for synthetic-track fixtures
Date: 2026-10-27. These definitions apply to **synthetic actor-role registration**, not survey-weighted estimates or a real farmer registry.

## Status and grain
- `role_id`: one actor-role entry, unique in accepted registry; `person_id`: an opaque distinct simulated individual, potentially linked to more than one role.
- `kind`: farmer or processor. `status`: pending, accepted or rejected.
- Distinct people are **not** calculated by adding farmer and processor counts.
- `complete`: currently a deliberately simplified educational flag. Actual completeness will use applicable required fields and skip logic in M1.
- Report refresh date and origin on any exported metric.

| ID | Indicator | Formula, grain and exclusions | Six-row fixture |
|---|---|---|---|
| KPI-01 | Submitted role records | COUNT(all submitted role entries); includes pending/rejected | 6 |
| KPI-02 | Accepted role records | COUNT(role_id WHERE status='accepted') | 4 |
| KPI-03 | Accepted farmer roles | COUNT(role_id WHERE accepted AND kind='farmer') | 2 |
| KPI-04 | Accepted processor roles | COUNT(role_id WHERE accepted AND kind='processor') | 2 |
| KPI-05 | Distinct people with accepted role | COUNT(DISTINCT person_id WHERE status='accepted') | 3 |
| KPI-06 | Complete accepted role records | COUNT(role_id WHERE accepted AND complete=true) | 3 |
| KPI-07 | Incomplete accepted role records | COUNT(role_id WHERE accepted AND complete=false) | 1 |

## Numerator/denominator rules
- Illustrative acceptance share = KPI-02 / KPI-01 = 4/6 = 66.7% (not registration completion or field quality).
- Illustrative completeness among accepted = KPI-06 / KPI-02 = 3/4 = 75%. This **is not** full questionnaire completeness.
- If denominator is zero, return undefined/NA, **not** silently 0%.
- Do not report counts as prevalence or population estimates. The fixture has only six synthetic submission records.

## Future KPIs requiring separate designs/tests
Geographic assignment completion, weighted survey estimates, quality issue prevalence, duplicate candidate *pairs* vs affected record rates, verification/back-check coverage, consent, pipeline freshness, commodity participation and privacy small-cell rules. Their inclusion criteria/denominators must be approved before implementation.

## Verification evidence
`src/agrisight/kpi_fixture.py` independently aggregates with Python and SQLite. `tests/test_kpi_fixture.py` compares both with manually enumerated counts and handles empty input. Github Foundation CI: https://github.com/Engr-Daniel/agrisight/actions/runs/40495776063.
