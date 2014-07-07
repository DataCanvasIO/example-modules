echo "tf_table" > input1.tbl
echo "idf_table" > input2.tbl
touch output.tbl
screwjack run docker --param-hdfs_root=hdfs://10.10.0.90/tmp/ \
    --param-HiveServer2_Host=10.10.0.90 \
    --param-HiveServer2_Port=10000 \
    --param-FILE_DIR=./resources/files \
    --param-UDF_DIR=./resources/udfs \
    --input_table1=./input1.tbl \
    --input_table2=./input2.tbl \
    --output_table=./output.tbl

rm -f ./input1.tbl ./input2.tbl ./output.tbl
