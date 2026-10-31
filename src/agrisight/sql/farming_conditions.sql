-- Grain: raw household-crop destination records, never crop-plot joins.
CREATE INDEX crop_branch ON crops(s03_cropsType, s01a_q07, s01h_q08);
CREATE INDEX harvest_crop ON harvest(s01b_harvestedCrops__id);
CREATE INDEX input_type ON inputs(s03c_inputType__id);
CREATE TEMP VIEW destination_complete AS
SELECT * FROM harvest WHERE s01b_q02 IN (1, 2) AND s01b_q20 IN (1, 2);
-- Grain: household-input record; null quantities are not zero.
CREATE TEMP VIEW input_quality AS
SELECT *, CASE WHEN s03c_q01 IS NULL THEN 'Missing'
 WHEN s03c_q01 < 0 OR ABS(s03c_q01) > 1.7976931348623157e308 THEN 'Invalid'
 WHEN s03c_q01 = 0 THEN 'Zero' ELSE 'Positive' END quantity_status
FROM inputs;
