import uuid as uuid
from flask import request, json, jsonify
import uuid

from app_main.utils import json_response
from . import app_main


workers_upload = []
index = 0

@app_main.route('/')
def worker_root():
    workers_upload.append("1")
    workers_upload.append("2")
    workers_upload.append("3")
    workers_upload.append("4")
    workers_upload.append("5")
    workers_upload.append("6")
    workers_upload.append("7")
    workers_upload.append("8")
    workers_upload.append("9")
    return "Master node"


@app_main.route('/worker/connect', methods=['POST'])
def route_worker_connect():

    global workers_upload
    data = request.json

    print("Received data: ")
    print(data)

    if request.method == 'POST':

        if data['ip'] not in set(workers_upload):
            workers_upload.append(data['ip'])

        print(workers_upload)

    return json_response({"status": "success"}, 200)


@app_main.route('/client/connect', methods=['GET'])
def route_client_connect():

    global index
    worker_ip = round_robin()
    return json_response({"ip": worker_ip}, 200)


def round_robin():

    global workers_upload
    global index

    ip = "null"

    try:
        ip = workers_upload[index]
        index += 1
    except Exception:
        index = 0
        ip = workers_upload[index]

    print("workers upload")
    print(workers_upload)
    print("ip")
    print(ip)
    print("index")
    print(index)

    return ip




