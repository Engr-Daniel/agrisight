# Real-data investigation plan: E1 → E2 → E3

Updated: 2026-10-29. **M1 E1 baseline and the first M2 E2 workflow are complete; E3 remains planned.** See [M1 review](M1_REVIEW.md), [M2 review](M2_REVIEW.md), [E1 protocols](experiments/E1_PROTOCOL.md) and [E2 findings](../reports/E2_AGRICULTURAL_FINDINGS.md). Not all 21 modules are analytically certified. Population/time/quantity restrictions remain binding. These are observational investigations, not controlled experiments or impact evaluations.

## Source and question gate

Use the [feasibility decisions](RESEARCH_FEASIBILITY.md). NASS is selected for the first sample descriptive workflow under [NASS-01](NASS_INDICATOR_CONTRACT.md); GHS remains a separately gated alternative for service-access questions. The following sequence records the original gates, now assessed in the technical review; it is not evidence that every possible indicator is supported.

1. Inspect relevant questionnaires, codebooks, methods, reference periods and access/redistribution terms. Record study/release and evidence locations.
2. Map variables, units, keys, join cardinality, eligibility/skip codes, supported domains, weights and variance-design information to questions. Mark supported, narrowed, deferred or unsupported with reasons.
3. Select the first feasible indicator and finalize its analytical contract; do not promise population estimates if design information is insufficient.
4. Select and lock dependencies for the chosen files/methods. Verify a Python 3.11+ clean environment and existing tests/lint; no need to install the future stack now.

## E1 — Data suitability and profiling (M1)

Question: What is the structure, completeness and internal consistency of the authorized source, and which analyses can it support?

- Acquire only permitted files into ignored `data/raw/<source>/<release>/`. Record filename, version, download date, SHA256 and actual access terms in a non-identifying manifest. Preserve raw files; local storage is not permission to redistribute.
- Keep intermediate and curated row-level outputs in ignored directories described in [data storage](../data/README.md).
- Inspect rows/types, keys, join multiplicity, categories, coded missingness, ranges and rule violations. Distinguish legitimate repeated observations/skips from defects. Flag unusual values for review, not automatic deletion.
- Define source-specific rules from documentation. Cross-check at least three baseline summaries independently in code/SQL; specify numeric tolerances.

Deliverables: source card under `docs/data_sources/`, populated feasibility matrix, finalized protocol under `docs/experiments/`, reproducible scripts/tests, and `reports/E1_REAL_DATA_PROFILING.md` with observed findings and limits. Create these only when supporting work exists.

Exit: documented access, hashes, units/keys/design, reviewed indicator definitions, verified profiling results and reproducible commands. Missing design information is a blocker or explicit scope restriction.

## E2 — Agricultural pattern analysis (M2)

Executed first workflow: NASS-01 under its [contract](NASS_INDICATOR_CONTRACT.md) and [pre-specified E2 protocol](experiments/E2_PROTOCOL.md). Implementation and limits are assessed in [M2 review](M2_REVIEW.md); the remaining text describes the general method, not approval for additional indicators.

Compute selected RQ1/RQ2 indicators with explicit population, denominator, eligibility, period and missingness. Identify the correct weight for each estimand; weights alone do not establish a valid confidence interval. Verify design-aware uncertainty methods before population inference, including supported domains and small-domain limitations. Otherwise restrict claims to labelled sample descriptions.

Deliverables: versioned SQL/Python transformations and contracts, independent reconciliations, estimates with sample counts/uncertainty where justified, and a reproducible agricultural findings report. Introduce PostgreSQL/dbt through the architecture gates. No causal claims from descriptive associations.

## E3 — Robustness and sensitivity (M3)

Pre-specify plausible alternatives for missingness, eligibility/exclusions and definitions. Compare against E2 and report stability without selecting assumptions to support a preferred finding. Unknown is not automatically zero/no; do not impute or discard without a rationale.

Deliverables: reproducible sensitivity comparisons, explanations of material changes, limitations and reporting recommendations.

## Separate supporting engineering investigations

Seeded synthetic records provide known truth for defect/duplicate evaluation and workload tests, including 55k role entries and other sizes. Report precision, recall, false positives and measured performance with conditions. Never pool simulated people with survey respondents. Interactive reporting follows checked findings; the first report is an increment toward the full platform.
