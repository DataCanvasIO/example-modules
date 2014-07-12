#!/bin/bash

echo "hdfs://10.10.0.173/tmp/zetjob/xiaolin/job456/blk789/sentiment_result" > input.avro_path

screwjack run docker \
    --param-hdfs_root="hdfs://10.10.0.173" \
    --param-AWS_ACCESS_KEY_ID="" \
    --param-AWS_ACCESS_KEY_SECRET="" \
    --param-output_path="s3n://xiaolin/review_sentiment_results" \
    --param-yarn_resourcemanager="10.10.0.173:8032" \
    --param-yarn_resourcemanager_scheduler="10.10.0.173:8030" \
    --avro_path=input.avro_path
