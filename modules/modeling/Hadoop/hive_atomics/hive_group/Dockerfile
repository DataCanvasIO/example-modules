# hive_group

# VERSION : 0.1

FROM zetdata/cdh:new
# MAINTAINER Your_name, Your_email_address

#RUN apt-get install -y hive

ADD requirements.txt /home/run/
RUN pip install -r /home/run/requirements.txt

ADD spec.json /home/run/
ADD main.py /home/run/
ADD main.hql /home/run/
ADD resources /home/run/resources/
