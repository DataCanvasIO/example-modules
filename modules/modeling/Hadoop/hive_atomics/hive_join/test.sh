#!/bin/bash


TEST_CLUSTER=${TEST_CLUSTER:-hdp_sandbox}

screwjack gen_ds --ds_type hive --ds_url "sample_07" > input_a.ds

screwjack gen_ds --ds_type hive --ds_url "sample_08" > input_b.ds

screwjack run local \
       --param-cluster $TEST_CLUSTER \
       --param-selected_columns "a.code,b.salary" \
       --param-on_condition "a.code = b.code" \
       --param-join_type "inner" \
       --table_a input_a.ds \
       --table_b input_b.ds \
       --joined_table output.ds


