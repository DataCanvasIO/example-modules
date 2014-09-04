touch ratings1
touch user1
touch cl_result1

echo "hdfs://10.10.0.114/tmp/zetjob/jiaqi/job123/blk456/ratings1" > ratings1
echo "hdfs://10.10.0.114/tmp/zetjob/jiaqi/job123/blk456/users1" > user1

screwjack run docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-HiveServer2_Host 10.10.0.114 \
  --param-HiveServer2_Port 10000 \
  --param-yarn_resourcemanager 10.10.0.114:8032 \
  --param-yarn_resourcemanager_scheduler 10.10.0.114:8030 \
  --ratings ./ratings1 \
  --usersFile ./user1 \
  --cl_result ./cl_result1
