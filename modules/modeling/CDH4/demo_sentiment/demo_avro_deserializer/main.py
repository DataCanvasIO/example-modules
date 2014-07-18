#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
from collections import OrderedDict
import boto
import json
import os
import sys

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

    # build parameters for hadoop job
    jar_file = "avro_tools/hadoop-streaming-2.0.0-mr1-cdh4.6.0.jar"
    hadoop_params = {}
    hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}
    jar_defs["mapred.job.name"] = "avro-streaming"
    jar_defs["mapred.reduce.tasks"] = "0"
    jar_defs["mapred.output.compress"] = "false"
    jar_defs["fs.s3n.awsAccessKeyId"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_ID
    jar_defs["fs.s3n.awsSecretAccessKey"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_SECRET
    jar_defs["fs.s3.awsAccessKeyId"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_ID
    jar_defs["fs.s3.awsSecretAccessKey"] = '"%s"' % settings.Param.AWS_ACCESS_KEY_SECRET
    jar_defs["mapreduce.framework.name"] = "yarn"
    jar_defs["yarn.resourcemanager.address"] = settings.Param.yarn_resourcemanager
    jar_defs["yarn.resourcemanager.scheduler.address"] = settings.Param.yarn_resourcemanager_scheduler
    jar_defs["fs.defaultFS"] = settings.Param.hdfs_root
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])

    other_args = OrderedDict()
    other_args["files"] = "avro_tools/avro-1.7.4-cdh4.5.0.2.jar,avro_tools/avro-mapred-1.7.4-cdh4.5.0.2-hadoop2.jar"
    other_args["libjars"] = "avro_tools/avro-1.7.4-cdh4.5.0.2.jar,avro_tools/avro-mapred-1.7.4-cdh4.5.0.2-hadoop2.jar"
    other_args["mapper"] = "org.apache.hadoop.mapred.lib.IdentityMapper"
    other_args["inputformat"] = "org.apache.avro.mapred.AvroAsTextInputFormat"
    other_args["input"] = settings.Input.avro_path.val
    other_args["output"] = output_path
    other_args_str = " ".join(["-%s %s" % (k,v) for k,v in other_args.items()])

    cmd_str = '%s hadoop jar %s %s %s' % (hadoop_params_str, jar_file, jar_defs_str, other_args_str)
    print("Executing:")
    print(cmd_str)
    ret = os.system(cmd_str)
    if ret != 0:
        print("Job failed")
        sys.exit(ret)

    settings.Output.output_path.val = output_path
    print("Done")

if __name__ == "__main__":
    main()
