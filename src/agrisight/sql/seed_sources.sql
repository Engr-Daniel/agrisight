-- Grain: temporary household-crop seed record; source responses may overlap.
SELECT 0,s0,COUNT(*) FROM seeds WHERE kind=1 GROUP BY s0
UNION ALL SELECT 1,s1,COUNT(*) FROM seeds WHERE kind=1 GROUP BY s1
UNION ALL SELECT 2,s2,COUNT(*) FROM seeds WHERE kind=1 GROUP BY s2
UNION ALL SELECT 3,s3,COUNT(*) FROM seeds WHERE kind=1 GROUP BY s3
UNION ALL SELECT 4,s4,COUNT(*) FROM seeds WHERE kind=1 GROUP BY s4;
