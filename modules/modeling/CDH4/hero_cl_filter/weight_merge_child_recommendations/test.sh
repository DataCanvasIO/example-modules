touch cosine_table
echo "zetjob_admin_job267_blk2146_OUTPUT_output_table" > cosine_table

touch hunter_cl_table
echo "cl_result_plan_table0" > hunter_cl_table

touch applicant_cl_table
echo "cl_result_plan_table1" > applicant_cl_table

touch result_table


screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-cosine_match_weight 0.7 \
  --param-cl_match_weight 0.3 \
  --hunter_cl_result_table hunter_cl_table \
  --applicant_cl_result_table applicant_cl_table \
  --cosine_match_result_table cosine_table \
  --result_table result_table

