touch history_table
echo "zetjob_jiaqi_job456_blk789_OUTPUT_output" > history_table
touch result_table
echo "zetjob_jiaqi_job456_blk789_OUTPUT_result_table" > result_table

touch filtered_table


screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --history_table history_table \
  --result_table result_table \
  --filtered_table filered_table

