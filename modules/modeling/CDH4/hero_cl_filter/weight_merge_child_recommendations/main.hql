
-- TODO : Fill your code here

DROP TABLE IF EXISTS ${OUTPUT_result_table};
CREATE TABLE ${OUTPUT_result_table} (aid STRING,bid STRING,score DOUBLE,a_type TINYINT )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

INSERT OVERWRITE TABLE ${OUTPUT_result_table}
SELECT coalesce(cosine_match.aid,cl_match.aid) AS aid,
       coalesce(cosine_match.bid,cl_match.bid) AS bid,
       coalesce(cosine_match.score,0.0) + coalesce(cl_match.score,0.0) AS score,
       coalesce(cosine_match.a_type,cl_match.a_type) AS a_type,
FROM
(
    SELECT aid,bid,${PARAM_cosine_match_weight}*score AS score,a_type 
    FROM ${INPUT_cosine_match_result_table}
)cosine_match
FULL OUTER JOIN
(
    SELECT aid,bid,${PARAM_cl_match_weight}*score/2.0 AS score,a_type
    FROM
    (
        SELECT auserid AS aid ,buserid AS bid,score,0 AS a_type FROM ${INPUT_hunter_cl_result_table}
        UNION ALL
        SELECT auserid AS aid ,buserid AS bid,score,1 AS a_type FROM ${INPUT_applicant_cl_result_table}
    )union_cl_result
)cl_match
ON cosine_match.aid = cl_match.aid
AND cosine_match.bid = cl_match.bid
AND cosine_match.a_type = cl_match.a_type;
