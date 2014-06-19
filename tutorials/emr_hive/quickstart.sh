#!/bin/bash

echo "This is not a script to run. Please read throught this script"
exit

readonly MODULE_NAME=test_emrhive
readonly MODULE_USERNAME=your_username

# docker's limit image name to lowercase
readonly MODULE_PATH=${MODULE_USERNAME,,}/${MODULE_NAME,,}

redonly AWS_ACCESS_KEY_ID="your_aws_key_id"
redonly AWS_ACCESS_KEY_SECRET="your_aws_key_secret"
redonly S3_BUCKET="your_bucket"
redonly Region="us-east-1"
redonly EMR_jobFlowId="your_emr_job_flow_id"

screwjack init emr_hive -n $MODULE_NAME -d "Test module for basic" -v "0.1" -c "python main.py" -b "zetdata/ubuntu:trusty"

cd $MODULE_NAME

screwjack param_add topN string

screwjack input_add query_log_dir_s3_dir hive.s3.query_log_dir_s3_dir
screwjack output_add hot_token_topN_s3_dir hive.s3.hot_token_topn_s3_dir
echo "s3n://get-hot-token-kk/input/query" > input.s3
cp ../files/jiaqi.hql main.hql
cp ../files/my-app-1.0-SNAPSHOT.jar resources/udfs

screwjack run local --param-AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --param-AWS_ACCESS_KEY_SECRET=$AWS_ACCESS_KEY_SECRET --param-S3_BUCKET=$S3_BUCKET --param-AWS_Region=$Region --param-EMR_jobFlowId=$EMR_jobFlowId --param-FILE_DIR=./resources/files/ --param-UDF_DIR=./resources/udfs/ --param-topN=10 --query_log_dir_s3_dir=input.s3 --hot_token_topN_s3_dir=output.s3

screwjack run docker --param-AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --param-AWS_ACCESS_KEY_SECRET=$AWS_ACCESS_KEY_SECRET --param-S3_BUCKET=$S3_BUCKET --param-AWS_Region=$Region --param-EMR_jobFlowId=$EMR_jobFlowId --param-FILE_DIR=./resources/files/ --param-UDF_DIR=./resources/udfs/ --param-topN=10 --query_log_dir_s3_dir=input.s3 --hot_token_topN_s3_dir=output.s3
