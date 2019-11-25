#!/bin/bash
source env/bin/activate
pip3 install -r requirements
cd src
python3 main.py
