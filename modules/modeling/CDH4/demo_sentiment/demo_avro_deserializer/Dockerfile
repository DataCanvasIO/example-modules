# avro_deserializer

# VERSION : 0.1

FROM zetdata/cdh:4
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

RUN pip install boto

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD avro_tools /home/run/avro_tools/
