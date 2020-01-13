#
# By Kaj Nygren, Alexander Ekström, Erik Dahlberg
# December 2019
#
import socket
import time

from flask import Flask, request, json, g
from flask_cors import CORS
import requests
import logging
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger

from app_google.urls import app_google
from app_main.urls import app_main


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# blueprints
app.register_blueprint(app_main)
app.register_blueprint(app_google)

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

    # config
    master_ip = "127.0.0.1"
    worker_ip = socket.gethostname()

    # connect to master
    request_url = "http://" + master_ip + ":5000/worker/connect"
    request_data = {"ip": worker_ip}

    res = 0
    while res != 200:
        time.sleep(2)
        try:
            print("Connecting to master...")
            print("Sending request to master: " + request_url + " " + json.dumps(request_data))
            res = requests.post(request_url, json=request_data)
            res = res.status_code
            print("Got response from master: " + str(res))
        except Exception as e:
            print("Connection error. Retrying...")

    print("Connected to master!")

    app.run(debug=True, host='0.0.0.0', port=5003)
