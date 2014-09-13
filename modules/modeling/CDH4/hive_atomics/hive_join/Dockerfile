# hive_join

# VERSION : 0.1

FROM zetdata/cdh:4
# MAINTAINER Your_name, Your_email_address
RUN apt-get install -y libsasl2-dev python-dev
RUN pip install pyhs2
RUN apt-get install -y hive


ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD main.hql /home/run/
ADD resources /home/run/resources/
