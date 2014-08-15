
-- TODO : Fill your code here
CREATE TEMPORARY FUNCTION agg_word AS 'com.zetdata.hive.udaf.AggregateKeyword';
CREATE TEMPORARY FUNCTION cosine_match AS 'com.zetdata.hive.udf.CosineMatch';
CREATE TEMPORARY FUNCTION rankongroup AS 'com.zetdata.hive.udf.RankerOnGroup';

DROP TABLE IF EXISTS ${OUTPUT_output_table};
CREATE TABLE ${OUTPUT_output_table} AS
SELECT pid1,pid2,score,rank
FROM
(
    SELECT pid1,pid2,score,rankongroup(pid1)+1 AS rank 
    FROM
    (
       SELECT pid1,pid2,score
       FROM
       (
            SELECT a.pid AS pid1 ,b.pid AS pid2,cosine_match(a.kv_seq,b.kv_seq) AS score
            FROM
            (
                    SELECT pid, agg_word(query) AS kv_seq
                    FROM ${INPUT_input_table} GROUP BY pid
            )a
            LEFT OUTER JOIN
            (
                    SELECT pid, agg_word(query) AS kv_seq
                    FROM ${INPUT_input_table} GROUP BY pid
            )b
            WHERE a.pid != b.pid
            DISTRIBUTE BY pid1
            SORT BY pid1,  score desc
        )res1
    )res2
)with_rank
WHERE rank<=${PARAM_topN};
