#!/bin/bash
PATH=$PATH:../../../../apps/google-cloud-sdk/bin
echo $PATH
gcloud auth activate-service-account superadmin@testproject-261510.iam.gserviceaccount.com --key-file=$1 --project=testproject
gcloud config get-value account
gsutil cp gs://umu-5dv192-project-eka/uploaded/input.mkv $2
