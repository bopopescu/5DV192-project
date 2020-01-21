#!/bin/bash
cd ../..
source env/bin/activate
pip3 install -r requirements.txt
cd src/master-service-registry/src
python3 app.py
