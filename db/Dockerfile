FROM postgis/postgis:13-master

RUN cd /tmp &&\
    curl -O -L -k https://github.com/golang-migrate/migrate/releases/latest/download/migrate.linux-amd64.tar.gz &&\
    tar -zxvf migrate.linux-amd64.tar.gz &&\
    mv migrate.linux-amd64 /usr/local/bin/migrate

WORKDIR /app

COPY data/migrations /app/migrations
COPY run_migrate.sh /app/run_migrate.sh
COPY run_psql.sh /app/run_psql.sh

COPY psql.up /app/psql.up
COPY psql.down /app/psql.down
COPY data/_processed /tmp/data/_processed

RUN chmod +x run_migrate.sh
RUN chmod +x run_psql.sh
