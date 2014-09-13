
DROP TABLE IF EXISTS ${OUTPUT_joined_table};
CREATE TABLE ${OUTPUT_joined_table} AS
SELECT a.id AS a_id,a.num AS a_num,a.rank AS a_rank,b.id AS b_id,b.check AS b_check 
FROM ${INPUT_table_a} a RIGHT OUTER JOIN ${INPUT_table_b} b 
ON a.id =b.id 
;
