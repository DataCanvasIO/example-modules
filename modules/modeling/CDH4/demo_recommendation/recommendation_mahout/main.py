#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
from collections import OrderedDict
import boto
import json
import os
import sys
import subprocess

def cmd(cmd_str):
    ret = subprocess.call(cmd_str, shell=True)
    return ret

def s3_delete(s3_path, settings):
    from urlparse import urlparse
    pr = urlparse(s3_path)
    if pr.scheme != "s3" and pr.scheme != "s3n":
        raise ValueError("Invalid scheme for path: '%s'" % s3_path)

    p = settings.Param
    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    bucket = s3_conn.get_bucket(pr.netloc)

    print("s3_delete %s" % s3_path)
    prefix_path = urlparse(s3_path).path[1:]
    for key in bucket.list(prefix=prefix_path):
        key.delete()
    return True

def get_s3_working_dir(settings, path=""):
    ps = settings
    p = settings.Param
    glb_vars = ps.GlobalParam

    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    s3_bucket = s3_conn.get_bucket(p.S3_BUCKET)
    
    remote_path = os.path.normpath(os.path.join(s3_bucket.name, 'zetjob', glb_vars['userName'], "job%s" % glb_vars['jobId'], "blk%s" % glb_vars['blockId'], path))
    return os.path.join("s3n://", remote_path)

def main():
    hr = HadoopRuntime("spec.json")
    settings = hr.settings
    print(settings)

    # allocate output_path, and clean it
    output_path = get_s3_working_dir(settings, "output_path")
    s3_delete(output_path, settings)

    # Prepare working directory
    hr.hdfs_clean_working_dir()
    temp_path = hr.get_hdfs_working_dir("temp")

    # build parameters for hadoop job
    jar_file = "mahout-core-1.0-SNAPSHOT-job.jar"
    hadoop_params = {}
    hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}
    jar_defs["fs.s3n.awsAccessKeyId"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_ID
    jar_defs["fs.s3n.awsSecretAccessKey"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_SECRET
    jar_defs["fs.s3.awsAccessKeyId"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_ID
    jar_defs["fs.s3.awsSecretAccessKey"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_SECRET
    jar_defs["mapreduce.framework.name"] = "yarn"
    jar_defs["yarn.resourcemanager.address"] = settings.Param.yarn_resourcemanager
    jar_defs["yarn.resourcemanager.scheduler.address"] = settings.Param.yarn_resourcemanager_scheduler
    jar_defs["fs.defaultFS"] = settings.Param.hdfs_root
    jar_defs["mapreduce.output.fileoutputformat.compress"] = "false"
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])

    other_args = OrderedDict()
    other_args["similarityClassname"] = "SIMILARITY_EUCLIDEAN_DISTANCE"
    other_args["input"] = settings.Input.ratings.as_datasource['URL']
    other_args["usersFile"] = settings.Input.usersFile.as_datasource['URL']
    other_args["output"] = output_path
    other_args["tempDir"] = temp_path
    other_args_str = " ".join(["--%s %s" % (k,v) for k,v in other_args.items()])

    cmd_str = '%s hadoop jar %s org.apache.mahout.cf.taste.hadoop.item.RecommenderJob %s %s' % \
            (hadoop_params_str, jar_file, jar_defs_str, other_args_str)
    print("Executing:")
    print(cmd_str)
    ret = cmd(cmd_str)
    if ret != 0:
        print("Job failed")
        sys.exit(ret)

    settings.Output.output_path.val = output_path
    print("Done")

if __name__ == "__main__":
    main()
