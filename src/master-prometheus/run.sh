#!/bin/bash
cd ../..
source env/bin/activate
cd src/master-prometheus
pip3 install -r requirements.txt
cd src
python3 app.py
