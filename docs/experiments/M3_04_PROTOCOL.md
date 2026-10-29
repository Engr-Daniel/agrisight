# M3-04: synthetic quality and duplicate evaluation protocol v1.0

Specified 2026-10-29. **Planned, not executed. SYNTHETIC DEMONSTRATION DATA.** This protocol addresses engineering accuracy, not agricultural prevalence. M3-04 and M3-05 remain unchecked until their evidence exists.

## Question and fixed baselines

Can simple explicit rules identify incomplete fields and repeated role submissions while preserving legitimate multiple roles and avoiding identity collisions? Use the [registration contract](../SYNTHETIC_REGISTRATION_CONTRACT.md), existing Python/SQLite tooling and current dependency lock. No fuzzy-matching package or new service is needed for the first baseline.

Freeze two person-matching baselines before evaluation:

- B0: exact non-null, nonblank raw name and contact agreement.
- B1: strip surrounding whitespace and casefold both tokens, then require both normalized nonempty tokens to agree. No punctuation removal, approximate distance or contact-only match.

Generate candidate pairs by grouping on the observable matching key. Null/empty keys generate no candidates. Duplicate-role predictions are predicted same-person pairs additionally having equal observed role kind. Status never filters matching: pending/accepted/rejected events remain in scope. Predictions are review flags, never automatic merges.

Evaluate field rules independently: missing/null or whitespace-only name/contact, and surrounding whitespace on non-null name/contact. A whitespace-only field may correctly receive both labels. Case variation alone is not a quality defect. A misspelled but nonblank token can cause matching failure without being detectable by these completeness rules.

## Fixtures and generated scenarios

First create manually calculable fixtures: one person/two legitimate roles; two same-role repeat events; three repeat events (three pairs); different people with identical names but distinct contacts; shared contacts but distinct names; different people sharing both tokens; same-person case/whitespace variants; typo variants; absent contacts; mixed statuses; empty input; no positive pairs; no predicted pairs. Include schema/key failures and row-order invariance.

Then implement a seeded generator with separately stored truth. Begin with one intended farmer role per person; assign processor roles to a configured fraction. Repeat submissions refer to an existing intended role. Randomize opaque submission-ID assignment and observation order independently of truth. Validate generated truth before evaluation.

Freeze initial development seeds101/202 and evaluation seeds303/404/505. Each accuracy dataset starts with1000 people. Configurations below are synthetic stress settings, not estimated real-world rates. Fractions are applied to documented disjoint person strata using floor counts, with assignment shuffled by the seeded generator; repeated events are additional rows. Record actual stratum/event/pair counts, including cross-role effects, rather than inferring denominators from nominal rates.

| Configuration | Dual-role people | People with one extra farmer submission | Stress allocation among repeat people |
|---|---:|---:|---|
| Clean | 20% | 0% | None |
| Exact-repeat | 20% | 20% | All repeats identical in matching fields |
| Mixed | 20% | 20% | 25% whitespace/case variants,25% name typo,25% missing contact,25% exact |

For Mixed, additionally select disjoint non-repeat person groups:20 pairs share names only,20 pairs share contacts only,10 pairs share both tokens. Keep their truth identities distinct. Apply equivalent changes across each person's legitimate roles; only repeated events receive repeat-specific perturbations. Spell out exact mutation and sampling order in the generator configuration before running evaluation; amend protocol if feasibility forces any change. A generated all-clean scenario is insufficient evidence by itself.

Develop/debug against hand fixtures and development seeds. Freeze detector code/configuration hashes before first evaluation-seed run. Do not tune thresholds or scenarios after seeing held-out scores and still call the same runs held out. A changed method needs a versioned protocol and fresh evaluation seeds. No target precision/recall is imposed to force a favourable result: low scores are reportable findings.

## Metrics and independent checks

For each relation and baseline, evaluate all unordered event pairs as the conceptual universe, even when blocking emits only a few candidates. Compute true positives (TP), false positives (FP), false negatives (FN) and true negatives (TN). Truth-positive pairs missed by blocking remain FN. Derive total pairs as N*(N-1)/2 and TN as total minus TP/FP/FN; do not materialize every negative pair.

- Precision = TP/(TP+FP), null if no predictions.
- Recall = TP/(TP+FN), null if no true positives exist.
- False-positive rate = FP/(FP+TN), null if there are no true negatives.
- Report FP count and predicted/true pair denominators even when a rate rounds to zero.

For quality rules, the universe is all events crossed with the four named rules. Report each rule's confusion counts/precision/recall plus micro totals. Do not combine field-rule and identity metrics into one accuracy percentage. Report same-person and duplicate-role results separately and include error counts by predeclared scenario; subgroup denominators may overlap for pair endpoints and must be stated.

Independently reconcile Python set-based counts against SQLite truth/prediction joins using exact integer agreement. Both implementations must match manual fixture truth, not merely one another. SQL truth self-joins must use canonical pair ordering, preventing double counts and self-pairs. Rates agree within absolute1e-12; undefined rates remain null. Share schema validation openly; independent aggregation does not mean independent generation.

## Acceptance and next handoff

M3-04 is complete only after generator/contract invariants, manual positive/negative/edge fixtures, targeted and regression tests, held-out execution, independent SQL reconciliation, deterministic reproduction and reviewed aggregate findings exist. Record commands, seeds/configuration, input/truth/code hashes, actual metrics and limitations. Preserve unsuccessful and collision cases; no performance or production-readiness claim follows from accuracy fixtures.

M3-05 remains a separate future protocol: benchmark a fixed validated workflow at multiple sizes including55000 role-event entries, with repeats, hardware/software, timing variability, memory methodology and failures. Distinguish intended roles from additional duplicate events in workload counts. Avoid an all-pairs negative enumeration; disclose candidate-group explosion when tokens collide. Do not run a timing study before fixing what work is timed.

Learning checkpoint: if two different people share both tokens, B0/B1 can falsely link them; if one person mistypes a name, both may miss the link. Perfect scores on exact repeats would therefore demonstrate only a narrow capability.

## Implementation clarification before execution — 2026-10-29

Sampling order is fixed as follows: shuffle people to choose200 repeat people (none for Clean); independently shuffle people to choose200 dual-role people (dual-role membership may overlap other strata). For Mixed, shuffle the800 non-repeat people and consume40/40/20 people in adjacent pairs for name-only/contact-only/both-token collisions. Partition the shuffled repeat list into consecutive groups of50 for whitespace/case, typo, missing-contact and exact repeats. Whitespace/case mutation wraps both lowercased tokens in one space; typo appends `-TYPO` to the name only. Missing contact is null on the repeat only. Names/contacts initially use visibly fictional indexed tokens. Independently seeded RNG streams control opaque event-ID assignment and row shuffling; statuses cycle over the three allowed values. Collision strata are disjoint from repeat strata; dual-role membership is independently selected. Thus the earlier phrase “disjoint person strata” applies to collision/repeat stress assignment, not dual-role membership.

Scenario pair breakdowns use pairs having at least one endpoint in the named stratum, with universe k*(N-k)+k*(k-1)/2 for k stratum events. The same pair can appear in multiple scenario breakdowns; do not sum those breakdowns. Main results use the full pair universe exactly once.
