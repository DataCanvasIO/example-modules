#!/bin/bash

TEST_CLUSTER="${TEST_CLUSTER:-hdp_sandbox}"

touch output_obj.json

screwjack run local \
    --param-cluster $TEST_CLUSTER \
    --param-connect_string "jdbc:mysql://192.168.1.52:3306/retail_db" \
    --param-username "retail_dba" \
    --param-password "cloudera" \
    --param-table "orders" \
    --param-additional_params "--delete-target-dir --as-textfile" \
    --param-target_dir "hdfs://192.168.1.51/tmp/my_orders/" \
    --O "output_obj.json"


# screwjack run local \
#     --param-cluster emr_cluster \
#     --param-connect_string "jdbc:postgresql://registry.datacanvas.io:5432/booktown" \
#     --param-username "xiaolin" \
#     --param-password "XiaolinAtZetyun" \
#     --param-table "books" \
#     --param-additional_params "-m 1 --delete-target-dir --as-textfile" \
#     --param-target_dir "hdfs://192.168.1.51/tmp/booktown_books/" \
#     --O "output_obj.json"
