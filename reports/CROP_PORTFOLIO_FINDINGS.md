# Temporary crop portfolio CP1

Observed run2026-10-31. Source: the frozen owner-authorized NBS NASS2023 archive. [CP1 contract v1.1](../docs/CROP_PORTFOLIO_CONTRACT.md) defines this analysis before its first successful calculation. This is an **unweighted observed-roster description**, not national crop prevalence or production ranking.

## What is counted

| Measure | Count |
|---|---:|
| Household records checked | 143105 |
| Main-season plot parent records checked | 273887 |
| Crop records checked | 480393 |
| Eligible temporary crop records | 380464 |
| Excluded permanent/continuous records | 99929 |
| Excluded permanent records with unlabelled crop code3140 | 155 |
| Households with at least one eligible temporary record | 119909 |
| Distinct household–temporary-crop combinations | 349322 |
| Observed eligible crop categories | 43 |
| Main-season crop-yes households without a temporary record | 12950 |
| Temporary-roster households without a crop-yes response | 0 |

The denominator for portfolio shares and diversity is **119909 represented households**. It is not143105 total survey households or132859 main-season crop-yes households. The12950-household difference is a scope/coverage distinction; it must not automatically be called missing data, non-farming or permanent-only farming. No classification of its causes is established here. The main-season file is contextualized by April–October2022; permanent/continuous records are excluded rather than assigned that temporary-crop window.

Repeated household/crop appearances on different plots are legitimate records. Each household counts once for each recorded temporary crop, after validation of unique raw household/plot/crop keys. The349322 household–crop combinations differ from both380464 eligible raw rows and119909 distinct represented households.

## Most frequently recorded temporary categories

Chart subset: ten categories; the application table contains all43 observed categories.

| Released crop category | Distinct households | Share of represented households |
|---|---:|---:|
| MAIZE | 73779 | 61.53% |
| GUINEA CORN/SORGHUM | 42079 | 35.09% |
| BEANS/COWPEA | 35614 | 29.70% |
| RICE | 31975 | 26.67% |
| MILLET/MAIWA | 30508 | 25.44% |
| WHITE YAM | 25965 | 21.65% |
| GROUND NUT/PEANUTS | 25154 | 20.98% |
| SOYA BEANS | 12017 | 10.02% |
| COCOYAM | 9066 | 7.56% |
| OKRO | 8683 | 7.24% |

Households can occur in several categories. Percentages overlap and must not be summed as unique households. This table identifies frequent reported categories for crop-specific follow-up, not the largest producers, most profitable crops or seed demand. It does not establish which specific crop pairs co-occur.

## Recorded-category diversity

| Distinct temporary categories recorded per household | Households | Share |
|---|---:|---:|
| 1 | 22764 | 18.98% |
| 2 | 32799 | 27.35% |
| 3 | 29187 | 24.34% |
| 4 | 18350 | 15.30% |
| 5+ | 16809 | 14.02% |

These mutually exclusive bins sum to119909. Mean recorded category count is349322/119909 =2.9132258629460672 (display2.91). Crop categories preserve the released distinctions between variants such as yam types, and unspecified “other” is a reporting category, not an identified species. This is not botanical richness, complete farm diversification, resilience or a measure of income risk. It motivates asking whether crop-specific information/services should account for multiple recorded crops; actual needs must be investigated separately.

## Quality gate and honest amendment

The original v1.0 contract required a label for every crop code and the first run stopped with no portfolio output. A separate quality-only check found155 code3140 records without labels in this crop module, with complete type codes overall. Contract v1.1 was documented before rerunning: only unlabelled codes on excluded permanent records are permitted, with an explicit independently checked counter; any unlabelled temporary code still aborts. The successful run confirms all155 are outside the temporary subset. No crop name was borrowed from another module and no source values were repaired.

Actual validation checks archive identity, household periods and keys, plot keys/parents, raw crop keys/parents, exact field/type/category labels and allowed eligible codes. Python sets/counters and independent SQLite DISTINCT/GROUP BY calculations reconcile portfolio counts, bins, type/metadata counts, household–crop combinations and coverage flags exactly. Shared validated ID/code staging is disclosed. The optional adapter checks accounting, shares, category labels, diversity bounds/mean and core household/plot/participation totals. Source/model/SQL/contract/labels/lock hashes are recorded in ignored output and the reviewed manifest.

## Reproduction and limits

```powershell
.venv-m4/Scripts/python.exe -m agrisight.crop_portfolio data/raw/nass_2023/owner_download_2026-10-29/NASS_anonymized_dataset.zip --output reports/private/crop_portfolio_cp1.json
.venv-m4/Scripts/python.exe -m pytest -q
.venv-m4/Scripts/python.exe -m ruff check src tests scripts streamlit_app.py research_explorer_app.py
```

Microdata and aggregate JSON remain ignored. Only released crop-label metadata and code are packaged. No crop-by-geography filters, household identities, permanent-crop diversity, pooled seasons, yields, area estimates, causal claims or new deployment. The existing state map remains sample coverage. Disclosure and permission/release-readiness M6-04 remains open; this is not permission to redistribute the survey. See the [delivery review](../docs/CROP_PORTFOLIO_REVIEW.md) for observed tests, installed-wheel reproduction and browser evidence.
