#!/bin/bash

download() {
    local url=$1
    local target_file=$2
    local retry_count=10

    if [ -z "$target_file" ]
    then
        target_file=$(basename $url)
    fi
    echo "Downloading '$url' to '$target_file'..."
    for i in `seq 1 $retry_count`; do
        wget -O $target_file $url && \
            break || \
            sleep 10
    done
}

##########
# Main
##########

echo "Prebuilding for sentiment analysis..."

download https://s3.amazonaws.com/datacanvas-modules/demo_recommendation/mahout-core-1.0-SNAPSHOT-job.jar
