-- NASS-02 v1.0: unknown nonnegative area bounds, not survey confidence intervals.
CREATE TABLE stg_nass_plot_area (
    household_id TEXT NOT NULL CHECK(length(trim(household_id)) > 0),
    plot_id TEXT NOT NULL CHECK(length(trim(plot_id)) > 0),
    area REAL CHECK(area IS NULL OR (area >= 0 AND area <= 1.7976931348623157e308)),
    PRIMARY KEY (household_id, plot_id)
);

CREATE VIEW int_nass02_known_areas AS
SELECT area, ROW_NUMBER() OVER (ORDER BY area) AS known_rank
FROM stg_nass_plot_area WHERE area IS NOT NULL;

CREATE VIEW mart_nass02_bounds AS
WITH counts AS (
    SELECT COUNT(*) AS total_plots, COUNT(area) AS observed_areas,
           COUNT(*) - COUNT(area) AS missing_areas
    FROM stg_nass_plot_area
), ranks AS (
    SELECT *, (total_plots+1)/2 AS r1, (total_plots+2)/2 AS r2,
              (observed_areas+1)/2 AS o1, (observed_areas+2)/2 AS o2 FROM counts
), known AS (
    SELECT area, known_rank FROM int_nass02_known_areas
), endpoints AS (
    SELECT *,
        CASE WHEN total_plots=0 THEN NULL WHEN r1<=missing_areas THEN 0.0
             ELSE (SELECT area FROM known WHERE known_rank=r1-missing_areas) END AS l1,
        CASE WHEN total_plots=0 THEN NULL WHEN r2<=missing_areas THEN 0.0
             ELSE (SELECT area FROM known WHERE known_rank=r2-missing_areas) END AS l2,
        (SELECT area FROM known WHERE known_rank=r1) AS u1,
        (SELECT area FROM known WHERE known_rank=r2) AS u2,
        (SELECT area FROM known WHERE known_rank=o1) AS v1,
        (SELECT area FROM known WHERE known_rank=o2) AS v2
    FROM ranks
), medians AS (
    SELECT total_plots, observed_areas, missing_areas,
        CASE WHEN total_plots>0 THEN r1 END AS middle_lower_rank,
        CASE WHEN total_plots>0 THEN r2 END AS middle_upper_rank,
        v1/2.0+v2/2.0 AS observed_only_median_m2,
        l1/2.0+l2/2.0 AS full_roster_lower_m2,
        u1/2.0+u2/2.0 AS full_roster_upper_m2,
        CASE WHEN total_plots=0 THEN 'undefined'
             WHEN r2>observed_areas THEN 'unbounded' ELSE 'bounded' END AS status
    FROM endpoints
)
SELECT *, full_roster_upper_m2-full_roster_lower_m2 AS width_m2 FROM medians;
