# Contributing and review protocol

1. Begin with `TASK.md` and the relevant design document; distinguish a learning exercise from deliverable acceptance.
2. State the change rationale, affected metric/source grain, trade-offs and test strategy.
3. Use a topic branch (`feat/m1-synthetic-data`, `docs/m0-kpis`, etc.), review code and documentation together.
4. Keep commits scoped; do not mix unverified performance claims into implementation.
5. Before a PR: run `python -m pytest`; document environment and actual outcome. Also run format/lint after configured.
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
