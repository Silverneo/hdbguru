
[Reference 1](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
[Reference 2](https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9)

### VPC & EC2


1. Choose AMI Amazon Linux 2
2. When adding security role, remember to add port 31001 which is for our api

### Docker Setup

```
sudo yum update
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
sudo reboot
docker info # make sure can see info
```

```
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version # verify to see version info
```

### Backend

#### Clone the github repository

```
sudo yum install -y git
git clone https://github.com/Silverneo/hdbguru-data-etl.git && cd hdbguru-data-etl
```

#### Copy data & .env over to the folder
```
cd db/data && mkdir _processed && cd _processed
wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_HAWKER_ADDR_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_HDB_ADDR_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_HDB_EXTRA_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_HDB_PROP_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_HDB_RESALE_PRICE.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_MALL_ADDR_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_MRT_LRT_ADDR_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_SCHOOL_INFO.csv.gzip\
&& wget https://hdbguru-s3-processed.s3.amazonaws.com/TBL_SMKT_ADDR_INFO.csv.gzip
```

#### Build Images and Spin Up the Service
```
docker-compose build && docker-compose up -d
docker exec -it hdbguru_db_1 bash ./run_migrate.sh up
curl "http://localhost:31001"
```
