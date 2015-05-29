
-- TODO : Fill your code here
DROP TABLE IF EXISTS ${OUTPUT_joined_table};
CREATE TABLE ${OUTPUT_joined_table} AS
SELECT ${PARAM_selected_columns}
FROM ${INPUT_table_a} a ${PARAM_join_type} JOIN ${INPUT_table_b} b
ON ${PARAM_on_condition}
;
