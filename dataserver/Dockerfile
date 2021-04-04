FROM python:3.9-slim-buster

ENV TZ=Asia/Singapore

RUN pip install --upgrade pip
RUN pip install numpy pandas requests sqlalchemy psycopg2-binary

ADD ./src /project/hdbguru/dataserver

WORKDIR /project/hdbguru/dataserver
