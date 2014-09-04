#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import sys
from specparser import HiveRuntime, cmd

def main():
    hr = HiveRuntime()
    
    hdfs_input_dir =  hr.settings.Input.input_dir.val
    hdfs_input_dir =  os.path.join(hdfs_input_dir,'')
    
    output_dir = hr.get_hdfs_working_dir("output_dir")
    output_dir =  os.path.join(output_dir,'')
    output_filename = os.path.join(output_dir, "merged_file")
    
    hadoop_del_dir  = "hadoop fs -rm -r %s " % output_dir
    print hadoop_del_dir
    ret = cmd(hadoop_del_dir)
    print "prepare(delete output dir successfully)"

    hadoop_shell = "hadoop fs -mkdir %s && hadoop fs -text %s/* | hadoop fs -put - %s" %(output_dir,hdfs_input_dir,output_filename)
    print hadoop_shell
    ret = cmd(hadoop_shell)
    if ret !=0:
        sys.exit(ret)
    hr.settings.Output.output_file.val = output_filename

    print("Done")

if __name__ == "__main__":
    main()
