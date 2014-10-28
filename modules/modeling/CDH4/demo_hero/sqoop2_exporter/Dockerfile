# sqoop2_exporter

# VERSION : 0.1

FROM zetdata/ubuntu:trusty
MAINTAINER Xiaolin Zhang, <zhangxl@zetyun.com>

RUN apt-get install -y freetds-dev python-dev
RUN pip install pymssql requests
RUN apt-get install -y python-psycopg2

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD pysqoop2.py /home/run/
