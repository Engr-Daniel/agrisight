# E3 readiness assessment — no substantive robustness result yet

Observed 2026-10-29. Source is the previously executed NASS-01 aggregate artifact, not modified or newly simulated survey records. See [pre-specified E3 protocol](../docs/experiments/E3_PROTOCOL.md).

## Limited NASS-01 result

The baseline has 143105 input/eligible records, numerator132859 and zero missing/invalid/excluded responses. The protocol's executable aggregate audit reconciled the arithmetic with SQLite at absolute tolerance1e-12:

| Check | Observed |
|---|---:|
| Valid-response versus all-record denominator difference | 0 |
| Unknown-response lower/upper range width | 0 |
| Baseline sample proportion | 0.9284022221445791 |

These equalities are expected because there are no excluded responses. They identify **no missing-response-driven variation in this snapshot**. They do not test response accuracy, omitted households, unverified design, measurement error or population representativeness. SQL/Python/order/rounding checks remain software/presentation checks, not substantive sensitivity evidence. An all-record analysis would not generally have the same target as a valid-responder description if excluded responses existed; this protocol refuses that changed case.

No missingness was injected, no weights applied, no households bootstrapped and no survey records altered. Machine audit output is ignored `reports/private/e3_readiness.json`, with source archive and consumed E2-result hashes. No new application module, dependency, test suite or CI workflow is needed to establish these arithmetic equalities.

## Recommended next investigation

**Conditional recommendation: bounds for the median released main-season plot-area field.** There are 48 missing areas in E1, so unknown values could affect a fixed full-roster median. Order-statistic bounds can quantify that uncertainty without imposing arbitrary imputed values or a maximum area. These are bounds from missing observations in the sample, not population confidence intervals.

The observed-area median and the target full-roster median are explicitly different quantities; the protocol does not disguise switching between them as the same estimand. It proposes bounding the latter while showing the former as a labelled reference.

This remains a proposal. The [released plot dictionary](https://microdata.worldbank.org/catalog/8194/data-dictionary/F16?file_name=3_Plot_mainSeason) labels `s02_q16a` in square metres and provides `areaAcresPlot`; questionnaire PDF p.16 distinguishes farmer estimates/units and GPS measurement. That evidence does not yet establish the derivation of the released field. Verify units, measurement/derivation status, eligible plot types and structural non-applicability before calculation. Do not claim it measures total farm size or certified GPS area.

Crop/livestock co-occurrence is another useful descriptive question but not inherently a sensitivity study. Input-type quantities have genuine missingness but need roster/unit review before use. These alternatives and their gates are recorded in the protocol; no numeric result for a successor indicator has been produced.

## Decision

M3 has started; it is **not complete**. Finalize the next indicator contract and executable E3 method after the area feasibility gate, then run independent Python/SQL bounds with known-truth edge tests and report numerical sensitivity without inventing a “robust” threshold. Synthetic registry matching/quality and 55k scale experiments remain separate, unexecuted M3 tasks.
