touch output_path

screwjack --username jiaqi run docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-data_path hdfs://10.10.0.114/tmp/data_path \
  --hdfs_path output_path

