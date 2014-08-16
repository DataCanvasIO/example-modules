# forecast

# VERSION : 0.1

FROM zetdata/r:3.0.2
# MAINTAINER Your_name, Your_email_address

ADD install_packages.R /home/run/
RUN /usr/bin/Rscript /home/run/install_packages.R

ADD spec.json /home/run/
ADD main.py /home/run/
ADD specparser.py /home/run/
ADD forecast.R /home/run/

