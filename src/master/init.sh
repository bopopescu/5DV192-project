#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
#sudo docker run -d -p 80:80 nginx
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/master:latest
#sudo docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 -p 15692:15692 rabbitmq:3-management
sudo docker run -d -e RABBITMQ_NODENAME=my-rabbit --hostname rabbitmq-01 -p 5672:5672 -p 15672:15672 -p 15692:15692 -p 9419:9419 -v rabbitmq-01-data:/var/lib/rabbitmq rabbitmq:3-management
sudo docker run -d --net=container:my-rabbit kbudde/rabbitmq-exporter
sudo docker run -d -p 3000:3000 grafana/grafana
sudo docker run -d -p 9090:9090 --hostname=prometheus-01 -v prometheus-01:/etc/prometheus gcr.io/testproject-261510/prometheus:latest
sudo docker run -d -p 5005:5005 -v prometheus-01:/etc/prometheus gcr.io/testproject-261510/service-registry:latest
