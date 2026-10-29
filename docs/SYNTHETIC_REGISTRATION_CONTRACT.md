# Synthetic registration experiment contract v1.0

Specified 2026-10-29, before M3-04 implementation or evaluation. **SYNTHETIC DEMONSTRATION DATA.** These are experimental assumptions, not approved field-registration rules. No survey records or real identities are inputs.

## Grain, keys and partitions

One observation is an immutable role-submission event. A person may legitimately submit both farmer and processor roles. A repeated submission for the same intended role is a duplicate event; multiple roles are not duplicates. Revision history and multiple programme enrollments are outside this initial single-programme snapshot.

| Table | Fields and contract |
|---|---|
| Detector observations | `submission_id`: unique nonblank string; `name_token`: artificial text or null; `contact_token`: artificial text or null; `role_kind`: farmer/processor; `status`: pending/accepted/rejected |
| Evaluator truth | `submission_id` foreign key; `true_person_id`: generated identity; `true_role_id`: intended role identity; `scenario`: generation stratum; `defect_labels`: zero or more named field defects |
| Run manifest | contract/generator versions, seed, configuration, ordered-input SHA256, truth SHA256, code/lock hashes and synthetic source label |

Truth IDs are stable within one generated dataset; they carry no cross-run identity guarantee. Submission IDs identify events, not people, and must not encode person or role truth. Canonically sort outputs by submission ID for hashing. Use UTF-8 JSON with explicit nulls; no NaN, implicit type coercion or blank-as-null ambiguity. Leading/trailing whitespace in observable tokens can deliberately be a labelled defect.

Truth is stored separately and joined only by the evaluator after predictions. The detector receives only observations; it cannot use truth IDs, labels, scenario, seed, generation order or configuration. Unique submission IDs are transport requirements: duplicate/missing IDs abort evaluation rather than becoming ordinary person-matching positives. Broken truth references, conflicting roles within a true role, or missing truth also abort.

No crops or coordinates are needed for this experiment. Spatial reference and coordinate precision are not applicable. Tokens must visibly be fictional (for example `SYN-NAME-...` and `SYN-CONTACT-...`), never real names, telephone numbers, emails, client identifiers or values sampled from survey records. Null means unknown, never a shared matching identity. Synthetic statuses do not establish real acceptance qualifications, and incompleteness does not automatically change status.

Row-level datasets and predictions belong under ignored `data/synthetic/` or `reports/private/`; reviewed small fixtures may live in tests. Raw generated observations remain immutable. Store flags/pair predictions separately; never merge people, delete submissions or overwrite defects automatically. This is local evaluation with no production access-control claim, external service or row-level public release.

## Ground-truth relations

Evaluate unordered distinct submission pairs, represented as sorted submission-ID tuples:

1. **Same person:** equal `true_person_id`, including valid cross-role pairs.
2. **Duplicate role submission:** equal `true_role_id`. Each true role belongs to exactly one person and kind. A person has at most one intended role per kind in this snapshot.

Three events for one true role create three positive duplicate pairs, not two. Report pair counts alongside distinct people, intended roles and event counts. Do not interpret pair recall as cluster quality, resolved identities or corrected KPI counts.

Field-defect truth is a set of `(submission_id, rule_name)` labels. Initial rules are missing name, missing contact, surrounding name whitespace and surrounding contact whitespace. Null name/contact are experimental completeness defects; their presence does not imply rejected registration. Unknown enums/types are schema failures tested separately. Matching ambiguity is not a field defect.

See the [pre-specified evaluation protocol](experiments/M3_04_PROTOCOL.md). Changes to these assumptions require a versioned amendment before the corresponding evaluation.
