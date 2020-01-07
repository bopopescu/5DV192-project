 #!/bin/bash
PATH=$PATH:../../apps/google-cloud-sdk/bin

gcloud auth activate-service-account superadmin@testproject-261510.iam.gserviceaccount.com --key-file=credentials.json --project=testproject

gcloud config set project 'testproject-261510'

gcloud compute instances create-with-container master-1 \
    --container-image gcr.io/cloud-marketplace/google/nginx1:latest