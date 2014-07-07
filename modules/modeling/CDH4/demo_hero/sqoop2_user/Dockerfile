# sqoop2_user

# VERSION : 0.1

FROM zetdata/cdh:4
MAINTAINER Jiaqi Guo, guojq@zetyun.com

RUN apt-get install -y sqoop2-client

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD pysqoop2.py /home/run/
