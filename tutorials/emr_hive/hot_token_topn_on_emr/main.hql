
set hive.base.inputformat=org.apache.hadoop.hive.ql.io.HiveInputFormat;

CREATE TEMPORARY FUNCTION splitword AS 'com.your_company.hive.udtf.SplitWord';

--CREATE OUTPUT TABLE

DROP TABLE IF EXISTS hot_token_topN_table;
CREATE EXTERNAL  TABLE hot_token_topN_table
(
        token STRING,
        freq  INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE LOCATION '${OUTPUT_hot_token_topN_s3_dir}';

--CREATE AN EXTERNAL TABLE TO LOAD THE QUERY DATA
DROP TABLE IF EXISTS query;
CREATE EXTERNAL TABLE query
(
        id STRING,
        site STRING,
        timestp TIMESTAMP
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
LOCATION '${INPUT_query_log_dir_s3_dir}';

INSERT OVERWRITE TABLE hot_token_topN_table
SELECT token, freq FROM
(
        SELECT token,count(1) AS freq FROM
        (
                SELECT splitword(site) AS token FROM query
        )token_table
        GROUP BY token
)token_frep
ORDER BY freq DESC LIMIT ${PARAM_topN};
