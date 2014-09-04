touch ./input.txt
touch ./output.txt
echo "hdfs://10.10.0.114/tmp/zetjob/jiaqi/job123/blk456/user1"> input.txt

screwjack run docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --input_dir ./input.txt \
  --output_file ./output.txt
