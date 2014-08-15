
-- TODO : Fill your code here

CREATE TEMPORARY FUNCTION cosine_feature_match AS 'com.zetdata.hive.udf.CosineFeatureMatch';
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
            SELECT a.pid AS pid1 ,b.pid AS pid2,
                    cosine_feature_match(a.feature,b.feature) AS score
            FROM
            (
                    SELECT pid , feature
                    FROM ${INPUT_input_table}
            )a
            LEFT OUTER JOIN
            (
                    SELECT pid, feature
                    FROM ${INPUT_input_table}
            )b
            WHERE a.pid != b.pid
            DISTRIBUTE BY pid1
            SORT BY pid1,score desc
        )res1
     )res2
)with_rank
WHERE rank <=${PARAM_topN};
