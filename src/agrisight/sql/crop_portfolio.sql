-- Count each household once per temporary crop category, across all its plots.
SELECT crop,COUNT(*) FROM (
    SELECT DISTINCT hh,crop FROM crops WHERE kind=1
) GROUP BY crop;
