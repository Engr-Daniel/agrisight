# M0-01 — Stakeholder questions and decision catalogue
Status: drafted / awaiting owner review. Date: 2026-10-26.

## Principle
A dashboard has value only when its users can take an appropriate, documented action based on a trustworthy indicator. These are **proposed use cases**, not interviews with real end users.

| ID | Persona | Decision question | Required indicator | Decision/action | Uncertainty/constraint | Acceptance example |
|---|---|---|---|---|---|---|
| D01 | Programme manager | How many accepted farmer-role and processor-role entries are registered? | Count by actor role and period | Compare registration progress with a *synthetic* goal | Dual-role people cannot be double-counted as distinct persons | Fixture: 1 farmer+processor person yields 2 roles, 1 person |
| D02 | Programme manager | Which approved geographic areas have the lowest completion against an assigned target? | Accepted roles / assigned synthetic target | Review allocation | An unregistered resident is not measured | Explicit zero-target handling |
| D03 | Field supervisor | Where are incomplete submissions clustering? | Applicable required fields present / applicable fields | Prioritize revisits | Valid skip logic must be excluded | A skipped non-applicable question is not missing |
| D04 | Field supervisor | Which batches display unusual submission patterns? | Quality flags, duration distributions, volume per enumerator | Investigate without presuming misconduct | A flag is not proof of fraud | Flag traces to batch and rule |
| D05 | Data quality lead | Which records are probable duplicates? | Candidate pair count, precision/recall on synthetic truth | Human verification | Similar names alone do not justify deletion | Ambiguous pair remains pending |
| D06 | Data quality lead | Are reported farm/enterprise coordinates consistent with permitted area? | Invalid/missing/implausible coordinate counts | Correct location or mark unverifiable | Consent restrictions and coordinate precision | No coordinates for refusal; synthetic coordinates labelled |
| D07 | Operations manager | Which commodities and processing services are represented? | Role-commodity counts with explicit many-to-many joins | Plan service categories | Do not add category sums as distinct persons | Multi-crop farmer counted once in unique-person total |
| D08 | Management | How recently were reports refreshed and validated? | Last ingestion, last quality pass, model version | Delay decisions based on stale data | Refresh success != accuracy | UI exposes timestamp and status |
| D09 | Analyst | Can each KPI be traced back to source and filter logic? | Metric definitions, SQL lineage and test fixtures | Challenge assumptions | Public survey design != operational registry grain | SQL/Python fixture reconciliation |
| D10 | Data protection lead | Can drill-down reveal sensitive or disclosive observations? | Aggregation disclosure checks and permissions | Suppress unsafe report | Synthetic does not mean privacy is irrelevant | Small-count drilldown blocked by rule |

## Demo user journeys
1. Supervisor selects an area → identifies unexpected missing data → drills into **synthetic, non-identifying** batch quality → records a review action.
2. Manager selects commodity and period → sees registered role counts vs distinct persons → understands limits of derived service needs.
3. Analyst reviews a chart → retrieves formula, denominator, data version and last quality status.
4. Governance reviewer tests small geographic segment → dashboard suppresses disclosive output, with rationale.

## Initial design priority
P0: D01, D03, D05, D09, D10.
P1: D02, D04, D06, D08.
P2: D07; expand as datasets support.

## Learning check
Explain why 55,000 actor-role registrations might correspond to fewer than 55,000 distinct people, and why a household-sample survey cannot be combined directly with synthetic registrations.
