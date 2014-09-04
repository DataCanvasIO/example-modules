touch ./output_dir.dir
# screwjack run docker --param-hdfs_root=hdfs://192.168.1.20/tmp/ --param-Sqoop2Server_Host=192.168.1.20 --param-Sqoop2Server_Port=12000 --message_dir=./output.msg_dir
screwjack run local \
    --param-hdfs_root=hdfs://10.10.0.114/ \
    --param-Sqoop2Server_Host=10.10.0.114 \
    --param-Sqoop2Server_Port=12000 \
    --param-connection_string="$ZET_CONNECTION_STRING" \
    --param-connection_username="$ZET_CONNECTION_USERNAME" \
    --param-connection_password="$ZET_CONNECTION_PASSWORD" \
    --param-input_columns "AUserid,BUserid,A2B,AType" \
    --param-partition_column "AUserid" \
    --param-table_name "dbo.MatchResult" \
    --param-where_clause "" \
    --output_dir=./output_dir.dir
#rm -f ./input_dir.dir
