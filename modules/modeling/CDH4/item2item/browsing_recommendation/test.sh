<<<<<<< HEAD

echo "something " > input.txt
screwjack run local \
=======
#!/bin/bash

echo "recm_raw_browsing" > input.txt
touch ./output.txt

screwjack run docker \
>>>>>>> a4faddbc419f09423d11a7e66584194e697b40fe
  --param-hdfs_root  hdfs://192.168.1.20 \
  --param-HiveServer2_Host 192.168.1.20 \
  --param-HiveServer2_Port 10000 \
  --param-FILE_DIR ./resources/files \
  --param-UDF_DIR  ./resources/udfs \
  --param-topN 1 \
  --input_table ./input.txt \
  --output_table ./output.txt


