# Water-management findings IR1

Observed run: 2026-10-31, using the owner-authorized NBS NASS2023 archive. The [IR1 contract](../docs/IRRIGATION_CONTRACT.md) was specified before calculation. These are **unweighted observed plot records**, not population estimates, actual-use measurements or unmet-demand estimates. Main-season reference: April–October2022.

## Infrastructure presence

| Response | Plot records | Share of valid responses |
|---|---:|---:|
| Yes | 11268 | 4.11% |
| No | 262619 | 95.89% |
| Missing | 0 | Excluded |
| Invalid | 0 | Excluded |

Input273887; valid yes/no denominator273887. All main-season roster plot types are included: cultivated conventional plots, temporarily fallow conventional plots and kitchen gardens. Counts agree with prior E1 evidence and the core SA1 roster total. They do not count unique households or farmers.

Supported observation: infrastructure is reported on a small share of this released plot roster. Further investigation could verify the type, condition and functionality of recorded infrastructure. A no response does not prove a plot is rain-fed, needs irrigation or would benefit from an irrigation investment. Crop-level irrigation use is a separate unanalysed measure.

## Main methods among infrastructure-yes plots

| Released main-method category | Plots | Share of valid eligible responses |
|---|---:|---:|
| Surface irrigation (flooding, furrows) | 8617 | 76.47% |
| Sprinkler irrigation | 1155 | 10.25% |
| Drip irrigation | 661 | 5.87% |
| Spray or microsprinkler irrigation | 274 | 2.43% |
| Bubbler irrigation | 40 | 0.35% |
| Equipped wetland and inland valley bottoms | 172 | 1.53% |
| Equipped flood recession cultivation | 112 | 0.99% |
| Spate irrigation | 13 | 0.12% |
| Other | 224 | 1.99% |

Eligible11268; valid11268; missing0; invalid0. The262619 infrastructure-no records have no populated method response, matching the expected skip. Code8 follows the released value label; the previously documented questionnaire-version discrepancy remains visible in the contract. These are single **main** methods, not all methods used or evidence of their efficiency. Rounded shares need not sum to exactly100%.

Surface irrigation is the largest recorded category in the eligible sample. This can focus further questions about how reported systems operate and what information is missing; it does not establish that surface irrigation causes lower/higher performance or should be replaced by another method.

## Main water sources among infrastructure-yes plots

| Released main-source category | Plots | Share of valid eligible responses |
|---|---:|---:|
| On-farm ground water | 6313 | 56.03% |
| On-farm surface water | 1899 | 16.85% |
| Off-farm surface water (lakes, rivers, watercourses) | 1819 | 16.14% |
| Municipal water supply or other water network | 563 | 5.00% |
| Treated waste water | 81 | 0.72% |
| Reservoir (used to avoid flooding) | 495 | 4.39% |
| Other | 98 | 0.87% |

Eligible11268; valid11268; missing0; invalid0. Again262619 infrastructure-no records are correctly skipped, with zero populated source fields. On-farm groundwater is the largest reported main-source category. This motivates follow-up about the recorded source and reliability, not a conclusion about groundwater availability, depletion, sustainability or water quality. No water volumes, reliability measures or hydrological assessments are derived.

## Validation and exclusions

The actual run checks the frozen archive hash; household uniqueness and period values; plot keys, parent relationships and roster types; exact question and value labels. Independent Python counters and SQLite groupings reconcile infrastructure counts, eligible category frequencies and populated-outside-yes flags exactly. Shared ID/code staging is disclosed. No records were changed, imputed or silently dropped. Method/source percentages each divide by their own valid eligible response denominator, not all273887 plots.

The dashboard exposes only these pooled aggregates. It has no irrigation geographic filters, household locations or linked small-area drill-down. The spate category has13 records across the whole pooled release; this is not a cell located to a state/community, and no identifying fields accompany it. The separate geographic map retains its conservative regional suppression rule. These local presentation choices are not a completed disclosure audit or permission to redistribute the microdata; M6-04 remains open.

The new artifact and raw source remain ignored. The map remains household sample coverage only. No national inference, confidence intervals, seasonal comparison, programme impact, geographic priority ranking or broader website redesign is introduced.

## Reproduce

```powershell
.venv-m4/Scripts/python.exe -m agrisight.irrigation data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/irrigation_ir1.json
.venv-m4/Scripts/python.exe -m pytest -q
.venv-m4/Scripts/python.exe -m ruff check src tests scripts streamlit_app.py research_explorer_app.py
```

Artifact source/model/SQL/contract/lock hashes and execution versions are recorded. The optional irrigation adapter pins reviewed bytes, checks arithmetic and compares the roster total with the core bundle; missing/changed/inconsistent irrigation evidence hides only Water Management findings. See the [delivery review](../docs/IRRIGATION_REVIEW.md) for observed package, test and browser evidence. Reproduction does not authorize automatic repinning of changed inputs or public hosting.
