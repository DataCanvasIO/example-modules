touch table_a.txt
echo "sample_a" > table_a.txt
touch table_b.txt
echo "sample_b" > table_b.txt
touch joined_table

screwjack run  docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-join_type "RIGHT OUTER" \
  --param-on_condition "a.id =b.id" \
  --table_a ./table_a.txt \
  --table_b ./table_b.txt \
  --joined_table ./joined_table
