#
# By Kaj Nygren, Alexander Ekström, Erik Dahlberg
# December 2019
#
import socket
import threading
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

def get_ip():
    try:
        host_name = socket.gethostname()
        return socket.gethostbyname(host_name)
    except Exception as e:
        print("Unable to get Hostname and IP")
        exit(-1)


class KeepConnectionThread(threading.Thread):

    def run(self):

        # config

        #master_ip = "35.228.95.170"
        master_ip = "127.0.0.1"

        # runtime

        print("Thread KeepConnectionThread started!")
        request_url = "http://" + master_ip + ":5000/worker/connect"
        request_data = {"ip": get_ip()}

        while 1:
            try:
                print("Connecting to master...")
                print("Sent: " + json.dumps(request_data) + " to " + request_url)
                res = requests.post(request_url, json=request_data)
                res = res.status_code
                print("Received: " + str(res))
                if res == 200:
                    print("Successfully connected!")
                else:
                    print("Received: " + str(res))
            except Exception as e:
                pass
            time.sleep(5)


if __name__ == '__main__':

    print("Thread KeepConnectionThread starting...")
    keep_connection_thread = KeepConnectionThread(name="KeepConnectionThread")
    keep_connection_thread.start()

    app.run(debug=True, host='0.0.0.0', port=5003)
