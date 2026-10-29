# E3 — Sensitivity readiness and next empirical question

Specified 2026-10-29. **NASS-01 readiness audit only; substantive E3 execution not complete.** No new agricultural indicator is implemented by this document. All M1 inference, reference-period and access restrictions remain active.

## 1. What can change the existing result?

NASS-01 describes main-season crop participation among valid responses in the recorded agricultural-household sample. E2 observed 143105 rows, 132859 yes, zero missing/invalid responses and complete unique keys. Preserve the same source hash, sample, period and outcome.

| Proposed check | Classification and disposition |
|---|---|
| Valid-response versus all-record denominator | Identical sets in this source snapshot because no response is excluded; limited invariance audit only |
| All unknown responses assumed no versus yes | No unknown responses exist, so both bounds collapse to the existing value; not evidence about unobserved households or response error |
| Different SQL/Python implementation, row ordering | Engineering correctness checks already tested in M2, not scientific sensitivity |
| Display rounding | Presentation choice, not analytical robustness |
| Restrict to crop growers, households with plots, or another geographic group | Changes the target group/question; requires a new indicator contract, not a sensitivity test of NASS-01 |
| Weighted versus unweighted result | Different inferential target and unverified weight/design applicability; not approved as a sensitivity shortcut |
| Household bootstrap / conventional CI | Does not establish the actual complex survey design; no population uncertainty claim |
| Inject missingness or errors into real records | Not authorized empirical E3; synthetic engineering studies stay separate |

An unchanged result here means **no sensitivity to observed response exclusions for this snapshot**, not broad robustness, accurate answers, complete sampling coverage or national representativeness.

## 2. Reproduce the limited audit

Run from the repository root in the existing pinned environment. The code below consumes only the ignored aggregate E2 artifact, refuses a changed source or newly excluded responses, and checks the arithmetic separately with SQLite. It never edits survey records.

```python
from pathlib import Path
import hashlib
import json
import math
import sqlite3

source = json.loads(Path('reports/private/nass01.json').read_text())
expected_hash = 'a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02'
if source['indicator'] != 'NASS-01' or source['source']['archive_sha256'] != expected_hash:
    raise ValueError('Unexpected indicator/source; reassess E3 readiness')
c = source['counts_and_rates']
if c['excluded_count'] != 0 or c['missing_count'] != 0 or c['invalid_count'] != 0:
    raise ValueError('New exclusions require a revised pre-specified protocol')
if not (0 <= c['numerator'] <= c['denominator'] == c['input_rows']):
    raise ValueError('Aggregate identity check failed')
if c['denominator'] == 0:
    raise ValueError('No eligible observations for this readiness audit')
python_value = c['numerator'] / c['denominator']
with sqlite3.connect(':memory:') as db:
    values = db.execute('''
        WITH x(yes, eligible, all_rows, excluded) AS (VALUES (?, ?, ?, ?))
        SELECT 1.0*yes/eligible, 1.0*yes/all_rows,
               1.0*yes/all_rows, 1.0*(yes+excluded)/all_rows FROM x
    ''', (c['numerator'], c['denominator'], c['input_rows'], c['excluded_count'])).fetchone()
if not all(math.isclose(python_value, v, rel_tol=0, abs_tol=1e-12) for v in values):
    raise ValueError('Readiness arithmetic did not reconcile')
if not math.isclose(python_value, c['proportion'], rel_tol=0, abs_tol=1e-12):
    raise ValueError('Readiness audit disagrees with the E2 baseline')
result = {
    'source_sha256': expected_hash, 'indicator': 'NASS-01',
    'baseline_result_sha256': hashlib.sha256(
        Path('reports/private/nass01.json').read_bytes()).hexdigest(),
    'excluded_responses': 0, 'baseline_proportion': python_value,
    'valid_all_denominator_difference': 0,
    'unknown_response_bounds_width': values[3] - values[2],
    'sql_python_match': True,
    'scope': 'Limited response-exclusion invariance, not substantive E3 completion'
}
target = Path('reports/private/e3_readiness.json')
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
```

If source counts change, re-specify before interpreting any new result. With positive missingness, an all-record target and a valid-responder target need not be identical; this audit deliberately does not generalize to that case.

## 3. Shortlist for an informative next question

| Candidate | Agricultural value | Sensitivity potential / readiness |
|---|---|---|
| Median released main-season plot area | Describe the middle recorded plot size, not total farm size or national holdings | 48 missing areas observed; same-target missing-outcome bounds possible. Recommended next feasibility gate; units/measurement lineage and eligible roster must be confirmed first |
| Main-season crop / annual livestock co-occurrence | Describe overlapping household activities without double counting | Relevant fields are documented and valid, but no missingness identified; useful new question, not inherently a sensitivity study. Seasonal versus annual reference periods must remain explicit |
| Input-type-specific quantity summaries | Characterize reported inputs with explicit units | 15409 missing quantities provide a real issue, but roster inclusion, type/unit harmonization and missingness meaning need further review; deferred, no pooled totals |

Source evidence: [E1 findings](../../reports/E1_REAL_DATA_PROFILING.md), [plot dictionary](https://microdata.worldbank.org/catalog/8194/data-dictionary/F16?file_name=3_Plot_mainSeason), local questionnaire PDF p.16 and [design/period review](../data_sources/NASS_DESIGN_AND_PERIOD_REVIEW.md). The questionnaire separates farmer estimates/units and GPS measurement; a released square-metre label alone does not certify GPS origin or conversion lineage.

## 4. Proposed same-target study: plot-area median bounds

**Status: conditional proposal, not approved numeric results or a new implemented indicator.** Draft label NASS-02; finalize a versioned contract only after the gates below. Do not call the complete-case median an already identified median of the full roster.

- Target: median of the selected released main-season area field over all eligible main-season plot records. Unit is one plot, not a household, farm enterprise or person. Retain cultivated/fallow/kitchen-garden distinctions when deciding eligibility; do not choose a subgroup after seeing the answer.
- Baseline: median among valid observed areas, explicitly conditional on observed values. Its difference from the full-roster target is part of the missing-data problem, not silently ignored.
- Sensitivity: calculate order-statistic lower/upper bounds on the **same full-roster median** over all possible nonnegative completions of genuinely missing area values. Do not insert artificial values into the original data and do not assume MAR or a convenient maximum area.
- For odd total N, middle rank r=(N+1)/2 and m unknown areas: the lower endpoint uses known rank r-m and upper endpoint known rank r, when those ranks exist. Otherwise retain nonnegative lower support0 or unbounded upper support as applicable. For even N apply the same logic to both middle ranks and their average; state that median convention explicitly.
- Teaching fixture: with N=5, known areas [1,3,5,7] and one missing area, the observed-only median is4 but the full-roster median is bounded by3 and5. This is synthetic mathematical illustration, not an agricultural finding.
- Independently reconcile ranks/endpoints in SQL and Python; test odd/even, no missing, all missing, invalid areas, duplicate keys and support endpoints before real execution. These are missing-value identification bounds, **not confidence intervals** or survey population bounds.
- Report numeric bound width and its relative scale without inventing a threshold to declare it “robust.” A tight interval would address only missing areas, not measurement error, selection, conversion uncertainty or population representativeness.

## 5. Mandatory next gates and scope

Before computing the next indicator: establish the selected area field's released unit and measurement/derivation status, inspect companion field labels and documented plot eligibility, distinguish structural non-applicability from unknown measurement, and define handling of nonpositive/nonfinite values. If provenance cannot be resolved, either explicitly target the released field with limited measurement claims or defer it; do not claim physical/GPS accuracy.

Finalize the contract and executable E3 protocol before numerical analysis, then produce reconciled sample results and a limitations report. Synthetic duplicate truth, precision/recall and the 55k workload are separate M3 tasks and remain unexecuted. This document/readiness audit alone does not complete M3.
