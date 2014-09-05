
CREATE TEMPORARY FUNCTION segment AS 'com.zetyun.hive.udf.WordSegment';

--------------------------------------
--Extract the tokens
--------------------------------------

DROP TABLE IF EXISTS ${OUTPUT_output_table1};
create table ${OUTPUT_output_table1}(id string,tokens string) 
row format delimited fields terminated by '\t';

insert overwrite table ${OUTPUT_output_table1} 
select userid,segment(raw_message) from ${INPUT_input_table} WHERE userid is not null AND raw_message is not null;

