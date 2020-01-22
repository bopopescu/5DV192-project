#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker

sudo apt-get -y install wget unzip
wget https://releases.hashicorp.com/terraform/0.12.19/terraform_0.12.19_linux_amd64.zip
unzip terraform_0.12.19_linux_amd64.zip
sudo mv terraform /usr/local/bin/

sudo docker rm $(docker ps -a -q) # stop and delete all old containers
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/scaler:latest
