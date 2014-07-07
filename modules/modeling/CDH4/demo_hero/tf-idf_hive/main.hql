
CREATE TEMPORARY FUNCTION explode_TF AS 'com.zetyun.hive.udtf.ExplodeTF';
CREATE TEMPORARY FUNCTION merge_TFIDF AS 'com.zetyun.hive.udaf.MergeTFIDFResolver';

--------------------------------------
--EXPLODE TF FOR CALCULATE TF-IDF
--------------------------------------
DROP TABLE IF EXISTS ${MYNS}explode_tf;
CREATE TABLE ${MYNS}explode_tf (id STRING,token STRING,tf DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';
INSERT OVERWRITE TABLE ${MYNS}explode_tf
SELECT explode_TF(id,tf_map) AS (id,token,tf)
FROM ${INPUT_input_table1};

---------------------------------------
--CALCULATE TF-IDF
---------------------------------------
DROP TABLE IF EXISTS ${MYNS}id_token_tfidf;
CREATE TABLE ${MYNS}id_token_tfidf (id STRING,token STRING,tfidf DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${MYNS}id_token_tfidf 
SELECT /*+MAPJOIN(token_idf) */
explode_tf.id AS id,
explode_tf.token AS token,
explode_tf.tf *token_idf.idf as tf_idf 
FROM 
${INPUT_input_table2} token_idf  JOIN ${MYNS}explode_tf explode_tf
ON  explode_tf.token = token_idf.token;

----------------------------------------
--GROUP BY ID
----------------------------------------
DROP TABLE IF EXISTS ${OUTPUT_output_table};
CREATE TABLE ${OUTPUT_output_table} (id STRING,tfidf STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

INSERT OVERWRITE TABLE ${OUTPUT_output_table}
SELECT id,merge_TFIDF(token,tfidf) AS token_list 
FROM ${MYNS}id_token_tfidf GROUP BY id;

