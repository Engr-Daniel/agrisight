-- Grain: one validated plot. Only infrastructure-yes plots enter method/source denominators.
SELECT 'presence',presence,COUNT(*) FROM plots GROUP BY presence
UNION ALL
SELECT 'method',method,COUNT(*) FROM plots WHERE presence='yes' GROUP BY method
UNION ALL
SELECT 'source',source,COUNT(*) FROM plots WHERE presence='yes' GROUP BY source;
