# KPI dictionary — candidates, NOT finalized

Every indicator needs: business question, decision, unit/grain, source, numerator, denominator, exclusions, date basis, privacy limits, owner, quality checks and test fixture.

| Metric | Draft definition | Critical caveat |
|---|---|---|
| Registered role entries | Count of accepted `actor_role` entries by type | Not necessarily distinct persons |
| Distinct registered persons | Count distinct stable `person_id` with accepted role | Exclude duplicate candidates pending human review only as explicitly approved |
| Profile completeness | Required non-null applicable fields / applicable required fields | Skip logic and non-applicable items must not count as missing |
| Verification coverage | Confirmed back-checks / eligible accepted submissions | Verification != accuracy |
| Duplicate-candidate rate | Candidate pairs or affected entries / appropriate stated base | Not a confirmed duplicate rate |
| Geo-validity rate | Passing spatial checks / coordinate-bearing eligible records | No coordinates may be valid if declined |
| Processing participation | Count of processor roles by category | Synthetic in operational demonstrations |
| Pipeline freshness | Time since completed successful refresh | Does not measure correctness |
| Coverage attainment | Completed eligible entries / **synthetic** assignment target | Not actual field coverage |

No KPI is considered approved until it has a separately tested SQL fixture and acceptance sign-off. For sampled public survey estimates, use documented design weights/uncertainty where justified; these operational registry indicators must not be mistaken for representative survey estimates.
