#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from specparser import HadoopRuntime


def main():
    hr = HadoopRuntime()
    settings = hr.settings
    output_dir = hr.get_hdfs_working_dir("some_path")
    settings.Output.match_result.val = output_dir


#    os.system("SPARK_HOME=/home/ansibler/work/spark/spark-1.1.0-bin-cdh4")
    os.system('''SPARK_HOME=/home/run/spark-1.1.0-bin-cdh4 && $SPARK_HOME/bin/spark-submit --class \"com.zetdata.hero.trial.SimpleApp\" \
--master %s \
--num-executors 3 --driver-memory 1024m  --executor-memory 1024m   --executor-cores 1 \
--conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:MaxPermSize=1024m" \
/home/run/spark_word_segement.jar \
%s %s %s '''  %(settings.Param.spark_host,settings.Input.rs_dir.val,settings.Input.jd_dir.val,settings.Output.match_result.val ))
    print("Done")

if __name__ == "__main__":
    main()
