
-- TODO : Fill your code here
DROP TABLE IF EXISTS ${OUTPUT_selected_table};

CREATE TABLE ${OUTPUT_selected_table} AS
SELECT ${PARAM_columns}
FROM ${INPUT_from_table};
