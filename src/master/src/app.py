import os
import subprocess
import threading
import time
import requests
from flask import Flask, g
from flask_cors import CORS
from flask import request, json
from app_google.google_bucket import GoogleBucket
import logging
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

IS_DEBUG = False

metrics = []
index = 0


def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')


def get_split_workers():

    url_service_registry = "http://35.228.95.170:5005/worker/get/"

    code = 0
    workers_split = []

    while code != 200:

        print("Retrieving workers...")

        try:

            res = requests.get(url_service_registry, timeout=5)
            code = res.status_code

            print(res)

            if code == 200:
                workers = res.json()
                print(workers)
                workers_split = workers['split']
                print(workers_split)

        except Exception as e:
            print(e)

        time.sleep(1)

    return workers_split


def get_worker():

    global index

    ip = "null"

    while ip == "null":

        workers_split = get_split_workers()

        try:
            ip = workers_split[index]
            index += 1
        except Exception:
            index = 0
            ip = "null"

    return ip


def get_threshold(minutes):
    return time.time() + 60*minutes


class KeepScalerAlive(threading.Thread):

    def run(self):

        # config

        ip = "34.89.115.86"
        port = "5000"

        # runtime

        url_main = "http://" + ip + ":" + port
        time_wait = 120

        while 1:

            print("Keeping alive...")

            try:
                res = requests.get(url_main, json={}, timeout=5)
                print(res.status_code)
                if res.status_code != 200:
                    self.terraform_restart()
                    time.sleep(time_wait)
            except Exception as e:
                print(e)
                self.terraform_restart()
                time.sleep(time_wait)

            time.sleep(1)

    def terraform_restart(self):

        print("Restarting scaler...")

        path_script = os.path.join(app.root_path, "../terraform/scaler")

        if IS_DEBUG:
            terraform = "../../../../apps/terraform"
        else:
            terraform = "terraform"

        try:
            out = subprocess.check_output([terraform, "init"], cwd=path_script)
            print(out.decode('UTF-8').rstrip())
            out = subprocess.check_output([terraform, "apply", "-auto-approve"], cwd=path_script)
            print(out.decode('UTF-8').rstrip())
        except subprocess.CalledProcessError as e:
            print("Error in subprocess: \n", e.output)


@app.route('/')
def worker_root():
    return "Main node"


@app.route('/isActive', methods=['GET'])
def main_is_active():
    return "main node"


@app.route('/client/connect', methods=['GET'])
def route_client_connect():
    return json_response({"ip": get_worker()}, 200)


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


LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "flask_google_cloud_logger.FlaskGoogleCloudFormatter",
            "application_info": {
                "type": "python-application",
                "application_name": "Example Application"
            },
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "handlers": {
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        }
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["json"]
        },
        "werkzeug": {
            "level": "WARN",  # Disable werkzeug hardcoded logger
            "handlers": ["json"]
        }
    }
}

config.dictConfig(LOG_CONFIG)  # load log config from dict
logger = logging.getLogger("root")  # get root logger instance
FlaskGoogleCloudLogger(app)

@app.teardown_request  # log request and response info after extension's callbacks
def log_request_time(_exception):
    logger.info(
        f"{request.method} {request.path} - Sent {g.response.status_code}" +
        " in {g.request_time:.5f}ms")


if __name__ == '__main__':

    keep_scaler_alive = KeepScalerAlive(name="KeepScalerAlive")
    keep_scaler_alive.start()

    if IS_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)

