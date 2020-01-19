from . import app_main

from app_google.google_bucket import GoogleBucket

import time
import uuid as uuid

import requests
from flask import request, json, jsonify
import uuid

import app
from app_main.utils import json_response


workers_upload = []
metrics = []
index = 0

@app_main.route('/')
def worker_root():
    return "Master node"


@app_main.route('/worker/connect', methods=['POST'])
def route_worker_connect():
    global workers_upload
    data = request.json
    if data['ip'] != 'null':
        if data and data['ip'] not in set(workers_upload):
            workers_upload.append(data['ip'])
        if data and data['ip'] not in set(metrics):
            metrics.append(data['ip'])
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
            #print("Check ip...")
            # check if ip is active, if not active remove it from pool
            try:
                if app.IS_DEBUG:
                    request_url = "http://" + worker_ip + ":5001/isActive"
                else:
                    request_url = "http://" + worker_ip + ":5000/isActive"
                res = requests.post(request_url, json={"test": "test"})
                res = res.status_code
                #print(res)
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


@app_main.route('/client/retrieve', methods=['POST'])
def route_client_retrieve():
    data = request.json

    print("data retrieve: ")
    print(data)

    if data:

        id = data['id']
        gcloud_folder_path = "finished/" + id
        file_name = id + ".mp4"
        bucket_name = "umu-5dv192-project-eka"
        bucket = GoogleBucket(bucket_name)

        timeout = time.time() + 60*10

        while True:
            if time.time() > timeout:
                return json_response({"response": "error: connection timed out"}, 201)
            if bucket.file_exist(bucket_name, gcloud_folder_path, file_name):
                break
            time.sleep(1)

        url = "https://storage.cloud.google.com/umu-5dv192-project-eka/finished/" + id + "/" + id + ".mp4"
        return json_response({"downloadUrl": url}, 200)

    else:

        return json_response({"response": "invalid request"}, 201)

