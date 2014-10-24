#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from specparser import get_settings_from_file


def main():
    settings = get_settings_from_file("spec.json")


#    os.system("SPARK_HOME=/home/ansibler/work/spark/spark-1.1.0-bin-cdh4")
    os.system('''SPARK_HOME=/home/run/spark-1.1.0-bin-cdh4 && $SPARK_HOME/bin/spark-submit --class \"com.zetdata.hero.trial.SimpleApp\" \
--master %s \
--num-executors 3 --driver-memory 1024m  --executor-memory 1024m   --executor-cores 1 \
--conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:MaxPermSize=1024m" \
/home/run/spark_word_segement.jar \
%s %s %s '''  %(settings.Param.spark_host,settings.Input.rs_dir,settings.Input.jd_dir,settings.Output.match_result ))
    print("Done")

if __name__ == "__main__":
    main()
