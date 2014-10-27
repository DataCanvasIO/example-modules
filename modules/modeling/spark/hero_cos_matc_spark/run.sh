#!/bin/bash

echo "hdfs://10.10.0.114/tmp/zetjob/admin/job320/blk1774/dump_dir" > rs_dir.input
echo "hdfs://10.10.0.114/tmp/zetjob/admin/job320/blk1773/dump_dir" > jd_dir.input
touch match_result.output


screwjack --username jiaqi run docker \
  --param-hdfs_root hdfs://10.10.0.114 \
  --param-spark_host  spark://10.10.0.114:7077 \
  --rs_dir rs_dir.input \
  --jd_dir jd_dir.input \
  --match_result match_result.output

#spark://10.10.0.114:7077 \

