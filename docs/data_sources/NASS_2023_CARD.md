# NASS 2023 — initial source feasibility card

Updated: 2026-10-29. M1 suitability baseline is technically complete after E1.1/E1.2; **no population analysis is approved**. See [findings](../../reports/E1_REAL_DATA_PROFILING.md), [inventory](NASS_2023_INVENTORY.md), [design/period review](NASS_DESIGN_AND_PERIOD_REVIEW.md) and [M1 disposition](../M1_REVIEW.md). This is not an exhaustive audit of every variable or the full survey report.

## Release and acquisition route

NBS study ID: `NGA-NBS-NASS-2023-v01`. The [NBS catalogue](https://microdata.nigerianstat.gov.ng/index.php/catalog/173) and [JSON metadata](https://microdata.nigerianstat.gov.ng/index.php/metadata/export/173/json) describe edited anonymized agricultural household data. The access summary addresses confidentiality and citation but does not establish blanket redistribution permission. The [download page](https://microdata.nigerianstat.gov.ng/index.php/catalog/173/get-microdata) requires login. Actual authenticated terms and file inventory remain unverified.

The [World Bank dictionary](https://microdata.worldbank.org/catalog/8194/data-dictionary) uses release ID `NGA_2023_NASS_v01_M_v01_A_ESS`; its access page routes to [FAO](https://microdata.fao.org/index.php/catalog/2874/get-microdata), which routes back to NBS. This is not an alternative unauthenticated microdata route. Do not assume the NBS download and mirrored dictionary have identical columns until inspected.

## Questionnaire evidence

Downloaded the public [NBS questionnaire](https://microdata.nigerianstat.gov.ng/index.php/catalog/173/download/1298) into ignored local storage on 2026-10-28:

- Local path: `data/raw/nass_2023/documentation/questionnaire.pdf`
- Size: 981956 bytes; 61 PDF pages.
- SHA256: `29a696d9764a1d8c70874a18d4e0b4d5f8d4b2d2ba6d8a7efaeabbd17ac4f676`
- Extracted text: ignored `data/interim/nass_2023/documentation/questionnaire.txt`, using inspection-only `pypdf==6.21.3` in `.venv`; not a core dependency decision.

Administrative activity questions distinguish rainy and dry seasons and disable non-applicable modules. Section 2 describes plot-level records (PDF pp. 12–15), including irrigation infrastructure (p. 13). Section 3C (p. 39) collects input quantities using types populated from earlier responses. Thus absent input rows cannot simply mean non-use. The catalogue's date fields and questionnaire seasons need reconciliation before assigning reference periods to outputs. No raw questionnaire copies or extracted text are committed.

## Relevant dictionary findings

The following are metadata observations, not verified schemas or computed findings:

- [Households F14](https://microdata.worldbank.org/catalog/8194/data-dictionary/F14?file_name=1_households): `hhid`, `zone_id`, `state_id`, `sector`, `final_weight`; activity fields `s00_q15a`, `s00_q15b`, `s00_q16`, `s00_q17`, `s00_q18`; reference fields `referenceAgYear`, `mainAgSeason`, `minorAgSeason`. Listing-prefilled activities must not silently replace interview responses.
- [Main-season plots F16](https://microdata.worldbank.org/catalog/8194/data-dictionary/F16?file_name=3_Plot_mainSeason): `hhid`, `s02_plotRoster__id`, `s02_q07`, `s02_q08`, `s02_q09`, `final_weight`. Candidate plot key is household + plot ID, subject to uniqueness checks.
- [Irrigation variable](https://microdata.worldbank.org/catalog/8194/variable/F16/V1112?name=s02_q07): codes 1=yes, 2=no for infrastructure presence. This is not irrigation use or access to an extension service. Published frequencies are not population estimates and are not reused as project results.
- [Input file F22](https://microdata.worldbank.org/catalog/8194/data-dictionary/F22?file_name=9_Input_use_mainSeason): `hhid`, `interview__id`, `s03c_inputType__id`, `s03c_q01`, `final_weight`. Quantity is labelled kilograms; unit harmonization and type/skip mapping require further review before summing or defining users.

## Proposed first E1 field and remaining gates

Begin with **main-season plot irrigation-infrastructure response validity/completeness**, using `s02_q07` and candidate plot keys. This is a proposed profiling target, not a finalized population indicator. Compare row counts, distinct candidate keys and yes/no/other/missing counts independently after permitted acquisition. Unknowns remain separate; never convert missing to no.

Population estimates remain deferred: verify downloaded release, universe, key uniqueness, period, final weight applicability and variance-design fields or valid replication information. A household weight repeated on plot rows does not turn a plot proportion into a household proportion. No LGA estimates or naive confidence intervals are authorized by geographic labels alone.

## GHS alternative

The [GHS Wave 5 catalogue](https://microdata.worldbank.org/catalog/6410) describes agriculture and household modules, national/zonal scope, and distinct cross-sectional versus longitudinal weights. Current ID is `NGA_2023_GHSP-W5_v02_M`; recheck at acquisition. It also notes a mixed-mode input/labour subsample whose reference periods require care.

GHS remains a genuine alternative for services/welfare questions. Retain NASS for this first documentation-led E1 target; this is not a final source lock. GHS variable-level matching is incomplete. Both require verified access terms; do not merge them to fill missing fields.

## Signed-in application evidence — 2026-10-28

Owner supplied two locally saved page PDFs. The get-microdata snapshot (p. 2) displays an access application, not a granted download inventory. The related-materials snapshot lists questionnaires, reports and tables, not respondent microdata files. Account details and full snapshots are not copied into Git.

Observed application conditions, paraphrased:

- No redistribution or sale of supplied data/materials without written archive agreement.
- Statistical/scientific research and aggregate reporting only; no investigations of specific individuals or organizations.
- No reidentification or use of inadvertently discovered identities; discoveries must be reported to the archive.
- No identifying linkage across archive or external datasets. This does not establish permission for arbitrary joins; retain only documented analytical relationships and verify ambiguity before use.
- Cite the dataset as required and send electronic copies of resulting reports/publications to the archive.
- Data providers disclaim responsibility for users' interpretations. Proceeding to retrieval signifies acceptance of the displayed conditions.

The owner must review and submit the intended-use application through their signed-in session. No submission, agreement acceptance, access grant or microdata acquisition was performed by the assistant. File inventory, authenticated download terms and release details remain pending after submission. Publication obligations are recorded for later fulfillment; no report has been sent to anyone.

The paragraph above records the 2026-10-28 state. On 2026-10-29 the owner reported a completed download and supplied a Drive folder. The archive was found locally, copied into ignored storage, hashed and CRC-checked. Its 21 Stata files are listed in the linked inventory. This establishes local acquisition, not independent observation of application acceptance or any additional authenticated terms. Record-level schema, keys, labels, release equivalence and survey-design suitability remain to be checked.

E1.1 update: household `hhid` and plot (`hhid`, `s02_plotRoster__id`) keys are complete and unique in the parsed files; all plot household IDs match household records. Selected infrastructure/weight labels agree with the dictionary descriptions. These checks support the bounded protocol, not full release equivalence or survey-design suitability. Wider schemas and analytical eligibility remain unverified.
