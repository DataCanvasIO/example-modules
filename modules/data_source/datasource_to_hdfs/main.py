#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import sarge
from datacanvas.new_runtime import DataCanvas
from datacanvas.io_types import DS_HDFS
from datacanvas.utils import mask_key
dc = DataCanvas(__name__)

def check_returncodes(ret_codes):
    print("exit code = %s" % ret_codes)
    return all(v == 0 for v in ret_codes)

def upload_s3_to_hdfs(rt, ds):

    output_dir = rt.get_working_dir("dest_hdfs")

    hadoop_params = {}
    # hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}

    if "key" in ds["Meta"] and "token" in ds["Meta"]:
        AWS_ACCESS_KEY_ID = ds["Meta"]["key"]
        AWS_SECRET_ACCESS_KEY = ds["Meta"]["token"]
        jar_defs["fs.s3n.awsAccessKeyId"] = '"%s"' % AWS_ACCESS_KEY_ID
        jar_defs["fs.s3n.awsSecretAccessKey"] = '"%s"' % AWS_SECRET_ACCESS_KEY
        jar_defs["fs.s3.awsAccessKeyId"] = '"%s"' % AWS_ACCESS_KEY_ID
        jar_defs["fs.s3.awsSecretAccessKey"] = '"%s"' % AWS_SECRET_ACCESS_KEY

    sec_keys = ["fs.s3n.awsAccessKeyId", "fs.s3n.awsSecretAccessKey",
                "fs.s3.awsAccessKeyId", "fs.s3.awsSecretAccessKey"]

    jar_defs_sec = { k: mask_key(v) if k in sec_keys else v for k,v in jar_defs.items() }

    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])
    jar_defs_sec_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs_sec.items()])
    cmd_str = '%s hadoop distcp %s %s %s' % (hadoop_params_str, jar_defs_str, ds['URL'], output_dir)
    cmd_str_sec = '%s hadoop distcp %s %s %s' % (hadoop_params_str, jar_defs_sec_str, ds['URL'], output_dir)
    print("Executing:")
    print(cmd_str_sec)

    ret = sarge.run(cmd_str, env=rt.cluster.env_vars)
    if not check_returncodes(ret.returncodes):
        sys.exit(-1)

    return DS_HDFS(URL=output_dir)

def upload_url_to_hdfs(rt, ds):
    output_dir = rt.get_working_dir("dest_hdfs")

    hadoop_params = {}
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])

    cmd_str = 'wget -q -O - %s | hadoop fs -put - %s' % (ds["URL"], output_dir)
    print("Executing:")
    print(cmd_str)

    ret = sarge.run(cmd_str, env=rt.cluster.env_vars)
    if not check_returncodes(ret.returncodes):
        sys.exit(-1)

    return DS_HDFS(URL=output_dir)


@dc.hadoop_runtime(spec_json="spec.json")
def mymodule(rt, params, inputs, outputs):
    import datacanvas
    print datacanvas.__version__
    jar_step_args = []

    # TODO: Execute your jar
    # Method 1 : Execute local jar
    # rt.execute_jar("./your_project.jar", jar_step_args)
    # Method 2 : Execute jar in s3
    # rt.execute_jar("s3n://your_bucket/your_project.jar", jar_step_args)

    ds = inputs.DS.val
    if ds['Type'] in ["Http", "LocalFile", "Http", "Ftp"]:
        ds_output = upload_url_to_hdfs(rt, ds)
    elif ds['Type'] in ["AWS_S3"]:
        ds_output = upload_s3_to_hdfs(rt, ds)
    elif ds['Type'] in ["HDFS"]:
        ds_output = ds
    else:
        raise ValueError("Invalid type for input datasource: '%s'" % ds['Type'])

    print ds
    print ds_output
    outputs.dest_hdfs.val = ds_output
    print("Done")


if __name__ == "__main__":
    dc.run()
