#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
#sudo docker run -d -p 80:80 nginx
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/master:latest
#sudo docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 -p 15692:15692 rabbitmq:3-management
sudo docker run -d -e RABBITMQ_NODENAME=my-rabbit --name my-rabbit -p 5672:5672 -p 15672:15672 -p 15692:15692 -p 9419:9419 rabbitmq:3-management
sudo docker run -d --net=container:my-rabbit kbudde/rabbitmq-exporter
