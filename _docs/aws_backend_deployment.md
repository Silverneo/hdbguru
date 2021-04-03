
[Reference 1](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
[Reference 2](https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9)

### VPC & EC2


1. Choose AMI Amazon Linux 2
2. When adding security role, remember to add port 31001 which is for our api

### Docker Setup

```
sudo yum update -y
sudo amazon-linux-extras install -y docker
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
sudo yum install -y git
```

### Backend

#### create folder hdbguru, copy .env & docker-compose.yml into it

#### Pull Images and Spin Up the Service
```
docker-compose up -d
docker exec -it hdbguru_db_1 bash ./run_migrate.sh up # Update DB to latest
curl "http://localhost:31001" # check api backend is up
```
