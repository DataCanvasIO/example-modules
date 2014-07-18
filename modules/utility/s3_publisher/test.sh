#!/bin/bash

echo "s3n://xiaolin/review_results_by_datacanvas" > input.s3_path
touch output.sink_http

screwjack run local \
    --param-AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
    --param-AWS_ACCESS_KEY_SECRET="$AWS_SECRET_ACCESS_KEY" \
    --param-Metadata_Type="application/json" \
    --s3_path=input.s3_path \
    --list_html=output.sink_http

