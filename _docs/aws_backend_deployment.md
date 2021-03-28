
[Reference 1](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
[Reference 2](https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9)

### VPC & EC2


1. Choose AMI Amazon Linux 2
2. When adding security role, remember to add port 31001 which is for our api

### Docker Setup

```
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

#### Copy data over to the folder

#### Build Images and Spin Up the Service
```
docker-compose build && docker-compose up -d
docker exec -it hdbguru_db_1 bash ./run_migrate.sh up
curl "http://localhost:31001"
```
