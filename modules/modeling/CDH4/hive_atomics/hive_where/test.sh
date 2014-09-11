touch input_table
echo "sample_a" > input_table
touch output_table


screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-where "id != 7" \
  --from_table ./input_table \
  --filtered_table ./output_table
