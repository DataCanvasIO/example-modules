#!/bin/bash


TEST_CLUSTER=${TEST_CLUSTER:-hdp_sandbox}

screwjack gen_ds --ds_type hive --ds_url "sample_07" > input.ds

screwjack run local \
       --param-cluster $TEST_CLUSTER \
       --param-order_by_columns "salary" \
       --param-limit "10" \
       --from_table input.ds \
       --ordered_table output.ds


