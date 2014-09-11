touch input_table
echo "sample_07" > input_table
touch output_table

screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-columns code,total_emp,salary \
  --from_table ./input_table \
  --selected_table ./output_table  

