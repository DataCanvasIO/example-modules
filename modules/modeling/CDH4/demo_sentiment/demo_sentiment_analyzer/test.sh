#!/bin/bash

touch output.hdfs && \
    screwjack run docker \
    --param-hdfs_root="hdfs://10.10.0.173" \
    --param-yarn_resourcemanager="10.10.0.173:8032" \
    --param-yarn_resourcemanager_scheduler="10.10.0.173:8030" \
    --DS=./input.ds \
    --sentiment_result=./output.hdfs

