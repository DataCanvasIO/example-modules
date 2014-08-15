
-- TODO : Fill your code here

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
            SELECT coalesce(m2.pid1,featu.pid1) AS pid1,
                   coalesce(m2.pid2,featu.pid2) AS pid2,
                   coalesce(m2.score,0.0)+${PARAM_weight4}* coalesce(featu.score,0.0) AS score
            FROM
            (
                SELECT coalesce(m1.pid1,keyw.pid1) AS pid1,
                       coalesce(m1.pid2,keyw.pid2) AS pid2,
                       coalesce(m1.score,0.0) + ${PARAM_weight3}*coalesce(keyw.score,0.0) AS score

                FROM
                (
                   SELECT coalesce(trans.pid1,brows.pid1) AS pid1,
                          coalesce(trans.pid2,brows.pid2) AS pid2,
                          ${PARAM_weight1}*coalesce(trans.score,0.0) + ${PARAM_weight2}* coalesce(brows.score,0.0) AS score
                   FROM
                   (
                       SELECT pid1,pid2,score
                       FROM ${INPUT_input_table1} 
                   )trans
                   FULL OUTER JOIN
                   (
                       SELECT pid1,pid2,score
                       FROM ${INPUT_input_table2}
                   )brows
                   ON trans.pid1 = brows.pid1
                   AND trans.pid2 = brows.pid2
                )m1
                FULL OUTER JOIN
                (
                    SELECT pid1,pid2,score
                    FROM ${INPUT_input_table3} 
                )keyw
                ON m1.pid1 = keyw.pid1
                AND m1.pid2 = keyw.pid2
            )m2
            FULL OUTER JOIN
            (
                SELECT pid1, pid2,score
                FROM ${INPUT_input_table4}
            )featu
            ON m2.pid1 = featu.pid1
            AND m2.pid2 = featu.pid2
        )res1
        DISTRIBUTE BY pid1
        SORT BY pid1,score desc
    )res2
)with_rank
WHERE rank<=${PARAM_topN} and score > 0.0;
