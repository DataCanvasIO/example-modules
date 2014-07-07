echo "hdfs://10.10.0.90/tmp/jiaqi/messageh/" >> ./input.hdfs
touch ./output.tmp
screwjack run docker \
    --param-hdfs_root=hdfs://10.10.0.90/tmp/ \
    --param-HiveServer2_Host=10.10.0.90 \
    --param-HiveServer2_Port=10000 \
    --param-FILE_DIR=./resources/files \
    --param-UDF_DIR=./resources/udfs \
    --param-SCHEMA="userid int, raw_message string, tsp timestamp" \
    --input=./input.hdfs \
    --output=./output.tmp
rm -f ./input.hdfs ./output.tmp
