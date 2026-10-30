# Water Management IR1 v1.0

Specified 2026-10-31 before the new analytical run. Stakeholder question: what irrigation infrastructure is reported on main-season plot records, and which main methods and water sources are reported among plots answering yes? This informs further investigation of recorded water-management arrangements, not investment allocation or unmet demand.

## Source, grain and periods

Use frozen NASS archive SHA256 `a5c0544f8b17f7e1f0627928b82ad19559110886930bf5f2e447fdef1b205d02`. Validate complete unique household keys and household main-season/year fields using the existing period guard. Main season is April–October2022. Plot grain: complete unique `(hhid,s02_plotRoster__id)`, with a valid parent household and type1/2/3. Include all roster plot types, including temporarily fallow plots and kitchen gardens; do not silently redefine the denominator as cultivated plots, people or households.

Validate exact field and value labels: `s02_q07` asks whether irrigation infrastructure exists;1=yes,2=no. `s02_q08` asks the main method:1 surface,2 sprinkler,3 drip,4 spray/microsprinkler,5 bubbler,6 equipped wetland/inland valley bottoms,7 equipped flood recession,8 spate,99 other. Code8 follows the released labels; preserve the previously recorded questionnaire-version discrepancy. `s02_q09` asks the main water source:1 on-farm groundwater,2 on-farm surface water,3 off-farm surface water,4 municipal/network,5 treated wastewater,6 reservoir,99 other. Preserve full released labels in the artifact.

## Eligibility, missingness and rates

- Infrastructure: yes/(yes+no). Missing ordinary/tagged Stata values and other numeric codes are separate exclusions; input=yes+no+missing+invalid. Zero valid denominator produces null, never0%.
- Method and source each have their own eligibility: only infrastructure-yes plot records. Report eligible total, valid categorical responses, missing and invalid exclusions. Valid denominator=eligible-missing-invalid. Category shares divide by that field's valid denominator; categories sum to that denominator. A zero valid denominator gives null shares. Include zero-count allowed categories so absence is distinguishable from unrecognized codes.
- Count records outside infrastructure-yes and populated method/source responses outside that subset. Missing fields on infrastructure-no records are expected skips, not quality failures. Missing/invalid infrastructure does not establish ineligibility in the real world; those records remain outside the observed-yes subset. Any populated response outside that subset is an inconsistency requiring review; the product hides irrigation results if this counter is nonzero.
- Nonnumeric/boolean codes, missing/duplicate keys, orphan parents, unknown plot types and missing/duplicate required columns abort. Do not impute, coerce, deduplicate or change raw inputs.

## Independent checks and presentation

Independently reconcile Python counters with SQLite groupings for infrastructure, eligible category frequencies and outside-yes skip flags. Shared validated staging is disclosed. Pin archive/model/SQL/contract/lock hashes and execution versions. Cross-check plot total with the core survey bundle and historical infrastructure counts with the prior E1 evidence during review. New artifact remains ignored, with a separately reviewed packaged manifest. The optional Water Management section fails closed independently; it must not hide existing activity/plot/map results.

Agricultural Insights gets one section with Infrastructure presence / Irrigation methods / Water sources controls and percentage/count mode. Each selection shows its eligible and valid denominator, missing/invalid exclusions, source, period, plain-language observation and supported next investigation. Methods/sources are single main categorical responses, unlike overlapping household activities. Do not pool them, chart states by irrigation, call infrastructure presence actual use, or infer that infrastructure-no plots need irrigation or are necessarily rain-fed. No household locations, geographic filters or automatic targeting. This delivery does not authorize deployment or survey redistribution; M6-04 stays open.

Acceptance: manually counted positive/negative/edge fixtures; explicit skip and unknown-code tests; actual record/label validation and SQL/Python equality; artifact accounting/hash/failure tests; selector/unit transitions and denominator checks; installed-wheel full JSON equality; actual desktop/narrow browser review. Record observed findings and limits separately after execution.
