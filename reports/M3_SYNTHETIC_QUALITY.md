# M3-04 synthetic quality and duplicate evaluation

Follow-up 2026-10-29: the later [workload findings](M3_WORKLOAD_BENCHMARK.md) and [combined M3 review](../docs/M3_REVIEW.md) supersede this accuracy-stage benchmark handoff. Accuracy results and their frozen protocol are unchanged.

Observed 2026-10-29. **SYNTHETIC DEMONSTRATION DATA.** M3-04 complete for the fixed baseline experiment; M3-05 benchmarking remains unexecuted. These are synthetic engineering results, not agricultural survey findings, enrollment counts or production accuracy estimates.

## Decision

Keep both methods as explicit review baselines, not automatic identity resolution. Normalization recovers case/whitespace variants, but exact name/contact agreement cannot resolve shared tokens, typos or absent contacts. No records were merged, deleted or corrected. No new matching dependency, database service or dashboard was introduced.

The fixed generator starts with1000 synthetic people and1200 intended roles (1000 farmer,200 processor). Clean has1200 events; Exact-repeat and Mixed each add200 repeated farmer submissions for1400 events. The dual roles are valid. Additional submissions increase events, not true people or intended roles. There are no crops or coordinates in this workload.

## Pre-specification and execution

The [contract](../docs/SYNTHETIC_REGISTRATION_CONTRACT.md) and [protocol](../docs/experiments/M3_04_PROTOCOL.md) preceded execution. The protocol's implementation clarification fixed mutation/sampling order before development or reserved-seed runs; its original prospective text is preserved. Development seeds101/202 were run first. Code, protocol, contract and lock hashes were saved to ignored `reports/private/m3_04_frozen.json` before first evaluation of303/404/505. All frozen bytes remained unchanged after evaluation; no score-driven retuning occurred. Reserved seeds test repeatability of this deliberately constrained generator, not generalization to real registrations.

B0 requires raw exact name/contact agreement. B1 strips surrounding whitespace and casefolds both tokens before exact agreement. Both abstain on absent/blank tokens; duplicate-role flags additionally require equal role kind. Status does not exclude events. Detector inputs contain only observations, not truth IDs, labels or scenario. Evaluator truth is constructed separately from mutation choices and used only after prediction.

## Reserved-seed identity results

Each row reports unordered submission pairs. TP/FP/FN/TN exhaust the full N*(N-1)/2 universe; negatives are not materialized. Precision and recall are fractions. A dash denotes an undefined denominator, not zero performance. Same-person positives include legitimate cross-role pairs; duplicate-role positives do not.

| Seed | Configuration | Method | Relation | TP | FP | FN | TN | Precision | Recall |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 303 | Clean | B0 | same_person | 200 | 0 | 0 | 719200 | 1.000000 | 1.000000 |
| 303 | Clean | B0 | duplicate_role | 0 | 0 | 0 | 719400 | - | - |
| 303 | Clean | B1 | same_person | 200 | 0 | 0 | 719200 | 1.000000 | 1.000000 |
| 303 | Clean | B1 | duplicate_role | 0 | 0 | 0 | 719400 | - | - |
| 303 | Exact-repeat | B0 | same_person | 442 | 0 | 0 | 978858 | 1.000000 | 1.000000 |
| 303 | Exact-repeat | B0 | duplicate_role | 200 | 0 | 0 | 979100 | 1.000000 | 1.000000 |
| 303 | Exact-repeat | B1 | same_person | 442 | 0 | 0 | 978858 | 1.000000 | 1.000000 |
| 303 | Exact-repeat | B1 | duplicate_role | 200 | 0 | 0 | 979100 | 1.000000 | 1.000000 |
| 303 | Mixed | B0 | same_person | 262 | 15 | 180 | 978843 | 0.945848 | 0.592760 |
| 303 | Mixed | B0 | duplicate_role | 50 | 10 | 150 | 979090 | 0.833333 | 0.250000 |
| 303 | Mixed | B1 | same_person | 322 | 15 | 120 | 978843 | 0.955490 | 0.728507 |
| 303 | Mixed | B1 | duplicate_role | 100 | 10 | 100 | 979090 | 0.909091 | 0.500000 |
| 404 | Clean | B0 | same_person | 200 | 0 | 0 | 719200 | 1.000000 | 1.000000 |
| 404 | Clean | B0 | duplicate_role | 0 | 0 | 0 | 719400 | - | - |
| 404 | Clean | B1 | same_person | 200 | 0 | 0 | 719200 | 1.000000 | 1.000000 |
| 404 | Clean | B1 | duplicate_role | 0 | 0 | 0 | 719400 | - | - |
| 404 | Exact-repeat | B0 | same_person | 436 | 0 | 0 | 978864 | 1.000000 | 1.000000 |
| 404 | Exact-repeat | B0 | duplicate_role | 200 | 0 | 0 | 979100 | 1.000000 | 1.000000 |
| 404 | Exact-repeat | B1 | same_person | 436 | 0 | 0 | 978864 | 1.000000 | 1.000000 |
| 404 | Exact-repeat | B1 | duplicate_role | 200 | 0 | 0 | 979100 | 1.000000 | 1.000000 |
| 404 | Mixed | B0 | same_person | 262 | 14 | 174 | 978850 | 0.949275 | 0.600917 |
| 404 | Mixed | B0 | duplicate_role | 50 | 10 | 150 | 979090 | 0.833333 | 0.250000 |
| 404 | Mixed | B1 | same_person | 320 | 14 | 116 | 978850 | 0.958084 | 0.733945 |
| 404 | Mixed | B1 | duplicate_role | 100 | 10 | 100 | 979090 | 0.909091 | 0.500000 |
| 505 | Clean | B0 | same_person | 200 | 0 | 0 | 719200 | 1.000000 | 1.000000 |
| 505 | Clean | B0 | duplicate_role | 0 | 0 | 0 | 719400 | - | - |
| 505 | Clean | B1 | same_person | 200 | 0 | 0 | 719200 | 1.000000 | 1.000000 |
| 505 | Clean | B1 | duplicate_role | 0 | 0 | 0 | 719400 | - | - |
| 505 | Exact-repeat | B0 | same_person | 446 | 0 | 0 | 978854 | 1.000000 | 1.000000 |
| 505 | Exact-repeat | B0 | duplicate_role | 200 | 0 | 0 | 979100 | 1.000000 | 1.000000 |
| 505 | Exact-repeat | B1 | same_person | 446 | 0 | 0 | 978854 | 1.000000 | 1.000000 |
| 505 | Exact-repeat | B1 | duplicate_role | 200 | 0 | 0 | 979100 | 1.000000 | 1.000000 |
| 505 | Mixed | B0 | same_person | 261 | 25 | 185 | 978829 | 0.912587 | 0.585202 |
| 505 | Mixed | B0 | duplicate_role | 50 | 14 | 150 | 979086 | 0.781250 | 0.250000 |
| 505 | Mixed | B1 | same_person | 318 | 25 | 128 | 978829 | 0.927114 | 0.713004 |
| 505 | Mixed | B1 | duplicate_role | 100 | 14 | 100 | 979086 | 0.877193 | 0.500000 |

Mixed duplicate-role recall is25% for B0 and50% for B1 across all reserved seeds. B1 precision is90.91%,90.91%,87.72% for303/404/505 respectively, with10/10/14 false-positive pairs. Of the200 true duplicate-role pairs, B1 misses100 (the50 typo and50 missing-contact repeats); B0 additionally misses50 normalized repeats. Collision false positives vary because valid processor-role overlap varies by seed.

Duplicate-role false-positive rates are10/979100,10/979100,14/979100 (about0.001021%,0.001021%,0.001430%). Those small percentages are dominated by the large negative universe; they must not conceal the imperfect precision above. Same-person rates use their separately reported FP+TN denominators, not979100. Exact values and all rates are retained in private aggregate JSON.

Clean has no true or predicted duplicate-role pairs, so duplicate precision/recall are undefined. It does have200 legitimate same-person cross-role pairs. Exact-repeat success is limited to intentionally easy matching fields. None of these results establish cluster accuracy, resolved-person counts, real-world defect prevalence or safe automated merging.

## Field-quality results

For each Mixed seed and either method, the four-rule universe is1400*4=5600 event-rule cells. Micro counts: TP150,FP0,FN0,TN5450; precision/recall1. Missing contact contributes50 positives, name whitespace50 and contact whitespace50. Missing name contributes0 positives in generated evaluation data, so its precision/recall are undefined there. Each rule has1400 cells; the first three positive rules each have1350 true negatives, and missing name1400. Clean and Exact-repeat have no quality positives/predictions; rates with zero denominators are null.

This perfect quality result is intentionally narrow: the generator inserts the exact completeness/whitespace defects the explicit rules recognize. Missing-name and whitespace-only combinations are checked in manual fixtures, not empirical evidence about unseen defect families. Typos are not detected as completeness defects. Do not combine these scores with person/role matching scores.

## Scenario diagnostics and checks

The private aggregate output includes pair confusion counts by scenario for both relations and methods, plus per-rule quality counts. A scenario breakdown includes pairs with at least one endpoint in that stratum; the universe is k*(N-k)+k*(k-1)/2 for k stratum events. Breakdowns overlap and must not be summed. They retain collision and missed-repeat errors rather than filtering difficult cases out of the headline scores.

Python set intersections/differences independently reconcile TP/FP/FN exactly against SQLite truth self-joins and prediction joins, including each quality rule. TN is derived from the same documented universe, not claimed to be an independent enumeration. Validation and generation are shared. Manual fixtures independently establish expected counts, including three events yielding three positive pairs, valid dual roles, collisions and overlapping field labels. No normal approximation, sampling weight or confidence interval applies to this fixed synthetic exercise.

All104 tests passed in working and installed-wheel environments, including27 new tests/cases. Ruff passed with repository and isolated configuration. Packaged execution in the existing pinned reproduction environment produced complete JSON exactly equal to the working run, including code/configuration/input/truth hashes. Windows Python3.11.9 and SQLite3.45.1 were observed. No new GitHub/Linux CI result is claimed. No performance measurements were taken.

## Provenance and reproduction

- Code SHA256: `19210828bf5b041fcc6b8fc4b2ec732d80a1e7e24305ef8b6f17e631f4cd9a78`.
- Protocol SHA256: `14793ef68b126b457adb978999aa5ae9c320ca3e1806d89c089478ba4e6ecb19`.
- Unchanged lock SHA256: `113aff71a432584d77b77c2272b72f413ef1ed3f7fb1c8931cead83bee0b148b`.

Input/truth SHA256 values identify canonically submission-ID-sorted UTF-8 JSON arrays from dataclasses (sorted JSON keys, compact separators). Row-level data need not be distributed; deterministic regeneration recreates the observations and separate truth.

| Seed | Configuration | Observations SHA256 | Truth SHA256 |
|---|---|---|---|
| 303 | Clean | `14958fe5d082e7648349664713090c68b6d15b8ac852ecdfb4ff7097f448e0ea` | `dde8a1a41bee1c86f214e117d90a3d8758a472c73a9ce7cd901d0f40f76ffebb` |
| 303 | Exact-repeat | `080a3925af99bc6673755d23c1845d37e83c2fa38eaccfeb28ef6dc6c8123e0b` | `0834bde57e9df5b76d444c2e4c9910a7f0f422d3b6c5094541b346cc822c552d` |
| 303 | Mixed | `5afcb5658d8176cfd5d66d886931ff8f17f0f508efa552e61932f1ed6f78db0a` | `4d029718981c135dad611f0a8830cb7480db4da8545832b1f34c0b8884191c53` |
| 404 | Clean | `23a83b405baa0728a8aef8eaa0532599de68a7041bd6da7048067b218b57b52a` | `ff0f4ee61763c3eb36536332aca21fc81a90ae88a29d57e27c10024802a9f113` |
| 404 | Exact-repeat | `ce6291f1e9cd208bdce52b85cb24fcf2adaba8815a5f450faccd07a1742b7939` | `1e200cd97852db82b2fe9031a7bf5a54c5f6a247ac4b742bcee7d2c87da47d76` |
| 404 | Mixed | `e2a114d0d70c627f80e4ec77de1e5c1356152e80dc88ec76fa56e29872216caa` | `9cda4341ac3d6622a250457f4b8169298eb423b6367c4b655ec28048a88aa978` |
| 505 | Clean | `101ea0f07043488e6db87b0c72862cff43c855946dde837dde1328adbcf11e20` | `fc7341b94c8b8d944a63085aa6fa43fef343e9042c6bfb3e5530b178b9618c80` |
| 505 | Exact-repeat | `1d46363603681621293e4810bdd02be4ceedcab10a0f5fc0d0935be5a9e0b461` | `63caa7f674bf3e7b3ec60dda07acff3a815cb9ebcfe8d84f3f5e151a28417491` |
| 505 | Mixed | `befb44ad51c095ff8f431d506b95d00ba9fc7cb7b158bf06d32412a11f8e0873` | `213f7397e3d8fd9a9fc60b721b8cc9306c07f7b6f1666af15cef9d77f23e56b7` |

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_synthetic_quality.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m agrisight.synthetic_quality --phase development --output reports/private/m3_04_development.json
.\.venv\Scripts\python.exe -m agrisight.synthetic_quality --phase evaluation --output reports/private/m3_04_evaluation.json
```

The CLI accepts only outputs beneath ignored `reports/private` and writes aggregates, never row-level tokens or truth. Run from the repository root; reuse `requirements/e1.lock`. For installed-wheel reproduction follow [development instructions](../docs/DEVELOPMENT.md). No survey source is read. Existing application version0.0.1 remains a development package; model/contract/generator hashes distinguish experiments.

## Handoff

Next define M3-05's fixed workflow, exact event-count configurations, repeats, hardware, time/memory methods and failure handling before timing. Include55000 events as one workload, not a special capacity threshold. Full M3 stays open. Large matching-key collisions can cause quadratic candidate output even though negative pairs are not enumerated; this accuracy study does not establish scalability.

Learning checkpoint: finding two roles for one person is correct identity matching; calling that pair a repeated role would be incorrect. Missing an actual repeat and falsely joining different people are separate errors with different consequences.
