#!/bin/bash
virtualenv -p python3 env
source env/bin/activate
pip3 install -r src/server/requirements.txt
