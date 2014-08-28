#!/bin/bash

echo "hdfs://10.10.0.162/user/hive/warehouse/tfidfcosineupdate" > input.hdfs_path

screwjack run local \
    --param-Sqoop2Server_Host "10.10.0.162" \
    --param-Sqoop2Server_Port "12000" \
    --param-connection_string="$ZET_CONNECTION_STRING" \
    --param-connection_username="$ZET_CONNECTION_USERNAME" \
    --param-connection_password="$ZET_CONNECTION_PASSWORD" \
    --param-table_name "dbo.UserMatch" \
    --hdfs_path "input.hdfs_path"
