# ds2hivetable_converter

# VERSION : 0.1

FROM zetdata/cdh:4
MAINTAINER Guo Jiaqi, guojq@zetyun.com

RUN apt-get install -y hive

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD main.hql /home/run/
ADD resources /home/run/resources/
