
-- TODO : Fill your code here

DROP TABLE IF EXISTS ${OUTPUT_filtered_table};
CREATE TABLE ${OUTPUT_filtered_table} (aid STRING,bid STRING,score DOUBLE,a_type TINYINT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';

INSERT OVERWRITE TABLE ${OUTPUT_filtered_table}
SELECT result.aid,result.bid,score,result.a_type
FROM
(
    SELECT aid,bid,score,a_type 
    FROM ${INPUT_result_table}
)result
LEFT OUTER JOIN
(
    SELECT auserid,buserid,atype 
    FROM ${INPUT_history_table}
)history
ON result.aid = history.auserid 
AND result.bid = history.buserid 
AND result.a_type= history.atype
WHERE history.buserid is null and result.aid != result.bid;
