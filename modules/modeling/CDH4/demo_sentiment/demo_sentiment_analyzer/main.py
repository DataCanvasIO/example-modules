#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
import json
import os
import sys
import subprocess

def cmd(cmd_str):
    ret = subprocess.call(cmd_str, shell=True)
    return ret

def main():
    hr = HadoopRuntime("spec.json")
    settings = hr.settings
    print(settings)

    ds = json.load(open(settings.Input.DS))

    if ds['Type'] != "AWS_S3":
        raise ValueError("Invalid data_source type: '%s'" % ds['Type'])

    # Prepare working directory
    hr.hdfs_clean_working_dir()
    output_dir = hr.get_hdfs_working_dir("sentiment_result")
    settings.Output.sentiment_result.val = output_dir

    AWS_ACCESS_KEY_ID = ds['Meta']['key']
    AWS_SECRET_ACCESS_KEY = ds['Meta']['token']

    # Execute "hadoop jar"
    jar_file = "HelloAvro-1.1-jar-with-dependencies.jar"
    hadoop_params = {}
    hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params["AWS_ACCESS_KEY_ID"] = ds['Meta']['key']
    hadoop_params["AWS_SECRET_ACCESS_KEY"] = ds['Meta']['token']
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

    cmd_str = '%s hadoop jar %s %s %s %s' % (hadoop_params_str, jar_file, jar_defs_str, ds['URL'], output_dir)
    print("Executing:")
    print(cmd_str)
    ret = cmd(cmd_str)
    print("exit code = %d" % ret)
    sys.exit(ret)

if __name__ == "__main__":
    main()
