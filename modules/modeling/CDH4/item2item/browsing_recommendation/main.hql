
-- TODO : Fill your code here
CREATE TABLE ${OUTPUT_output_table} AS
SELECT a_pid,b_pid,dotprod,a_len,b_len,1.0*dotprod/sqrt(a_len)/sqrt(b_len)
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
;
