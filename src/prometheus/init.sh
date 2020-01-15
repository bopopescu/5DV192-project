#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
sudo docker run -p 9090:9090 gcr.io/testproject-261510/prometheus:latest

