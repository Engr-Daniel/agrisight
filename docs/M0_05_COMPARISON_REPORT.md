# M0-05 — Matched validation case comparison

Status: implementation committed; execution evidence to be appended after GitHub Actions completes.

> Historical status above is superseded by the execution evidence recorded in [ADR-003](adr/ADR-003-validation-choice.md) and [M0 review](M0_REVIEW.md). Pandera is the working initial choice. No new framework run or performance benchmark is claimed by this clarification.

## Objective
Compare Pandera and Great Expectations (GX Core) on **seven synthetic registration scenarios** using the same accepted/rejected outcome criterion.

| Scenario | Expected |
|---|---|
| Two valid roles for one person | Accept |
| Empty person ID | Reject |
| Empty role ID | Reject |
| Invalid role category | Reject |
| Invalid registration status | Reject |
| Integer instead of boolean | Reject |
| Duplicated role key | Reject |

Each test case begins with two nonidentifying synthetic rows; the comparison is **not** a speed benchmark, a statistical experiment or evidence of successful field deployment.

Both implementations check nonblank strings, category sets, unique role identifiers, and a strict boolean field. Pandera uses a DataFrame schema; GX Core uses explicit expectations against a Pandas batch. Results and actual package versions are printed in the workflow log.

**Important limitations:**
- Pandas dtype coercion/inference influences the `complete` column in this small example. Later test nullable, mixed-dtype and missing-column behavior.
- Matching pass/fail outcomes does **not** imply identical error reporting, performance or production features.
- Errors are not yet reconciled by rule/code, only by scenario.
- Null treatment and whitespace handling deserve dedicated parity tests.

## Run
`python -m agrisight.framework_comparison` using the optional research dependencies installed by `.github/workflows/framework-comparison.yml`.

## Decision status
Provisional Pandera-first recommendation remains. Choose a primary framework after reviewing observed outcomes, developer ergonomics and maintainability. GX can still serve monitoring needs later if justified.
