FROM ubuntu:18.04

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && \
    apt-get install -y python3 python3-pip python3-tk libglib2.0-0 libsm6 libxrender-dev libxext-dev
RUN pip3 install --upgrade pip
RUN pip3 install numpy pandas flask jinja2 requests gunicorn[gevent] sqlalchemy 
RUN pip3 install psycopg2

ADD ./src/searchserver /project/hdbguru/searchserver

WORKDIR /project/hdbguru/searchserver