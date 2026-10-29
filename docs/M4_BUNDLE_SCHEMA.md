# M4 aggregate reporting bundle schema v1.0

Implemented by [reporting_adapter.py](../src/agrisight/reporting_adapter.py), independent of Streamlit. This defines the metric-record schema promised by the [reporting contract](M4_REPORTING_CONTRACT.md). It adds no analytical estimator or row-level input.

## Trust and lifecycle

The packaged [manifest](../src/agrisight/reporting/artifact_manifest_v1.json) binds four previously reproduced aggregate artifacts to exact raw-byte SHA256 and reviewed indicator/version/provenance fields. It contains only checksums, experiment/model identifiers, labels and an observation date, not restricted rows or identifying coordinates. The CLI always loads this packaged manifest; it cannot mint a new trusted snapshot, accept a manifest upload or change source paths interactively.

For a new snapshot, reproduce and review the analytical outputs first, verify source/model/contract/protocol/lock provenance and scientific permissions, then explicitly amend/version the manifest and relevant contracts in a reviewable change. Do not regenerate the manifest simply to silence a mismatch. Hashes identify reviewed bytes; they do not establish authenticity or statistical validity.

Offline `build_bundle(root, manifest=None, built_at=None)` permits a developer-supplied alternate manifest for tests. That parameter is a trusted development interface, not an untrusted request input. CI manifests use purpose `TEST FIXTURE`, forcing that origin label on every panel, including survey-shaped records. Production CLI uses the reviewed local evidence manifest only.

The root is a checkout directory; only the four fixed filenames beneath `reports/private` are read. Resolved paths must remain beneath that root, including when symlinks/junctions are present. No raw microdata, URL fetch, database query, experiment run or Streamlit import occurs. Parsed JSON rejects duplicate keys, nonfinite floats and invalid JSON. Unknown input fields are never copied through to reporting records.

## Envelope and panels

| Field | Type and semantics |
|---|---|
| `report_contract_version` | String `1.0` |
| `built_at_utc` | Actual timezone-aware ISO8601 UTC timestamp; not the survey date or proof of updated data |
| `artifacts` | Exactly the four logical filenames. Each maps to `{sha256, status}`; `verified` means byte/provenance checks passed, not that later panel arithmetic passed. Unavailable input has null checksum and `unavailable` status |
| `panels` | Exactly `survey`, `synthetic_quality`, `synthetic_workload`; no common population or rolled-up total |

Each panel has `origin`, `reference_period`, `observed_date`, `limitations`, `status`, `records`, `provenance`. Available panels have their allow-listed records and only reviewed manifest provenance fields. Unavailable panels have no records/provenance and a generic safe remediation `message`. Invalid arithmetic may make a panel unavailable even when its input bytes match the manifest. Logs/output never include caught exception text or source contents.

The survey panel depends on both NASS artifacts and is blocked as a unit. Each synthetic panel has its own artifact and independent status. No cached success or fallback constants survive a failed reload. The CLI writes the current bundle, including unavailable states, and exits1 if any panel is unavailable; a successful bundle exits0. Output must remain under ignored `reports/private` and cannot overwrite any of the four evidence inputs. CLI validation failures emit a generic remediation message without traceback or local paths.

## Metric records

Every record has exactly `id`, `selectors`, `counts`, `values`, `units`, `status`. The composite of `id` and selectors identifies a cell; `id` alone is not unique across synthetic cells. Counts are nonnegative JSON integers, never booleans; NASS-02 rank fields alone may be null for an empty roster. Numeric values are finite/nonnegative numbers or explicit nulls as below. No presentation rounding occurs in the adapter.

| ID | Selectors | Count keys | Values/units and status |
|---|---|---|---|
| `NASS-01` | Empty | `input_rows`, `numerator`, `denominator`, `no_count`, `missing_count`, `invalid_count`, `excluded_count` | `proportion` fraction, `percentage` percent. Status `defined` or `undefined` for zero eligible denominator; values null in that case |
| `NASS-02` | Empty | `total_plots`, `observed_areas`, `missing_areas`, `middle_lower_rank`, `middle_upper_rank` | `observed_only_median_m2`, `full_roster_lower_m2`, `full_roster_upper_m2`, `width_m2`, all released labelled square metres. Status `bounded`, `unbounded` or `undefined`; null is never substituted with0 |
| `synthetic_quality` | `seed`, `configuration`, `baseline`, `measure` | `events`, `people`, `intended_roles`, `tp`, `fp`, `fn`, `tn`, `universe`, `true_pairs_or_labels`, `predicted_pairs_or_labels` | `precision`, `recall`, `false_positive_rate` as fractions/null. Record status `defined` means a valid aggregate cell; individual rates may still be undefined/null |
| `synthetic_workload` | `events`, `collision` boolean | `events`, `people`, `intended_roles`, `candidate_pairs`, `pair_budget` | `timing` summary in seconds, `traced_allocation` summary in MiB; status `success` or `candidate_budget_exceeded` |

Quality selections are exactly seeds 303/404/505, configurations Clean/Exact-repeat/Mixed and methods B0/B1. Measures are `same_person`, `duplicate_role`, `quality` (micro field total), or one of `missing_name`, `missing_contact`, `name_whitespace`, `contact_whitespace`. This produces 126 records. People/roles/events describe that dataset, not the count of flagged identities. Baseline field-quality results are intentionally equal; no independent corroboration is claimed from that equality.

Benchmark selections are four bounded cases (1000/10000/55000/100000 events) plus separate collision cases 300 and1000. A summary is `{values, minimum, median, maximum, sample_stdev}`; all 5 timing and 3 independent memory repetitions are retained. A rejected cell has both summaries null, not zero-valued summaries. Worker logs, raw row identifiers, tokens, scenario pair breakdowns and machine paths are not projected. Benchmark hardware/conditions remain in the reviewed findings report; panel limitations preserve timed scope, shared load and partial-memory exclusions.

## Validation formulas and limits

- NASS-01 checks yes+no=denominator, missing+invalid=excluded and denominator+excluded=input rows. Reconciles supplied proportion/percentage to counts; zero denominator requires null values.
- NASS-02 checks known+missing=roster, middle ranks, known-only null semantics and bounded/unbounded/empty status consistency. Known values/bounds are nonnegative, lower cannot exceed a bounded upper, and width equals upper-lower. No missing values requires endpoints equal to the known-only reference. This checks existing aggregate structure; without raw areas it cannot independently recompute the order statistics. Those were already SQL/Python reconciled in M3.
- Confusion counts satisfy TP+FP+FN+TN=universe; true positives count=TP+FN; predictions=TP+FP. Pair universe is events*(events-1)/2, quality micro universe events*4, and per-rule universe events. The four rule count vectors sum to micro counts; baseline truth-positive pair counts agree.
- Precision=TP/(TP+FP), recall=TP/(TP+FN), FPR=FP/(FP+TN), null if the respective denominator is0. These denominators are available from count keys. Rates are verified rather than accepted because a stored percentage looks plausible.
- Dataset counts obey people<=intended roles<=events and intended roles<=2*people for this single-programme/two-role snapshot.
- Benchmark checks exact case/repetition sets, statuses, verified flags, worker count/input/truth/prediction agreement and full summary statistics. Reference accuracy cells pass the same aggregate metric checks before projection. Candidate budget250000 and the expected1000-event collision rejection remain explicit, not a learned production threshold.

Count/status/rank identities are exact. Numeric comparisons use absolute1e-12 and relative1e-12; area endpoint/width checks use absolute1e-9 and relative1e-12, matching their original contract. Adapter rate/statistic calculations operate only on already-reviewed aggregate counts/repetitions. They do not replace the original independent SQL/Python analytical evidence.

## M4-03 handoff

The interface should consume these records and fixed context, not raw artifacts. Preserve source labels on selection changes, compute display formatting under the reporting contract, and explain null rates using the relevant denominator. A later UI must not accept an arbitrary edited bundle as trusted evidence or cache an old successful panel after validation fails. Bundle build timestamps legitimately differ between reproductions; all other fields matched in the observed paired package runs.
