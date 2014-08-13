#!/bin/bash

echo "recm_raw_browsing" > input.txt
touch ./output.txt

screwjack run docker \
  --param-hdfs_root  hdfs://192.168.1.20 \
  --param-HiveServer2_Host 192.168.1.20 \
  --param-HiveServer2_Port 10000 \
  --param-FILE_DIR ./resource/files \
  --param-UDF_DIR ./resource/udfs \
  --input_table ./input.txt \
  --output_table ./output.txt

