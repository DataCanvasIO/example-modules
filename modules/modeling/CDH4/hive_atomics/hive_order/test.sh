touch from_table
touch ordered_table
echo "sample_a" > from_table


screwjack run  docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-order_by_columns "id desc" \
  --param-limit "   " \
  --from_table ./from_table \
  --ordered_table ./ordered_table
