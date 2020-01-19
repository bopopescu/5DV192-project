#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
sudo docker run -d -p 3000:3000 grafana/grafana
sudo docker run -p 9090:9090 --hostname=prometheus-01 -v prometheus-01:/etc/prometheus gcr.io/testproject-261510/prometheus:latest
