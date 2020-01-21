#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/scaler:latest
