touch ./output.msg_dir
# screwjack run docker --param-hdfs_root=hdfs://192.168.1.20/tmp/ --param-Sqoop2Server_Host=192.168.1.20 --param-Sqoop2Server_Port=12000 --message_dir=./output.msg_dir
screwjack run docker --param-hdfs_root=hdfs://10.10.0.90/tmp/ --param-Sqoop2Server_Host=10.10.0.90 --param-Sqoop2Server_Port=12000 --message_dir=./output.msg_dir
rm -f ./output.msg_dir
