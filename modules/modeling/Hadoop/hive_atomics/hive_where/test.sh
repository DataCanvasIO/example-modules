#!/bin/bash


TEST_CLUSTER=${TEST_CLUSTER:-hdp_sandbox}

screwjack gen_ds --ds_type hive --ds_url "sample_07" > input.ds

screwjack run local \
       --param-cluster $TEST_CLUSTER \
       --param-select_columns "*" \
       --param-where "salary > 20000" \
       --from_table input.ds \
       --filtered_table output.ds


