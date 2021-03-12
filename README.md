## HDBguru Data ETL

### Setup Postgres Database

1. Check with Chunmeng for .env which includes the db creds

2. Copy over contents of data (those dirs starting with _) from team's share folder

3. Run below commands to bring up the db locally with data

```
# start postgis db
docker-compose up -d

# run required migration sql scripts
bin\migrate -path data/migrations -database postgres://[uid]:[pwd]@127.0.0.1:5432/hdbguru goto 5
```
