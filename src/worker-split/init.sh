#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
sudo docker rm $(docker ps -a -q) # stop and delete all old containers
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/split:latest
sudo docker run -d -p 9100:9100 prom/node-exporter
