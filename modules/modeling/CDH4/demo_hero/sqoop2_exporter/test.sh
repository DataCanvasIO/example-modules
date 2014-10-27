#!/bin/bash

echo "hdfs://10.10.0.114/tmp/hero_postgre_export_test/" > input.hdfs_path

screwjack run docker \
    --param-Sqoop2Server_Host "10.10.0.114" \
    --param-Sqoop2Server_Port "12000" \
    --param-connection_string="jdbc:postgresql://118.192.89.126/hero" \
    --param-connection_username="hero" \
    --param-connection_password="Server2008!" \
    --param-table_name "\"UserMatch\"" \
    --hdfs_path "input.hdfs_path"
