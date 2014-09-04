
touch ./input_table
echo 'cl_result0' > ./input_table
touch ./output_table


screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --cl_result_table ./input_table \
  --cl_result_plan_table ./output_table 

