#!/bin/bash
PATH=$PATH:../../apps/google-cloud-sdk/bin

gcloud auth activate-service-account docker@testproject-261510.iam.gserviceaccount.com --key-file=credentials-docker.json --project=testproject

gcloud config set project 'testproject-261510'

gcloud builds submit --tag gcr.io/testproject-261510/master-1
