import time
import uuid as uuid
from flask import request, json, jsonify
import uuid

from app_main.utils import json_response
from . import app_main


workers_upload = []
index = 0

@app_main.route('/')
def worker_root():
    return "Master node"


@app_main.route('/worker/connect', methods=['POST'])
def route_worker_connect():

    global workers_upload
    data = request.json

    if request.method == 'POST':

        if data['ip'] not in set(workers_upload):
            if data['ip'] != 'null':
                workers_upload.append(data['ip'])

    return json_response({"status": "success"}, 200)


@app_main.route('/client/connect', methods=['GET'])
def route_client_connect():

    global index

    worker_ip = "null"

    while worker_ip == "null":
        worker_ip = round_robin()
        time.sleep(1)

    return json_response({"ip": worker_ip}, 200)


def round_robin():

    global workers_upload
    global index

    try:
        ip = workers_upload[index]
        index += 1
    except Exception:
        index = 0
        return "null"

    print("Registered workers:")
    print(workers_upload)

    return ip




