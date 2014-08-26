# hivetable2hdfs_convertor

# VERSION : 0.1

FROM zetdata/ubuntu:trusty
MAINTAINER GuoJiaqi, guojq@zetyun.com
RUN apt-get install -y libsasl2-dev python-dev
RUN pip install pyhs2

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
