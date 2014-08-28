touch ./output.msg_dir
# screwjack run docker --param-hdfs_root=hdfs://192.168.1.20/tmp/ --param-Sqoop2Server_Host=192.168.1.20 --param-Sqoop2Server_Port=12000 --message_dir=./output.msg_dir
screwjack run docker \
    --param-hdfs_root=hdfs://10.10.0.162/tmp/ \
    --param-Sqoop2Server_Host=10.10.0.162 \
    --param-Sqoop2Server_Port=12000 \
    --param-connection_string="$ZET_CONNECTION_STRING" \
    --param-connection_username="$ZET_CONNECTION_USERNAME" \
    --param-connection_password="$ZET_CONNECTION_PASSWORD" \
    --message_dir=./output.msg_dir
rm -f ./output.msg_dir
