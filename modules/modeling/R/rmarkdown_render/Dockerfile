# rmarkdown_render

# VERSION : 0.1

# FROM zetdata/r:3.0.2
FROM rocker/ropensci:latest
MAINTAINER Xiaolin Zhang, zhangxl@zetyun.com

ADD install_packages.R /home/run/
RUN /usr/bin/Rscript /home/run/install_packages.R

ADD spec.json /home/run/
ADD main.R /home/run/
