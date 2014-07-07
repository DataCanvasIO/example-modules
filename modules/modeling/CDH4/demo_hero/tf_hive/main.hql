
CREATE TEMPORARY FUNCTION tf AS 'com.zetyun.hive.udf.TFFunction';
---------------------------------------
--Calculate the tf
---------------------------------------

DROP TABLE IF EXISTS ${OUTPUT_output_table};
create table ${OUTPUT_output_table}(id string,tf_map string) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t';

insert overwrite table ${OUTPUT_output_table}
select id,tf(tokens) from ${INPUT_input_table};

