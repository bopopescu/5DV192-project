#!/bin/bash

# config

GCLOUD_USERNAME="superadmin"
GCLOUD_PROJECT="testproject-261510"
GCLOUD_BUILD_NAME="convert"

GCLOUD_FILE_CREDENTIALS="src/credentials.json"

# env

PATH=$PATH:../../apps/google-cloud-sdk/bin

# runtime

gcloud auth activate-service-account ${GCLOUD_USERNAME}@${GCLOUD_PROJECT}.iam.gserviceaccount.com --key-file=${GCLOUD_FILE_CREDENTIALS} --project=${GCLOUD_PROJECT}
gcloud config set project ${GCLOUD_PROJECT}
gcloud builds submit --tag gcr.io/${GCLOUD_PROJECT}/${GCLOUD_BUILD_NAME}
