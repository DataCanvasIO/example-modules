# sqoop1_import_hdfs

# VERSION : 0.1

FROM zetdata/cdh:new
# MAINTAINER Your_name, Your_email_address

# TODO: add JDBC drivers
# http://www.cloudera.com/content/cloudera/en/documentation/core/v5-3-x/topics/cdh_ig_jdbc_driver_install.html
RUN apt-get install libmysql-java libpostgresql-jdbc-java && \
    curl -L 'http://download.microsoft.com/download/0/2/A/02AAE597-3865-456C-AE7F-613F99F850A8/sqljdbc_4.0.2206.100_enu.tar.gz' | tar xz && \
    cp sqljdbc_4.0/enu/sqljdbc4.jar /usr/share/java/ && \
    rm -rf sqljdbc_4.0

ADD requirements.txt /home/run/
RUN pip install -r /home/run/requirements.txt

ADD spec.json /home/run/
ADD main.py /home/run/

