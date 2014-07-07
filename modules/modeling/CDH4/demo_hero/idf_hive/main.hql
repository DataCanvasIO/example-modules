
CREATE TEMPORARY FUNCTION explode_tokens AS 'com.zetyun.hive.udtf.ExplodeTokens';
CREATE TEMPORARY FUNCTION token_contains AS 'com.zetyun.hive.udf.TokenContains';

---------------------------------------
--Count the total num of message
---------------------------------------
DROP TABLE IF EXISTS ${MYNS}message_total_num;
CREATE TABLE ${MYNS}message_total_num (num BIGINT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}message_total_num
SELECT COUNT(1) FROM ${INPUT_input_table};


----------------------------------------
--Get token list
----------------------------------------
DROP TABLE IF EXISTS ${MYNS}tokens;
CREATE TABLE ${MYNS}tokens (token STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}tokens 
SELECT DISTINCT token FROM 
(
    SELECT explode_tokens(tokens) AS token
    FROM ${INPUT_input_table}
)all_tokens;

-----------------------------------------
--JOIN THE TOKENS WITH ALL ID_TOKENS
--COUNTING TOKEN REFERENCE BY MESSAGE
-----------------------------------------
DROP TABLE IF EXISTS ${MYNS}token_refnum;
CREATE TABLE ${MYNS}token_refnum (token STRING,refnum INT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}token_refnum
SELECT token,count(1) AS ref_count FROM 
(
    SELECT /*+ MAPJOIN(t) */ t.token,token_contains(t.token,idt.tokens) as mark
    FROM ${MYNS}tokens t JOIN ${INPUT_input_table} idt
)token_with_mark
WHERE mark = 1
GROUP BY token;

-------------------------------------------
--CALCULATE THE IDF
-------------------------------------------
DROP TABLE IF EXISTS ${OUTPUT_output_table};
CREATE TABLE ${OUTPUT_output_table} (token STRING,idf DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${OUTPUT_output_table}
SELECT /*+MAPJOIN(mtn)*/ tf.token,log2(1.0*mtn.num/(tf.refnum)) 
FROM ${MYNS}message_total_num mtn JOIN ${MYNS}token_refnum tf ;

