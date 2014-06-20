# hot_site_topN

# VERSION : 0.1

FROM zetdata/ubuntu:trusty
MAINTAINER Jiaqi Guo, <guojq@zetyun.com>

RUN pip install boto

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD main.pig /home/run/
ADD resources /home/run/resources/
