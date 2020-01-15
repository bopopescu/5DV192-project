#!/bin/bash
cd ../..
source env/bin/activate
pip3 install -r requirements.txt
cd src/worker-split/src
python3 app.py
