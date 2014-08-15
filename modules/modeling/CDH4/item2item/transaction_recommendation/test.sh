#!/bin/bash

<<<<<<< HEAD
echo "recm_raw_transaction" >> input.txt
touch out.txt

screwjack run docker \
  --param-hdfs_root hdfs://192.168.1.20 \
  --param-HiveServer2_Host 192.168.1.20 \
  --param-HiveServer2_Port 10000 \
  --param-FILE_DIR ./resources/files \
  --param-UDF_DIR  ./resources/udfs \
  --param-topN  1 \
  --input_table ./input.txt \
  --output_table ./output.txt
=======
echo "zetjob_jiaqi_job456_blk789_OUTPUT_output" > input.txt
>>>>>>> a4faddbc419f09423d11a7e66584194e697b40fe
