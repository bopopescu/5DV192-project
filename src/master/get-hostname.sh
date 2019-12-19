#!/bin/bash
PATH=$PATH:../../apps/google-cloud-sdk/bin
gcloud compute instances describe $1 --format='get(networkInterfaces[0].accessConfigs[0].natIP)' --zone $2