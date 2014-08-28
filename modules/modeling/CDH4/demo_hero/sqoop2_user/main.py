#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
from pysqoop2 import MySqoop, pp

def main():
    hr = HadoopRuntime()
    settings = hr.settings
    print(settings)
    hr.clean_working_dir()
    output_dir = hr.get_hdfs_working_dir("user_dir")

    sqoop = MySqoop(settings.Param.Sqoop2Server_Host, int(settings.Param.Sqoop2Server_Port))

    # First, Create an connection
    conn_name = "import_u_job%s_blk%s" % (
            settings.GlobalParam["jobId"],
            settings.GlobalParam["blockId"])
    conn_ret = sqoop.create_connection(conn_name=conn_name,
            conn_str=settings.Param.connection_string,
            username=settings.Param.connection_username,
            password=settings.Param.connection_password)

    # Then, Run sqoop import job
    fw_ps = {
        "output.storageType": "HDFS",
        "output.outputFormat": "TEXT_FILE",
        "output.outputDirectory": output_dir
    }
    job_ps = {
        "table.sql": "select UserId, type from [User] where ${CONDITIONS}",
        "table.partitionColumn": "UserId"
    }
    job_name = "import job :: username(%s) job %s, block %s" % (
            settings.GlobalParam["userName"],
            settings.GlobalParam["jobId"],
            settings.GlobalParam["blockId"])
    r = sqoop.create_import_job(job_name=job_name,
                                connection_id=conn_ret["id"],
                                framework_params=fw_ps,
                                job_params=job_ps)
    pp(r)
    sqoop.run_job(r['id'])
    sqoop.wait_job(r['id'])
    sqoop.delete_job(r['id'])

    # Finally, Delete connection we created
    sqoop.delete_connection_by_id(conn_ret["id"])

    settings.Output.user_dir.val = output_dir

    print("Done")

if __name__ == "__main__":
    main()
