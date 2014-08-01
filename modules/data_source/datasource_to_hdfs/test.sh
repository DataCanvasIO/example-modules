#!/bin/bash

set -x

# screwjack gen_ds \
#     --ds_type=s3 \
#     --ds_url=s3n://xiaolin/movielens/big/ratings.csv \
#     key=$AWS_ACCESS_KEY_ID \
#     token=$AWS_SECRET_ACCESS_KEY > input2.ds.json

# screwjack gen_ds \
#     --ds_type=http \
#     --ds_url=http://nlp.stanford.edu/courses/NAACL2013/NAACL2013-Socher-Manning-DeepLearning.pdf \
#     > input2.ds.json

screwjack gen_ds \
    --ds_type=hdfs \
    --ds_url=hdfs://10.10.0.162/tmp/movielens/big/ratings.csv \
    > input2.ds.json

touch output.hdfs

screwjack run docker \
    --param-hdfs_root="hdfs://10.10.0.162" \
    --param-yarn_resourcemanager="10.10.0.162:8032" \
    --param-yarn_resourcemanager_scheduler="10.10.0.162:8030" \
    --DS=input2.ds.json \
    --dest_hdfs=output.hdfs && \
    cat output.hdfs

