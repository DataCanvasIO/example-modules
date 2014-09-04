touch output.hive.table
touch input.hdfs.directory
echo "hdfs://10.10.0.114/tmp/zetjob/jiaqi/job123/blk456/match_result/" > input.hdfs.directory

screwjack run local \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-SCHEMA "auserid string,buserid string,a2b int,atype int" \
  --param-FIELD_DELIMITER "," \
  --input ./input.hdfs.directory  \
  --output ./output.hive.table
