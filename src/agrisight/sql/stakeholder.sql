-- SA1 v1.0: one row per household/plot in separate staging tables; no grain-changing join.
WITH activity AS (
 SELECT 'crops' AS activity, crops AS response FROM hh
 UNION ALL SELECT 'livestock', livestock FROM hh
 UNION ALL SELECT 'fish_farming', fish_farming FROM hh
 UNION ALL SELECT 'fish_capture', fish_capture FROM hh
)
SELECT activity, COUNT(*) AS input_rows,
 SUM(response='yes') AS yes, SUM(response='no') AS no,
 SUM(response='missing') AS missing, SUM(response='other') AS invalid
FROM activity GROUP BY activity ORDER BY activity;
