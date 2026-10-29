# NASS-01 — Main-season crop participation in the observed sample

Contract v1.0, 2026-10-29. Selected after E1 suitability review. Authoritative definition for the first M2 sample indicator; no population estimate is approved.

| Property | Definition |
|---|---|
| Purpose | Describe recorded main-season crop participation before expanding reporting |
| Source | Owner-supplied NASS ZIP frozen by SHA256 in the acquisition inventory |
| Input/grain | `1_households.dta`; one released agricultural-household record per `hhid` |
| Population of description | Recorded agricultural households in this released sample, not all Nigerian households or farmers |
| Period | Released `mainAgSeason`: April–October 2022; retain survey title NASS 2023 separately |
| Response | `s00_q15a`: 1=yes; 2=no; verified labels in actual file |
| Numerator | Distinct complete-key household records with response 1 |
| Denominator | Distinct complete-key household records with response 1 or 2 |
| Missing/invalid | Report missing/other counts separately; exclude them from denominator, never change them to no |
| Keys | `hhid` must be complete and unique before calculation; halt if duplicate/missing key, rather than dropping or choosing a record |
| Zero denominator | Undefined/null, not 0% |
| Weight/uncertainty | Unweighted sample proportion only; no population CI or statistical significance claim |
| Geography | First output pooled sample only; no local prevalence or causal comparisons |
| Joins | None required; any later plot join must preserve household grain and undergo reconciliation |
| Freshness | Historical 2022/2023 study; acquisition 2026-10-29, not current field conditions |
| Access | Owner-authorized local statistical research, aggregate outputs only; restrictions and publication obligations in source card |
| Cross-check | Independently compute yes and eligible-household counts in SQL/Python; exact integers and absolute proportion tolerance 1e-12 |

E1 observed eligible counts: 132859 yes + 10246 no = 143105. Those are sample counts, not an implementation or interpretation of the M2 indicator. E2 must expose denominator, missingness, source version and scope on every output.

Candidate RQ1 is **narrowed** to observed-sample participation; population/domain comparisons remain gated. RQ2 access/service inference is **deferred**; infrastructure presence and input quantity are not access measures. RQ3 robustness is **deferred** until an E2 baseline exists. No invented geography or causal effect fills those gaps.
