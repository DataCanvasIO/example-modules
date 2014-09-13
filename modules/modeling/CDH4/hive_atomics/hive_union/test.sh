touch table_a
touch table_b 
touch union_table
echo "sample_a" > table_a
echo "sample_aa" > table_b

screwjack run docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --table_a ./table_a \
  --table_b ./table_b \
  --union_table ./union_table
