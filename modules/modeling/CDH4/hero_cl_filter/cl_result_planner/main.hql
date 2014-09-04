
create temporary function cl_result_planner AS 'com.zetdata.hive.hero.udtf.CLResultPlanner';

DROP TABLE IF EXISTS ${OUTPUT_cl_result_plan_table};
CREATE TABLE ${OUTPUT_cl_result_plan_table} (auserid STRING,buserid STRING,score DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',';


INSERT OVERWRITE TABLE ${OUTPUT_cl_result_plan_table}
SELECT cl_result_planner(id,cl_result_list) AS (auserid,buserid,score) FROM ${INPUT_cl_result_table};
