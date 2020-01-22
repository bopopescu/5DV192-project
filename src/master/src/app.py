import time
import requests

from flask import Flask
from flask_cors import CORS
from flask import request, json
from app_google.google_bucket import GoogleBucket

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

IS_DEBUG = False

workers_upload = []
metrics = []
index = 0


def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')


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


def get_threshold(minutes):
    return time.time() + 60*minutes


@app.route('/')
def worker_root():
    return "Master node"

@app.route('/isActive', methods=['GET'])
def main_is_active():
    return "master node"


@app.route('/worker/connect', methods=['POST'])
def route_worker_connect():
    global workers_upload
    data = request.json
    if data['ip'] != 'null':
        if data and data['ip'] not in set(workers_upload):
            workers_upload.append(data['ip'])
        if data and data['ip'] not in set(metrics):
            metrics.append(data['ip'])
    return json_response({"status": "success"}, 200)


@app.route('/client/connect', methods=['GET'])
def route_client_connect():

    global index
    global workers_upload

    worker_ip = "null"

    while worker_ip == "null":

        worker_ip = round_robin()
        flag_for_deletion = False

        if worker_ip == "null":
            time.sleep(1)
        else:
            try:
                if IS_DEBUG:
                    request_url = "http://" + worker_ip + ":5001/isActive"
                else:
                    request_url = "http://" + worker_ip + ":5000/isActive"
                res = requests.post(request_url, json={"test": "test"}, timeout=3)
                res = res.status_code
                if res != 200:
                    flag_for_deletion = True
                else:
                    print(worker_ip)
            except Exception:
                flag_for_deletion = True

        if flag_for_deletion:
            print("Removing ip...")
            if worker_ip in workers_upload:
                workers_upload.remove(worker_ip)
            print(workers_upload)
            worker_ip = "null"

    return json_response({"ip": worker_ip}, 200)


@app.route('/client/retrieve', methods=['POST'])
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

        while True:
            if time.time() > get_threshold(10):
                return json_response({"response": "error: connection timed out"}, 201)
            if bucket.file_exist(bucket_name, gcloud_folder_path, file_name):
                break
            time.sleep(1)

        url = "https://storage.cloud.google.com/umu-5dv192-project-eka/finished/" + id + "/" + id + ".mp4"
        return json_response({"downloadUrl": url}, 200)

    else:

        return json_response({"response": "invalid request"}, 201)


if __name__ == '__main__':

    if IS_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)

