#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
from collections import OrderedDict
import json
import os
import sys
import subprocess

def cmd(cmd_str):
    ret = subprocess.call(cmd_str, shell=True)
    return ret

def get_the_line_of_transaction(path):
    abs_path = os.path.join(path,'*')
    cmd_str = "hadoop fs -text %s | wc -l " % abs_path
    return cmd(cmd_str)

def main():
    hr = HadoopRuntime("spec.json")
    settings = hr.settings
    print(settings)

    # Prepare working directory
    hr.hdfs_clean_working_dir()
    # allocate temp_path
    temp_path = hr.get_hdfs_working_dir("temp")
    # allocate output_path
    output_path = hr.get_hdfs_working_dir("output_path")
    
    # build parameters for hadoop job
    jar_file = "./mahout-core-1.0-SNAPSHOT-job.jar"
    hadoop_params = {}
    hadoop_params["HADOOP_MAPRED_HOME"] = "/usr/lib/hadoop-mapreduce"
    hadoop_params_str = " ".join(["%s=%s" % (k,v) for k,v in hadoop_params.items()])

    jar_defs = {}
    jar_defs["mapreduce.framework.name"] = "yarn"
    jar_defs["yarn.resourcemanager.address"] = settings.Param.yarn_resourcemanager
    jar_defs["yarn.resourcemanager.scheduler.address"] = settings.Param.yarn_resourcemanager_scheduler
    jar_defs["fs.defaultFS"] = settings.Param.hdfs_root
    jar_defs["mapreduce.output.fileoutputformat.compress"] = "false"
    jar_defs_str = " ".join(["-D %s=%s" % (k,v) for k,v in jar_defs.items()])

    other_args = OrderedDict()
    other_args["similarityClassname"] = "SIMILARITY_EUCLIDEAN_DISTANCE"
    other_args["input"] = settings.Input.ratings.val
    other_args["usersFile"] = settings.Input.usersFile.val
    other_args["output"] = output_path
    other_args["tempDir"] = temp_path
    other_args_str = " ".join(["--%s %s" % (k,v) for k,v in other_args.items()])
    
    line_num =get_the_line_of_transaction(settings.Input.ratings.val)
    
    if line_num >0: 
        cmd_str = '%s hadoop jar %s org.apache.mahout.cf.taste.hadoop.item.RecommenderJob %s %s' % \
                (hadoop_params_str, jar_file, jar_defs_str, other_args_str)
        print("Executing:")
        print(cmd_str)
        ret = cmd(cmd_str)
        if ret != 0:
            print("Job failed")
            sys.exit(ret)
    else:
        print "Collaborative Input Transaction Matrix is empty. Skip the calcuating."   
    settings.Output.cl_result.val = output_path

    print("Done")

if __name__ == "__main__":
    main()
