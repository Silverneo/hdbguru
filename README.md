## HDBguru Data ETL

### Setup searchserver
1. Run build.sh to build docker image

### Setup Postgres Database

1. Check with Chunmeng for .env which includes the db creds

2. Copy over contents of data (those dirs starting with _) from team's share folder

3. Run below commands to bring up the db locally with data

```
# start postgis db and search server
docker-compose build && docker-compose up -d

# run required migration sql scripts
docker exec -it hdbguru_db_1 bash ./run_migrate.sh up
```

You can adjust database stage by running above command with up / down / goto [x]

For details on how to use migrate, refer to their [cli guide](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate)

### Test
```
curl "http://localhost:31001"

curl "http://localhost:31001/api/v1/get_neighbor_detail?latitude=1.3489086885502&longitude=103.876715676102&topn=2"

curl "http://localhost:31001/api/v1/get_nearby_hdb?where=531008&topn=20"
```