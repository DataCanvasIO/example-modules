#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from specparser import HadoopRuntime, cmd

def upload_s3_to_hdfs(hr, settings, ds):

    # Prepare working directory
    hr.hdfs_clean_working_dir()

    output_dir = hr.get_hdfs_working_dir("dest_hdfs")

    AWS_ACCESS_KEY_ID = ds["Meta"]["key"]
    AWS_SECRET_ACCESS_KEY = ds["Meta"]["token"]

    hadoop_params = {}
    hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}
    jar_defs["fs.s3n.awsAccessKeyId"] = '"%s"' % AWS_ACCESS_KEY_ID
    jar_defs["fs.s3n.awsSecretAccessKey"] = '"%s"' % AWS_SECRET_ACCESS_KEY
    jar_defs["fs.s3.awsAccessKeyId"] = '"%s"' % AWS_ACCESS_KEY_ID
    jar_defs["fs.s3.awsSecretAccessKey"] = '"%s"' % AWS_SECRET_ACCESS_KEY
    jar_defs["mapreduce.framework.name"] = "yarn"
    jar_defs["yarn.resourcemanager.address"] = settings.Param.yarn_resourcemanager
    jar_defs["yarn.resourcemanager.scheduler.address"] = settings.Param.yarn_resourcemanager_scheduler
    jar_defs["fs.defaultFS"] = settings.Param.hdfs_root
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])

    cmd_str = '%s hadoop distcp %s %s %s' % (hadoop_params_str, jar_defs_str, ds['URL'], output_dir)
    print("Executing:")
    print(cmd_str)
    ret = cmd(cmd_str)
    print("exit code = %d" % ret)
    if ret != 0:
        sys.exit(ret)

    return {
        "Name": "Dummy datasource : %s" % output_dir,
        "Type": "HDFS",
        "URL": output_dir,
        "Meta": {}
    }

def upload_url_to_hdfs(hr, settings, ds):
    # Prepare working directory
    hr.hdfs_clean_working_dir()
    output_dir = hr.get_hdfs_working_dir("dest_hdfs")

    hadoop_params = {}
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}
    jar_defs["fs.defaultFS"] = settings.Param.hdfs_root
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])

    cmd_str = 'wget -q -O - %s | hadoop fs -put - %s' % (ds["URL"], output_dir)
    print("Executing:")
    print(cmd_str)
    ret = cmd(cmd_str)
    print("exit code = %d" % ret)
    if ret != 0:
        sys.exit(ret)

    return {
        "Name": "Dummy datasource : %s" % output_dir,
        "Type": "HDFS",
        "URL": output_dir,
        "Meta": {}
    }

def main():
    hr = HadoopRuntime("spec.json")
    settings = hr.settings
    print(settings)

    ds = json.load(open(settings.Input.DS))


    if ds['Type'] in ["Http", "LocalFile", "Http", "Ftp"]:
        ds_output = upload_url_to_hdfs(hr, settings, ds)
    elif ds['Type'] in ["AWS_S3"]:
        ds_output = upload_s3_to_hdfs(hr, settings, ds)
    elif ds['Type'] in ["HDFS"]:
        ds_output = ds
    else:
        raise ValueError("Invalid type for input datasource: '%s'" % ds['Type'])

    settings.Output.dest_hdfs.val = json.dumps(ds_output)
    print("Done")

if __name__ == "__main__":
    main()
