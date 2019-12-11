#!/bin/bash
source env/bin/activate
pip3 install -r requirements.txt
cd src
python3 app.py
