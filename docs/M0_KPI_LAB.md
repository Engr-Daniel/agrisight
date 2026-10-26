# M0-04 — Registration KPI reconciliation lab

**Status:** executable small fixture; no real data, no registry, no fieldwork.

## Learning goal
The unit of observation (grain) matters. A person may have more than one agricultural role. Six **synthetic role submissions** yield four accepted roles but three accepted distinct persons because p2 has both farmer and processor roles.

| Metric | Expected |
|---|---:|
| Submitted role records | 6 |
| Accepted role records | 4 |
| Accepted farmer roles | 2 |
| Accepted processor roles | 2 |
| Distinct people with accepted roles | 3 |
| Complete accepted role records | 3 |
| Incomplete accepted role records | 1 |

The fixture also includes one pending and one rejected record, neither counted as accepted. These six deliberately constructed examples are **not** observations from Nasarawa or any public survey.

## Run
```bash
python -m pip install -e ".[dev]"
python -m agrisight.kpi_fixture
python -m pytest -q
```
The lab requires only the Python standard library; the demonstration SQL runs through SQLite in memory. PostgreSQL/dbt are proposed for M2, not represented as implemented here.

## Reconciliation
`python_metrics` performs Python aggregations. `sql_metrics` uses SQL COUNT, SUM(CASE) and COUNT(DISTINCT). Tests assert equality to a manually calculated expected result, not merely that two algorithms agree. SQL constraints reject invalid role/status values and repeated role keys. COALESCE makes empty-dataset SUM results zero instead of NULL.

## Limitations and follow-ups
- This is a tiny deterministic fixture, not a 55,000-record performance test.
- `complete` is a simplified illustrative flag; actual field-specific mandatory data and skip logic are future tasks.
- There is no real person-identification matching or duplicate-detection benchmark yet.
- Field statuses, role overlap policy, revised records and geographical grain still need formal approval.
- Do not generalize fixture proportions as prevalence in any agricultural population.

## Review exercises
1. Why does adding farmer and processor role counts not necessarily equal distinct people?
2. What happens if a role changes from pending to accepted?
3. Should a profile flagged incomplete be excluded from accepted registration? Why does that depend on status definitions?
4. Which SQL aggregation incorrectly inflates unique people when joining to multiple commodities?
