
[Reference 1](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html)
[Reference 2](https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9)

### VPC & EC2


1. Choose AMI Amazon Linux 2
2. When adding security role, remember to add port 31001 which is for our api
3. For DB please bind the private ip to **10.0.2.222**

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

### Deploy

```
ssh [ssh_host_to_ec2]
mkdir -p hdbguru && exit
scp .env docker-compose.prod.yml Makefile [ssh_host_to_ec2]:~/hdbguru
ssh [ssh_host_to_ec2]
cd hdbguru
make deploy-[api/db/web]
```
