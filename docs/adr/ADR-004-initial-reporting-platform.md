# ADR-004 - Initial reporting platform

Date: 2026-10-29. Status: **Selected for the local M4 prototype; dependency/adapter foundation verified, UI pending.**

## Decision and purpose

Use Streamlit for one local, read-only evidence explorer, governed by the [reporting contract](../M4_REPORTING_CONTRACT.md). The intended reader is an analyst or reviewer inspecting what the completed experiments establish. This is a proposed audience, not validated stakeholder demand.

The repository already contains Python analytical models and pytest checks. A Python presentation layer allows a small adapter and UI to reuse checked outputs without creating a second authoritative metrics implementation. Streamlit documents local Python-server/browser operation and headless AppTest support; both fit the planned local prototype and automated interaction checks.

Official references, checked 2026-10-29: [architecture](https://docs.streamlit.io/develop/concepts/architecture/architecture), [app testing](https://docs.streamlit.io/develop/api-reference/app-testing), [configuration](https://docs.streamlit.io/develop/api-reference/configuration/config.toml). These establish capabilities, not verified compatibility with a version not yet installed here.

## Alternatives and trade-offs

| Option | Project fit and disposition |
|---|---|
| Streamlit | Select for reuse of Python and a compact, testable local evidence explorer. Adds a runtime dependency/server and requires explicit state/loading tests. Not an operational authorization system |
| Power BI | Retain for a future distinct BI audience or learning deliverable. A second reporting implementation now adds reconciliation/maintenance work without a demonstrated additional use case |
| Static Markdown | Retain as the reviewed findings baseline. It already communicates evidence, but cannot demonstrate controlled selections and corresponding denominator/provenance changes |
| Custom frontend/service | Defer: current aggregate navigation does not justify another stack, API or persistence layer |

No claim is made that one product is generally faster, cheaper or better. The decision concerns this repository's existing outputs, learning goal and minimal-architecture rule.

## Implementation gates and consequences

- Select a compatible Streamlit version and lock its dependency graph before UI implementation. Reproduce installation in a clean Python3.11+ environment and run regression checks; preserve analytical locks/results rather than silently upgrading them.
- Keep validation/adaptation independent of Streamlit. UI consumes an allow-listed aggregate reporting bundle; it does not read survey microdata, generate experiments, execute arbitrary SQL or rerun benchmarks on interaction.
- Bind the initial server to loopback, disable optional usage telemetry and avoid remote assets. Verify configuration against the selected version. No hosting account, public endpoint, external analytics or deployment is included.
- Test selection changes, source labels, denominator visibility, undefined values and unavailable/corrupt input states with AppTest and pure-Python adapter tests. Run a local server smoke check; headless tests alone do not demonstrate browser usability.
- Keep charts secondary to clearly labelled values and evidence tables. Display-only selectors cannot imply unsupported geographic or demographic analysis.

Revisit the platform if stakeholder requirements, distribution needs or maintainability evidence justify a change. Adding Power BI later requires a distinct purpose and reconciliation against the same reporting contract.

Implementation follow-up: [M4-02 verification](../M4_ADAPTER_REVIEW.md) records Streamlit1.66.1 installation, lock reproduction, adapter/schema and SDK smoke. The gates above remain requirements for the UI, not claims that the interface is implemented.
