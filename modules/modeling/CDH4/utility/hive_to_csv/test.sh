#!/bin/bash

echo "xiaolin_sa_groupcount_result" > input.input_tbl
screwjack run local \
    --param-Host=10.10.0.87 \
    --param-Port=10000 \
    --param-Where_Clause="" \
    --param-LIMIT=10 \
    --param-SCHEMA="*" \
    --input_tbl=./input.input_tbl \
    --O=tmp.csv
