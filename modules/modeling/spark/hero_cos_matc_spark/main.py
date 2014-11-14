#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from specparser import HadoopRuntime


def main():
    hr = HadoopRuntime()
    settings = hr.settings
    match_result_output_dir = hr.get_hdfs_working_dir("match_result")
    settings.Output.match_result.val = match_result_output_dir
    match_analysis_output_dir = hr.get_hdfs_working_dir("match_analysis")
    settings.Output.match_analysis.val = match_analysis_output_dir

#SPARK_HOME=/home/run/spark-1.1.0-bin-cdh4 
#/home/run/spark_word_segement.jar
#    os.system("SPARK_HOME=/home/ansibler/work/spark/spark-1.1.0-bin-cdh4")
    os.system('''SPARK_HOME=/home/run/spark-1.1.0-bin-cdh4 \
&& $SPARK_HOME/bin/spark-submit --class \"com.zetdata.hero.trial.SimpleApp\" \
--master %s \
--num-executors 3 --driver-memory 1024m  --executor-memory 1024m   --executor-cores 1 \
--conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:MaxPermSize=1024m" \
/home/run/spark_word_segement.jar \
%s %s %s %s %s '''  %(settings.Param.spark_host,
                      settings.Input.jd_dir.val,
                      settings.Input.rs_dir.val,
                      settings.Output.match_result.val,
                      settings.Output.match_analysis.val,
                      settings.Input.white_dict.val
                      ))
    print("Done")

if __name__ == "__main__":
    main()
