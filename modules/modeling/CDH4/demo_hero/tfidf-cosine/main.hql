
CREATE TEMPORARY FUNCTION tfidf_cosine AS 'com.zetyun.hive.udf.TFIDFCosine';

-------------------------------------
--GET HUNTER ID
-------------------------------------
DROP TABLE IF EXISTS ${MYNS}hunter_id;
CREATE TABLE ${MYNS}hunter_id (id STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}hunter_id
SELECT userid FROM ${INPUT_input_table1}
WHERE type = 0;

-------------------------------------
--GET APPLICANT ID
-------------------------------------
DROP TABLE IF EXISTS ${MYNS}applicant_id;
CREATE TABLE ${MYNS}applicant_id (id STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}applicant_id
SELECT userid FROM ${INPUT_input_table1}
WHERE type = 1;

---------------------------------------
--GET HUNTER MESSAGE
---------------------------------------
DROP TABLE IF EXISTS ${MYNS}hunter_tfidf;
CREATE TABLE ${MYNS}hunter_tfidf (id STRING,tfidf STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}hunter_tfidf
SELECT h_id.id,id_tfidf.tfidf
FROM ${MYNS}hunter_id h_id
LEFT OUTER JOIN ${INPUT_input_table2} id_tfidf 
ON h_id.id = id_tfidf.id;

---------------------------------------
--GET APPLICANT MESSAGE
---------------------------------------
DROP TABLE IF EXISTS ${MYNS}applicant_tfidf;
CREATE TABLE ${MYNS}applicant_tfidf (id STRING,tfidf STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}applicant_tfidf
SELECT a_id.id,id_tfidf.tfidf
FROM ${MYNS}applicant_id a_id
LEFT OUTER JOIN ${INPUT_input_table2} id_tfidf 
ON a_id.id = id_tfidf.id;

-----------------------------------------
--MATCH HUNTER WITH APPLICANT
-----------------------------------------
DROP TABLE IF EXISTS ${MYNS}match_result_h2a;
CREATE TABLE ${MYNS}match_result_h2a (hunter_id STRING,applicant_id STRING,score DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';
INSERT OVERWRITE TABLE ${MYNS}match_result_h2a
SELECT hunter_tfidf.id ,applicant_tfidf.id, tfidf_cosine(hunter_tfidf.tfidf,applicant_tfidf.tfidf)
FROM  ${MYNS}hunter_tfidf hunter_tfidf
LEFT OUTER JOIN ${MYNS}applicant_tfidf applicant_tfidf;




-----------------------------------------
--MATCH APPLICANT WITH HUNTER
-----------------------------------------
DROP TABLE IF EXISTS ${MYNS}match_result_a2h;
CREATE TABLE ${MYNS}match_result_a2h (applicant_id STRING, hunter_id STRING,score DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';
INSERT OVERWRITE TABLE ${MYNS}match_result_a2h

SELECT applicant_tfidf.id, hunter_tfidf.id , tfidf_cosine(applicant_tfidf.tfidf,hunter_tfidf.tfidf)
FROM  ${MYNS}applicant_tfidf applicant_tfidf
LEFT OUTER JOIN ${MYNS}hunter_tfidf hunter_tfidf;


-------------------------------------
--UNION THE DIRECT MATCH
-------------------------------------
DROP TABLE IF EXISTS ${OUTPUT_output_table};
CREATE TABLE ${OUTPUT_output_table} (aid STRING,bid STRING,score DOUBLE,b_type TINYINT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';


INSERT OVERWRITE TABLE ${OUTPUT_output_table}
SELECT union_input.aid,
       union_input.bid,
       union_input.score,
       b_type
FROM
(
    SELECT hunter_id AS aid,applicant_id AS bid,score , 0 AS b_type
    FROM ${MYNS}match_result_h2a WHERE score > 0
UNION ALL
    SELECT applicant_id AS aid, hunter_id AS bid, score, 1 AS b_type
    FROM ${MYNS}match_result_a2h WHERE score > 0
)union_input;

