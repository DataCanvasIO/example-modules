# recommendation_mahout

# VERSION : 0.1

FROM zetdata/cdh:4
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

RUN pip install boto

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD mahout-core-1.0-SNAPSHOT-job.jar /home/run/
