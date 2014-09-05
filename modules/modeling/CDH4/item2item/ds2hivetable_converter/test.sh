#!/bin/bash

screwjack gen_ds --ds_type hdfs --ds_url="hdfs://192.168.1.20/tmp/jiaqi/item2item/transaction/transaction.csv" > input.txt

screwjack run local \
  --param-hdfs_root=hdfs://192.168.1.20 \
  --param-HiveServer2_Host=192.168.1.20 \
  --param-HiveServer2_Port=10000 \
  --param-FILE_DIR=./resources/files/ \
  --param-UDF_DIR=./resources/udfs/ \
  --param-SCHEMA="userid STRING, pid STRING,timstp TIMESTAMP" \
  --input=./input.txt \
  --output=./output.txt

