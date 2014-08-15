
echo "something " > input.txt
screwjack run local \
  --param-hdfs_root  hdfs://192.168.1.20 \
  --param-HiveServer2_Host 192.168.1.20 \
  --param-HiveServer2_Port 10000 \
  --param-FILE_DIR ./resources/files \
  --param-UDF_DIR  ./resources/udfs \
  --param-topN 1 \
  --input_table ./input.txt \
  --output_table ./output.txt


