import time
import uuid as uuid

import requests
from flask import request, json, jsonify
import uuid

import app
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

    print("data")
    print(data)

    if data and data['ip'] not in set(workers_upload):
        if data['ip'] != 'null':
            workers_upload.append(data['ip'])

    print("Registered workers:")
    print(workers_upload)

    return json_response({"status": "success"}, 200)


@app_main.route('/client/connect', methods=['GET'])
def route_client_connect():

    global index
    global workers_upload

    worker_ip = "null"

    while worker_ip == "null":

        worker_ip = round_robin()
        flagForDeletion = False

        if worker_ip == "null":
            time.sleep(1)
        else:
            print("Check ip...")
            # check if ip is active, if not active remove it from pool
            try:
                if app.IS_DEBUG:
                    request_url = "http://" + worker_ip + ":5001/isActive"
                else:
                    request_url = "http://" + worker_ip + ":5000/isActive"
                res = requests.post(request_url, json={"test": "test"})
                res = res.status_code
                print(res)
                if res != 200:
                    flagForDeletion = True
                else:
                    print(worker_ip)
            except Exception:
                flagForDeletion = True

        if flagForDeletion:
            print("Removing ip...")
            if worker_ip in workers_upload:
                workers_upload.remove(worker_ip)
            print(workers_upload)
            worker_ip = "null"



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




