# SS1 analytical and product review

Date2026-10-31. Owner requested proceeding after crop portfolio delivery. Scope: seed channels and overlap where supported; no broader redesign or unsupported variety rates.

## Evidence and decisions

Read current README/TASK/MEMORY and opportunity/previous model/UI/tests. Inspected released seed metadata and restricted field-level code/period diagnostics. Modern/traditional fields have observed0/1/missing values but no mapping labels; existing questionnaire Section4 lists three certification/variety options. Primary NBS variable/dictionary pages confirm labels/range without resolving that mapping. Therefore variety/certification rates remain an explicit gate, not a fabricated deliverable.

[SS1 contract](SEED_SOURCE_CONTRACT.md) specifies source codes0/1, type1 temporary records and exact period matching, household–crop grain, per-field denominators and complete-vector overlap. After raw combinations revealed small pooled cells, v1.1 conservatively defines six frequent named profiles plus a pooled residual before enabling the product. A rerun records the amended contract hash; exact analytical masks stay ignored. See [findings](../reports/SEED_SOURCE_FINDINGS.md).

The model independently reconciles Python counters with SQLite categories/combinations/counts and coverage. Its adapter validates identities, valid/excluded denominators, shares, unique masks, combination marginal bounds and core household totals, then projects only published groups. Optional absence/tampering affects only seed findings. Metadata includes crop/source labels only, no respondent IDs or locations. Seed-source quantities are not loaded or summed across units.

Agricultural Insights adds Sources / Source combinations, percentages/record counts, denominator/period/grain/exclusions, complete published table, overlap explanation and variety caveat. Exact combination labels say “only” to distinguish them from source marginals. Common bar rendering uses actual shares for percentage widths, preserving per-field denominators and existing water/crop charts. Geographic map meaning is unchanged.

## Validation record

Initial seed/water/crop targeted79 passed14.76s before additional residual/marginal tests. Tests cover manual0/1/no-vs-invalid2, overlapping sources, incomplete vectors, empty/missing cases, raw keys/parents/crop/type/period errors, duplicate/schema failures, independent SQL disagreement, aggregate/tampering/variety-claim rejection, disclosure grouping/suppression, CLI guards and UI controls/optional failure. Actual run and publication projection reviewed:349068 eligible temporary records,349046 complete/valid responses,22 missing per field,0invalid,119897 represented households,64981 excluded permanent records; no contradictions with household crop-yes coverage. Further executed checks follow below.

## Remaining work

Variety interpretations require release-specific mapping; the SS1 source deliverable does not close that gate. Seed channels do not establish certification, demand, affordability, quality or impacts. No raw/location drill-down or smaller geography. Conservative profile pooling is not a completed disclosure review. M6-04 privacy/permission/security/release-readiness and any new deployment remain open. Further land-tenure/travel questions need their own contract; no additional dataset is automatically introduced.

## Regression evidence

Full378 tests passed in development122.10s after adding explicit combination marginal-bound and residual-threshold tests (30 SS1 cases total). Ruff passed. Common percentage bars now use each row's verified share while count bars retain an explicitly labelled common scale, so differing source denominators cannot distort widths. Existing crop/water tests cover their unchanged defaults. Final installed-wheel/reproduction/browser results follow after execution; no unobserved CI status is inferred.

## Installed package and provenance evidence

Full378 tests passed in the noneditable installed-wheel environment131.58s, alongside development122.10s. Both pip checks passed. Complete SS1 JSON reproduces byte-for-byte, SHA256 `9af54e0919b399ad88f73aa3363aba3d38752087c1e26e173d45477025dfe69d`. Final wheel SHA256 `4bf06ee3cfb0a8f4cb8d2cae2c9bc388d423917709d21e76286218e3f8852f44`; model, adapter, presentation, SQL, minimal source/crop metadata and manifest verified in the wheel, including exact-profile ?only? labels. Current model/SQL/contract/metadata/lock hashes and document links checked. No application dependency changes. Original four survey/engineering artifacts plus SA1, GC1, IR1 and CP1 hashes remain unchanged.

## Final browser and local preview evidence

Final Chrome audit UTC `stakeholder-browser-20261031T001837Z`, local2026-10-31:22 checks passed across58 captures, desktop1440 x1000 and narrow390 x844;0 JavaScript exceptions; loopback request host only; no document/main horizontal overflow; both temporary ports closed; no cleanup notes. Keyboard checks exercise both seed modes/units, exact source values, combination values, denominators and visible variety gate, plus existing activity/crop/water/map/table/tooltip flows.

Inspected desktop sources/profiles and final narrow sources/profiles. Final profile labels explicitly say ?only,? denominators remain above charts, and longer combined-channel labels wrap on narrow screens. Published residual is11754; no raw rare mask/count pairs are projected. Screenshots/profiles stay ignored. Final fresh audit follows the exact-profile wording clarification and uses the final packaged source. No broader redesign was introduced.

The verified workspace preview was restarted hidden on loopback8501 with telemetry off; command-line guard and health200 observed; it intentionally remains running. Ruff, provenance/package/link checks and preservation of prior artifacts passed. No new deployment, survey redistribution or remote-CI result is claimed. Variety interpretation is not completed by this source increment and remains an unchecked TASK item.
