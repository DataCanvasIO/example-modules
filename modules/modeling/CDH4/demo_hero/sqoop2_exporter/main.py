#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
from pysqoop2 import MySqoop, pp, parse_jdbc, pymssql_delete_table

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    sqoop = MySqoop(settings.Param.Sqoop2Server_Host, int(settings.Param.Sqoop2Server_Port))

    # 1. Create an connection
    conn_name = "exporter_job%s_blk%s" % (
            settings.GlobalParam["jobId"],
            settings.GlobalParam["blockId"])
    conn_ret = sqoop.create_connection(conn_name=conn_name,
            conn_str=settings.Param.connection_string,
            username=settings.Param.connection_username,
            password=settings.Param.connection_password)

    # 2. empty the table
    print "Deleting the Table %s" % settings.Param.table_name
    conn_str = settings.Param.connection_string
    cfg = parse_jdbc(conn_str)
    cfg["username"] = settings.Param.connection_username
    cfg["password"] = settings.Param.connection_password
    #pymssql_delete_table(cfg, settings.Param.table_name)

    # 3. Run sqoop export job
    print "Running Sqoop2 Job to Export"
    fw_ps = {
        "input.inputDirectory": settings.Input.hdfs_path.val
   }
    job_ps = {
        "table.tableName": settings.Param.table_name,
        "table.columns": settings.Param.table_columns
    }
    job_name = "export job :: username(%s) job %s, block %s" % (
            settings.GlobalParam["userName"],
            settings.GlobalParam["jobId"],
            settings.GlobalParam["blockId"])

    r = sqoop.create_export_job(job_name=job_name,
                                connection_id=conn_ret["id"],
                                framework_params=fw_ps,
                                job_params=job_ps)
    pp(r)
    sqoop.run_job(r['id'])
    sqoop.wait_job(r['id'])
    sqoop.delete_job(r['id'])

    # Finally, Delete connection we created
    #sqoop.delete_connection_by_id(conn_ret["id"])

    print("Done")

if __name__ == "__main__":
    main()
