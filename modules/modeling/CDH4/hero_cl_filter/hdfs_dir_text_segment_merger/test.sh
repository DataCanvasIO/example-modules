touch ./input.txt
echo "hdfs://10.10.0.114/tmp/hive-jiaqi/dir_merger_input/" > ./input.txt

screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --input_dir ./input.txt \
  --output_dir ./output.txt
