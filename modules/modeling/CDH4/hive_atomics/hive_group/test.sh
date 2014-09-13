touch from_table
touch grouped_table

echo " zetjob_admin_job388_blk5016_OUTPUT_result_table" > from_table

screwjack run docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port  10000 \
  --param-group_by_columns "aid,a_type" \
  --param-selected_columns "aid,a_type,count(bid),avg(score)" \
  --from_table ./from_table \
  --grouped_table ./grouped_table

