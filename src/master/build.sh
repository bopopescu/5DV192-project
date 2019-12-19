#!/bin/bash

# config
GCLOUD_USERNAME="superadmin"
GCLOUD_CREDENTIALS="credentials.json"
GCLOUD_PROJECT="testproject-261510"
GCLOUD_BUILD_NAME="master-build-1"
GCLOUD_VM_NAME="master-vm-1"
GCLOUD_ZONE="europe-north1-a"

# env
PATH=$PATH:../../apps/google-cloud-sdk/bin

# runtime
gcloud auth activate-service-account ${GCLOUD_USERNAME}@${GCLOUD_PROJECT}.iam.gserviceaccount.com --key-file=${GCLOUD_CREDENTIALS} --project=${GCLOUD_PROJECT}
gcloud config set project ${GCLOUD_PROJECT}
gcloud builds submit --tag gcr.io/${GCLOUD_PROJECT}/${GCLOUD_BUILD_NAME}
gcloud compute instances create-with-container ${GCLOUD_VM_NAME} --container-image gcr.io/${GCLOUD_PROJECT}/${GCLOUD_BUILD_NAME} --zone=${GCLOUD_ZONE}