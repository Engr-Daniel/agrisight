-- NASS-01 model v1.0. One row per released agricultural household.
-- NULL/other codes are retained for audit and excluded only from valid denominator.
CREATE TABLE stg_nass_households (
    household_id TEXT NOT NULL PRIMARY KEY CHECK (length(trim(household_id)) > 0),
    main_crop_code REAL
);

CREATE VIEW int_nass01_eligibility AS
SELECT
    household_id,
    CASE
        WHEN main_crop_code IS NULL THEN 'missing'
        WHEN main_crop_code = 1 THEN 'yes'
        WHEN main_crop_code = 2 THEN 'no'
        ELSE 'invalid'
    END AS response_status
FROM stg_nass_households;

CREATE VIEW mart_nass01 AS
WITH counts AS (
    SELECT
        COUNT(*) AS input_rows,
        COALESCE(SUM(CASE WHEN response_status = 'yes' THEN 1 ELSE 0 END), 0) AS yes_count,
        COALESCE(SUM(CASE WHEN response_status = 'no' THEN 1 ELSE 0 END), 0) AS no_count,
        COALESCE(SUM(CASE WHEN response_status = 'missing' THEN 1 ELSE 0 END), 0)
            AS missing_count,
        COALESCE(SUM(CASE WHEN response_status = 'invalid' THEN 1 ELSE 0 END), 0)
            AS invalid_count
    FROM int_nass01_eligibility
)
SELECT
    input_rows,
    yes_count AS numerator,
    yes_count + no_count AS denominator,
    no_count,
    missing_count,
    invalid_count,
    missing_count + invalid_count AS excluded_count,
    CAST(yes_count AS REAL) / NULLIF(yes_count + no_count, 0) AS proportion,
    100.0 * yes_count / NULLIF(yes_count + no_count, 0) AS percentage
FROM counts;
