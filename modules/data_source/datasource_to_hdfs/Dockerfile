# datasource_to_hdfs

# VERSION : 0.1

FROM zetdata/cdh:new
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

ADD requirements.txt /home/run/
RUN pip install -r /home/run/requirements.txt

ADD spec.json /home/run/
ADD main.py /home/run/
