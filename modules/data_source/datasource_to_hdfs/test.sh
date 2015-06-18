#!/bin/bash

# export PYTHONPATH=/home/xiaolin/work/zetyun/pyDataCanvas.git/

set -x

TEST_CLUSTER=playground_cdh4

# EXEC_METHOD=local
# EXEC_METHOD=docker
EXEC_METHOD=docker-machine
TEST_CLUSTER="${TEST_CLUSTER:-hdp_sandbox}"


###############
# Test Case 1
###############
screwjack gen_ds \
    --ds_type=hdfs \
    --ds_url=hdfs://10.10.0.162/tmp/movielens/big/ratings.csv \
    > input2.ds.json

screwjack run ${EXEC_METHOD} \
    --param-cluster=${TEST_CLUSTER} \
    --DS=input2.ds.json \
    --dest_hdfs=output.hdfs && \
    cat output.hdfs

###############
# Test Case 2
###############
screwjack gen_ds \
    --ds_type=http \
    --ds_url=http://nlp.stanford.edu/courses/NAACL2013/NAACL2013-Socher-Manning-DeepLearning.pdf \
    > input2.ds.json

screwjack run ${EXEC_METHOD} \
    --param-cluster=${TEST_CLUSTER} \
    --DS=input2.ds.json \
    --dest_hdfs=output.hdfs && \
    cat output.hdfs


###############
# Test Case 3
###############
# screwjack gen_ds \
#     --ds_type=s3 \
#     --ds_url=s3n://xiaolin/movielens/big/ratings.csv \
#     key=$AWS_ACCESS_KEY_ID \
#     token=$AWS_SECRET_ACCESS_KEY > input2.ds.json

# WITH aws_key/aws_sec
screwjack gen_ds \
    --ds_type=s3 \
    --ds_url=s3n://datacanvas-opendata/movielens/medium/ratings.csv \
    key=$AWS_ACCESS_KEY_ID \
    token=$AWS_SECRET_ACCESS_KEY \
    > input2.ds.json

# # WITHOUT aws_key/aws_sec
# screwjack gen_ds \
#     --ds_type=s3 \
#     --ds_url=s3n://datacanvas-opendata/movielens/medium/ratings.csv \
#     > input2.ds.json

screwjack run ${EXEC_METHOD} \
    --param-cluster=${TEST_CLUSTER} \
    --DS=input2.ds.json \
    --dest_hdfs=output.hdfs && \
    cat output.hdfs
