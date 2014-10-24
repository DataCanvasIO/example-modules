# hero_cos_matc_spark

# VERSION : 0.1

FROM zetdata/cdh:4
# MAINTAINER Your_name, Your_email_address

RUN apt-get install -y hive

ADD spark_word_segement.jar /home/run/
ADD spark-1.1.0-bin-cdh4/ /home/run/spark-1.1.0-bin-cdh4/
ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
