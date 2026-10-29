# M4 reporting contract v1.0

Specified 2026-10-29 before dashboard implementation. **Contract/initial platform decision complete; application, adapter, dependency lock and UI validation pending.** [ADR-004](adr/ADR-004-initial-reporting-platform.md) selects Streamlit for a local read-only prototype. This contract does not authorize deployment or data redistribution.

## Reader and interaction

Help an analyst or reviewer answer: what was measured, over which records, what changed under a documented choice, and what remains uncertain? Keep official survey results and synthetic engineering evidence in distinct views with persistent source labels. No combined population, enrollment total, map or overall accuracy score.

Initial navigation has three evidence views: survey findings, synthetic matching/quality and synthetic workload measurements. A source/provenance panel accompanies the selected evidence. Include brief explanations of households versus plots, people versus roles versus submission events, and false positives versus missed pairs. Avoid exposing developer logs in the reader flow.

## Display allow-list

| Evidence | Permitted values and denominators | Mandatory interpretation |
|---|---|---|
| NASS-01 | Yes132859, no10246, valid denominator143105, missing/invalid/excluded0; participation92.84% | Unweighted pooled released agricultural-household sample; April-October2022; not national/current prevalence; uncertainty not estimated |
| NASS-02 | Roster273887, known273839, missing48; known-only median and full-roster endpoints6070.290058851242, displayed6070.29; width0 | Released labelled square-metre field, measurement lineage unverified. Known-only reference and full-roster target are distinct. Bounds address unknown nonnegative values only; not confidence intervals or measurement-error bounds |
| Synthetic matching | Evaluation seeds303/404/505, Clean/Exact-repeat/Mixed, B0/B1, same-person/duplicate-role relation; TP/FP/FN/TN, true/predicted pair counts, precision/recall/false-positive rate | SYNTHETIC DEMONSTRATION DATA. Unordered event-pair universe N*(N-1)/2; legitimate cross-role links are not duplicate roles; no automatic merging or real-world accuracy claim |
| Synthetic field quality | Four named rules and micro total; event counts and event-rule confusion counts/rates | Separate from identity matching. Micro universe events*4; each rule universe events. Perfect inserted-rule detection does not validate other defect families |
| Synthetic benchmark | Bounded sizes1000/10000/55000/100000 and separate collision diagnostics; actual event/person/role/candidate counts; all repetitions, min/median/max/sampleSD seconds and separate traced-allocation peaks | Shared-machine validation+guard+B1 batch only; generation/import/startup/hashing/SQL checks/I/O excluded. Existing inputs/native memory excluded from traced peak; not RSS, SLA or production capacity |

Underlying contracts/reviews remain authoritative: [NASS-01](NASS_INDICATOR_CONTRACT.md), [NASS-02](NASS02_INDICATOR_CONTRACT.md), [synthetic contract](SYNTHETIC_REGISTRATION_CONTRACT.md), [quality findings](../reports/M3_SYNTHETIC_QUALITY.md), [benchmark findings](../reports/M3_WORKLOAD_BENCHMARK.md), [M3 review](M3_REVIEW.md). These displayed baseline values are acceptance expectations, not instructions to hard-code UI cards independently of artifacts.

## Inputs and reporting boundary

The planned offline adapter reads only four operator-selected, existing aggregate artifacts under ignored `reports/private`: `nass01.json`, `nass02.json`, `m3_04_evaluation.json`, `m3_05_benchmark.json`. Resolve paths beneath that root and refuse escapes; do not accept browser uploads, arbitrary URL/path inputs or raw Stata/ZIP/row-level tables. Synthetic worker detail may be summarized, but identifiers, matching tokens, actual home paths, hostnames and stack traces never enter reader-facing payloads.

Produce a versioned allow-listed bundle rather than exposing entire input dictionaries. Envelope fields: `report_contract_version` (1.0), `built_at_utc` (timezone-aware ISO8601), `artifacts` (the four logical artifact names with SHA256), and `panels` (separately keyed `survey`, `synthetic_quality`, `synthetic_workload`). Each panel carries its own origin label, metric records, reference-period/experiment metadata, exclusions, uncertainty/status and relevant source/model/contract/protocol/lock hashes. Exact metric-record schema must be documented with the adapter before implementation completion; unknown/extra input keys must not be forwarded automatically.

Validate expected indicator/model/contract versions and frozen survey archive SHA256; verify included provenance against an explicitly reviewed manifest of artifact/model/protocol hashes. Establish this manifest from existing reproduced outputs, not trust-on-first-use from a browser session. Hash agreement identifies bytes; it is not proof of source authenticity, permissions or statistical validity. Validate synthetic seed/configuration/baseline sets and workload statuses against the specified experiments. An adapter must reject mixing artifacts from incompatible model/source versions; a new version requires a reviewed contract/manifest amendment.

Validate denominators, finite numeric types and integer counts (booleans are not counts), arithmetic identities and rates before building the bundle. Preserve available independent reconciliation evidence; UI code does not replace SQL/Python verification. Only recompute display rates/statistics from validated aggregate counts/repetitions, using authoritative formulas/tolerances, not new analytical definitions. No raw survey access, query execution, imputation, deduplication or experiment reruns from UI controls.

CI uses clearly labelled tiny synthetic reporting fixtures, including survey-shaped schema fixtures labelled TEST FIXTURE, never presented as actual NASS findings. Actual owner-authorized artifacts remain ignored. Do not silently replace missing real artifacts with fabricated or hard-coded production-looking results. No downloadable bundle or row-level export in the first prototype.

## Valid selections and presentation semantics

- Survey view: select NASS-01 versus NASS-02 only. No state/LGA, crop, sex, role, date-range or season filters: these pooled aggregates cannot support them.
- Matching view: select one evaluation seed, configuration, baseline and relation. Selection chooses an existing aggregate cell, never filters person rows. Keep dataset event/person/intended-role counts and pair denominator visible. Do not average seed percentages or pool runs silently. Development seeds are excluded from headline views.
- Quality view: select an existing rule or micro total for the chosen seed/configuration. Rule choice changes the evaluation universe and label together. Do not combine rule and identity scores.
- Benchmark view: select workload/collision condition and timing versus traced allocation. Use stored repetitions; no interactive rerun button. Separate collision diagnostics from the bounded-size series; never plot a rejected workload as zero seconds or zero memory. Show full timed scope and memory exclusions beside values.
- Scenario-level pair breakdowns remain out of the initial UI to avoid presenting overlapping groups as additive. They remain available in documented aggregate evidence for later justified work.

Store full precision in the bundle. Display percentages to2 decimal places, area to2 decimals, seconds to3 decimals and MiB to2 decimals; exact counts remain integers. Small positive rates rounding below0.01% display `<0.01%`, never0.00%; preserve FP counts and exact denominators in the evidence table. Do not imply physical measurement precision from stored digits.

Undefined precision/recall from zero denominators displays `Not defined` with the denominator reason; null is not0. Empty/unavailable median is distinct from unbounded upper endpoint, and both are distinct from recorded0. Rejected benchmark cells display `Rejected: candidate budget exceeded`,499500 potential candidates versus250000 budget, with time/memory unavailable. Future unsupported rejection reasons cannot inherit this specific label automatically.

## Freshness, failures and local access

Distinguish survey period April-October2022, acquisition/experiment observation date2026-10-29 and bundle build time. A new build does not make findings current. Refresh is an explicit offline artifact-validation/build step, not a live feed or automatic reanalysis. Reload by bundle content hash; no stale cached success after failed validation or source replacement.

Missing, malformed, nonfinite, hash-mismatched, incompatible or internally inconsistent artifacts block their dependent panels with a concise unavailable message and safe remediation. Valid unrelated panels may remain available only with visibly independent status; no partial mixture within a dependent panel. Logs remain local and must not dump artifact contents or sensitive paths. Do not fabricate a "last successful" result after a failure.

Initial server is local loopback only; no multi-user roles/authentication, sharing URL, public deployment or cloud persistence is implemented by this contract. No maps, coordinates, geography boundary downloads, respondent drill-downs or cross-season comparisons. These require separate data/support/disclosure review before any future implementation.

## Definition of done and learning checks

1. Pin/reproduce the presentation dependency increment without silently changing analytical results; implement the strict adapter/manifest and document the metric-record schema.
2. Test happy/negative/edge cases: absent/corrupt/mixed-version artifacts, path escapes, altered hashes, negative/nonfinite/boolean counts, zero denominators, unbounded/undefined area status, benchmark rejection and no leakage of unknown fields. Check fixture truth independently, not only adapter/UI agreement.
3. Use Streamlit AppTest to verify every supported selection preserves its source label, unit, denominator, value and limitation; test unavailable panels and selection transitions. Verify rounded presentation against exact aggregate expectations. Existing regression checks must pass.
4. Execute the app locally using actual authorized aggregate artifacts, observe server startup and conduct a browser/usability review when browser tooling is available. Record what was genuinely inspected; headless tests or a running port alone do not prove visual usability.
5. Complete an internal M4 review recording reproducible commands, observed outcomes and remaining gates before checking the prototype complete. No requirement to add Power BI, maps, hosting or another framework to close this scoped prototype.

Learning checks: does changing from same-person to duplicate-role update the meaning and precision/recall denominators while preserving the same total pair universe? Can a reader distinguish55000 events from39363 true synthetic people? Can the reader explain why a zero-width missing-area bound does not certify physical measurement accuracy? These are interpretation checks, not completed stakeholder validation.

## M4-02 implementation follow-up

The [bundle schema](M4_BUNDLE_SCHEMA.md) now defines the exact record shape and trust boundary. [Adapter/dependency review](M4_ADAPTER_REVIEW.md) verifies the corresponding implementation and installed-wheel reproduction. The prospective specification above is preserved; its initial pending statements describe that earlier stage. UI, local server/usability checks and full M4 completion remain pending.

## M4-03 implementation follow-up

[UI verification](M4_UI_REVIEW.md) records the now-implemented views and automated interactions. Local loopback health checks passed and the test server was stopped; actual browser/usability review and combined M4 closure remain pending. No scientific/data-release gate is waived.
