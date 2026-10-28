# Contributing and review protocol

1. Begin with `TASK.md` and the relevant design document; distinguish a learning exercise from deliverable acceptance.
2. State the change rationale, affected metric/source grain, trade-offs and test strategy.
3. Use a topic branch (`feat/m1-source-feasibility`, `docs/m0-kpis`, etc.), review code and documentation together.
4. Keep commits scoped; do not mix unverified performance claims into implementation.
5. Before a PR: run `python -m pytest -q` and `python -m ruff check src tests`; document environment and actual outcomes. Use the Python 3.11+ environment described in [development setup](DEVELOPMENT.md).
6. Add or revise checks for altered schema, metric denominator, null semantics, duplicate rules or geographic definitions.
7. Keep `MEMORY.md` factual and update the checklist only after evidence exists.
8. For demos and reports, visibly label synthetic outputs and cite permitted sources.

## Pull request checklist
- [ ] Relevant task/acceptance criteria linked
- [ ] No confidential data or secrets introduced
- [ ] Source/data provenance and licences documented where relevant
- [ ] Tests added or explicit reason for omission
- [ ] Tests executed and results recorded truthfully
- [ ] README/docs and milestone memory updated

## Evidence-based review changes

Make substantive changes for a demonstrated defect, meaningful risk or justified improvement against agreed objectives. Record rationale, expected benefit, trade-off and verification, following [review alignment](REVIEW_ALIGNMENT.md). Preserve historical results; mark superseded decisions explicitly rather than inventing retrospective evidence.

Candidate questions remain provisional until the source feasibility matrix supports them. Select and lock dependencies for the next analytical increment; do not install the future stack merely because it appears in the architecture. Before downloads, verify [local data protection](../data/README.md). No new CI infrastructure is required by the current review.
