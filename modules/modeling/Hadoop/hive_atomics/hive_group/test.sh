#!/bin/bash


TEST_CLUSTER=${TEST_CLUSTER:-hdp_sandbox}

screwjack gen_ds --ds_type hive --ds_url "sample_07" > input.ds

screwjack run local \
       --param-cluster $TEST_CLUSTER \
       --param-selected_columns "salary, count(1)" \
       --param-group_by_columns "salary" \
       --from_table input.ds \
       --grouped_table output.ds


