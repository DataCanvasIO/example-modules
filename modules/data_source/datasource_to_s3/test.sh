#!/bin/bash

set -x

touch output.s3

screwjack run local \
    --param-AWS_ACCESS_KEY_ID="" \
    --param-AWS_ACCESS_KEY_SECRET="" \
    --param-S3_BUCKET="xiaolin" \
    --DS=input2.ds.json \
    --dest_s3=output.s3 && \
    cat output.s3
