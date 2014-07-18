# Hive to CSV

# VERSION : 1.0

FROM zetdata/ubuntu:14.04
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

RUN apt-get install -y libsasl2-dev python-dev
RUN pip install pyhs2

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
