#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
from pysqoop2 import MySqoop, pp

def main():
    # settings = get_settings_from_file("spec.json")
    # print(settings)
    hr = HadoopRuntime()
    settings = hr.settings
    print(settings)
    hr.clean_working_dir()
    output_dir = hr.get_hdfs_working_dir("message_dir")

    sqoop = MySqoop(settings.Param.Sqoop2Server_Host, int(settings.Param.Sqoop2Server_Port))
    fw_ps = {
        "output.storageType": "HDFS",
        "output.outputFormat": "TEXT_FILE",
        "output.outputDirectory": output_dir
    }
    job_ps = {
        "table.sql": "select UserId,Description,RefreshDate from Message where ${CONDITIONS}",
        "table.partitionColumn": "UserId"
    }
    r = sqoop.create_import_job(job_name="zdwechat message",
                                connection_name="zdwechat message",
                                framework_params=fw_ps,
                                job_params=job_ps)
    pp(r)
    sqoop.run_job(r['id'])
    sqoop.wait_job(r['id'])

    print("Done")

if __name__ == "__main__":
    main()
