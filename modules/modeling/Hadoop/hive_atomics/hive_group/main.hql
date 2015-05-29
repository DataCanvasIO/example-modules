
-- TODO : Fill your code here
DROP TABLE IF EXISTS ${OUTPUT_grouped_table};

CREATE TABLE ${OUTPUT_grouped_table} AS
SELECT ${PARAM_selected_columns}
FROM ${INPUT_from_table}
GROUP BY ${PARAM_group_by_columns};

