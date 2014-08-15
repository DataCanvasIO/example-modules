
-- TODO : Fill your code here


DROP TABLE IF EXISTS ${OUTPUT_output_table};
CREATE TEMPORARY FUNCTION rankongroup AS 'com.zetdata.hive.udf.RankerOnGroup';

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
            SELECT a_pid AS pid1,b_pid AS pid2,1.0*dotprod/sqrt(a_len)/sqrt(b_len) AS score
            FROM
            (
                    SELECT a.pid AS a_pid,b.pid AS b_pid,count(distinct a.sessionid) AS dotprod
                    FROM ${INPUT_input_table} a JOIN ${INPUT_input_table} b ON  a.sessionid = b.sessionid
                    WHERE a.pid != b.pid
                    GROUP BY a.pid,b.pid
            )dotprod_part
            LEFT OUTER JOIN
            (
                    SELECT pid ,count(sessionid) AS a_len
                    FROM ${INPUT_input_table}
                    GROUP BY pid
            )a_len_part
            ON dotprod_part.a_pid = a_len_part.pid
            
            LEFT OUTER JOIN
            (
                    SELECT pid,count(sessionid) AS b_len
                    FROM ${INPUT_input_table}
                    GROUP BY pid
            )b_len_part
            ON dotprod_part.b_pid = b_len_part.pid
            DISTRIBUTE BY pid1
            SORT BY pid1,score desc
        )res1
    )res2
)with_rank
WHERE rank<=${PARAM_topN}
;
