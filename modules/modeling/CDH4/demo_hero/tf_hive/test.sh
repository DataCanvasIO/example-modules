echo "tokenh" > input.tbl
touch output.tbl
screwjack run docker --param-hdfs_root=hdfs://10.10.0.90/tmp/ \
    --param-HiveServer2_Host=10.10.0.90 \
    --param-HiveServer2_Port=10000 \
    --param-FILE_DIR=./resources/files \
    --param-UDF_DIR=./resources/udfs \
    --input_table=./input.tbl \
    --output_table=./output.tbl

rm -f ./input.tbl ./output.tbl
