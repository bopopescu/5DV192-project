import json
import os
import subprocess
import threading
import time
from flask import Flask, request, g
from flask_cors import CORS
import requests
from rabbit_mq import RabbitMQ
import logging
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

IS_DEBUG = True
RABBITMQ_IP = "35.228.95.170"


def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')


def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


class KeepMasterAlive(threading.Thread):

    def run(self):

        # config

        master_ip = "35.228.95.170"
        master_port = "5000"

        # runtime

        url_master = "http://" + master_ip + ":" + master_port
        time_wait = 120

        while 1:

            print("Keeping alive...")

            try:
                res = requests.get(url_master, json={}, timeout=5)
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

        print("Restarting master...")

        path_script = os.path.join(app.root_path, "../terraform/master")

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



class AutomaticScaling(threading.Thread):

    def run(self):

        # config
        time_wait = 120
        worker_convert_folder = "worker-convert"
        worker_merge_folder = "worker-merge"
        rabbitmq_convert_queue = "convert_queue"
        rabbitmq_merge_queue = "merge_queue"

        rabbit_mq = RabbitMQ(RABBITMQ_IP)
        size_convert_previous = 0
        size_merge_previous = 0

        while 1:

            size_convert = 0
            size_merge = 0

            # gather metrics for 1 minute
            for i in range(0, 60):

                rabbit_mq.create_channel()

                try:
                    size_convert_i = rabbit_mq.get_queue_length(rabbitmq_convert_queue)
                    size_merge_i = rabbit_mq.get_queue_length(rabbitmq_merge_queue)
                except Exception:
                    break

                print("Size convert: " + str(size_convert_i))
                print("Size merge: " + str(size_merge_i))

                size_convert += size_convert_i
                size_merge += size_merge_i

                time.sleep(1)

            self.scale_init(size_convert, size_convert_previous, worker_convert_folder)
            self.scale_init(size_merge, size_merge_previous, worker_merge_folder)

            size_convert_previous = size_convert
            size_merge_previous = size_merge
            time.sleep(time_wait)

    def scale_init(self, size, size_previous, worker_type):

        if size == size_previous:
            # do not scale
            num_workers = 2
        elif size > size_previous:
            # scale up
            num_workers = 3
        else:
            # scale down
            num_workers = 1

        self.scale(num_workers, worker_type)

    def scale(self, num_workers, worker_type):

        print("Scaling to {" + str(num_workers) + "} workers")

        path_script = os.path.join(app.root_path, "../terraform/" + worker_type)

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
def main_route():
    return "Scaler"


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

    keep_master_alive = KeepMasterAlive(name="KeepMasterAlive")
    keep_master_alive.start()

    '''automatic_scaling = AutomaticScaling(name="AutomaticScaling")
    automatic_scaling.start()'''

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5011)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)




