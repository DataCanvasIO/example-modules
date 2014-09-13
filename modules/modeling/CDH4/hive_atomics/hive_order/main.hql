
DROP TABLE IF EXISTS ${OUTPUT_ordered_table};

CREATE TABLE ${OUTPUT_ordered_table} AS
SELECT *
FROM ${INPUT_from_table}
ORDER BY ${PARAM_order_by_columns}  
;
 
