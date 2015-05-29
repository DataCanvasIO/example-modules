
-- TODO : Fill your code here
DROP TABLE IF EXISTS ${OUTPUT_union_table};

CREATE TABLE ${OUTPUT_union_table} AS
SELECT *
FROM (
  SELECT *
  FROM ${INPUT_table_a}
  UNION ALL
  SELECT *
  FROM ${INPUT_table_b}
) unionResult;
