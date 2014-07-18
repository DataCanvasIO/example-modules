#!/bin/bash

echo "hdfs://10.10.0.87/tmp/zetjob/admin/job99/blk380/sentiment_result" > input.avro_path
touch output.s3_path

screwjack run docker \
    --param-hdfs_root="hdfs://10.10.0.87" \
    --param-AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
    --param-AWS_ACCESS_KEY_SECRET="$AWS_SECRET_ACCESS_KEY" \
    --param-yarn_resourcemanager="10.10.0.87:8032" \
    --param-yarn_resourcemanager_scheduler="10.10.0.87:8030" \
    --avro_path=input.avro_path \
    --output_path=output.s3_path \
    --param-S3_BUCKET="xiaolin"
