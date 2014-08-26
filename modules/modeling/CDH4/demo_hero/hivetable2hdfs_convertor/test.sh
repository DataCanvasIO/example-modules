#!/bin/bash

touch ./output.txt 

screwjack run local \
  --param-HiveServer2_Host 192.168.1.20 \
  --param-HiveServer2_Port 10000 \
  --table_name zetjob_jiaqi_job456_blk789_hot_token_topn \
  --output_dir ./output.txt
