# db_dumper

# VERSION : 0.1

FROM zetdata/sci-python:2.7
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

RUN apt-get update && apt-get install -y python-dev libpq-dev

ADD requirements.txt /home/run/
RUN pip install -r /home/run/requirements.txt

ADD spec.json /home/run/
ADD main.py /home/run/
