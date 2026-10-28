# AgriSight project charter

Updated: 2026-10-28. Working direction after the project review; M0 remains a completed design foundation. This is not evidence of user interviews, empirical findings or production readiness.

## Purpose

AgriSight combines two connected objectives:

1. **Empirical agricultural intelligence:** investigate authorized Nigerian agricultural data, estimate defensible indicators, assess uncertainty and communicate findings relevant to decisions.
2. **Trustworthy analytics delivery:** demonstrate reproducible pipelines, SQL modelling, data quality, statistical reasoning, privacy-aware geography and interactive reporting.

Research determines what the data support. Engineering makes those conclusions reproducible and useful. The first checked agricultural result is an initial complete workflow, not the full project's exit criterion.

## Scope and evidence boundaries

Real survey analysis is primary. Separate synthetic registration experiments provide known truth for counting, defect detection, duplicate evaluation and scale testing. The 55,000-role target is an engineering workload, not a real registry or population finding. Never pool these populations.

In scope: documented source selection, analytical contracts, survey-aware methods, independent SQL/Python checks, reproducible transformations, supported geographic summaries and tested reporting. PostgreSQL/dbt and dashboard capabilities remain learning goals whose introduction requires a concrete need.

Out of scope: real farmer enrollment, client-system reproduction, confidential client materials, identifying locations, unsupported small-area estimates, causal claims from descriptive associations and public release without owner authorization.

## Candidate research questions

Provisional until the [feasibility matrix](RESEARCH_FEASIBILITY.md) establishes suitable variables, permissions and survey design:

- **RQ1:** How does participation in selected agricultural activities vary across statistically supported geographic domains?
- **RQ2:** How does access to selected agricultural inputs or services differ across defined farming groups?
- **RQ3:** How sensitive are those findings to missing data, eligibility rules and reasonable analytical assumptions?

## Users and engineering questions

Proposed users, not interview-validated personas: programme managers interpreting patterns; analysts tracing estimates; data administrators reviewing quality; governance reviewers checking disclosure. Supervisors and registry reviewers belong to the synthetic operational demonstration.

Engineering questions: Do transformations preserve grain and reconcile? Can controls detect labelled defects without excessive false positives? Do dashboards preserve denominators and disclosure rules? How does performance change across documented input sizes?

## Acceptance

- E1 establishes suitability; E2 produces checked agricultural findings; E3 tests sensitivity. See the [investigation plan](M1_EXPERIMENT_PLAN.md).
- Every indicator defines unit, population, denominator, reference period, exclusions, null semantics, weight and uncertainty method.
- Every result has source/version provenance, reproducible commands, independent checks and limitations.
- Reports expose provenance, missingness, scope and supported geography; synthetic outputs are explicitly labelled.
- Engineering benchmarks report known truth, false positives, hardware, input size and repeat conditions where applicable.
- Real user validation and explicit publication authorization remain future gates. See [M0 review](M0_REVIEW.md) for historical foundation evidence.
