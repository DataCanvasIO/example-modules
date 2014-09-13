
DROP TABLE IF EXISTS ${OUTPUT_union_table};

CREATE TABLE ${OUTPUT_union_table} AS
SELECT *
FROM (
  SELECT id AS id,num AS num,rank AS rank
  FROM ${INPUT_table_a}
  UNION ALL
  SELECT idd AS id,numm AS num,rankkk AS rank
  FROM ${INPUT_table_b}
) unionResult;

