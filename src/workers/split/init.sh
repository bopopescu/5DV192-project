#!/bin/bash
sudo curl -sSL https://get.docker.com/ | sh
sudo apt-get --yes --force-yes install ffmpeg
sudo usermod -aG docker `echo $USER`
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/split:latest

