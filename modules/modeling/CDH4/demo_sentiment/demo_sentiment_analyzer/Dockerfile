# sentiment_analyzer

# VERSION : 0.1

FROM zetdata/cdh:4
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

RUN pip install boto

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD HelloAvro-1.0-SNAPSHOT-jar-with-dependencies.jar /home/run/
