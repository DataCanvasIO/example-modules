
-- TODO : Fill your code here
DROP TABLE IF EXISTS ${OUTPUT_filtered_table};
CREATE TABLE ${OUTPUT_filtered_table} AS
SELECT *
FROM ${INPUT_from_table}
WHERE ${PARAM_where};
