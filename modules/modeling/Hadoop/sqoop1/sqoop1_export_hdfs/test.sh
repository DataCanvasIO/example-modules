#!/bin/bash

TEST_CLUSTER="${TEST_CLUSTER:-hdp_sandbox}"

screwjack gen_ds --ds_type=hdfs --ds_url="hdfs://192.168.1.51/tmp/my_orders/" > input_obj.ds

screwjack run local \
    --param-cluster $TEST_CLUSTER \
    --param-connect_string "jdbc:mysql://192.168.1.52:3306/retail_db" \
    --param-username "retail_dba" \
    --param-password "cloudera" \
    --param-table "new_orders" \
    --param-additional_params "" \
    --I "input_obj.ds"
