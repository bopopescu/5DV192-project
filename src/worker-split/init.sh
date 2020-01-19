#!/bin/bash
sudo apt-get update
sudo curl -sSL https://get.docker.com/ | sh
sudo systemctl start docker
sudo docker run -d -p 5000:5000 gcr.io/testproject-261510/split:latest
sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  gcr.io/google-containers/cadvisor:latest
