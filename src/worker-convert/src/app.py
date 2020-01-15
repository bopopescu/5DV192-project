from convert.converter import Converter

import threading
import time
from flask import Flask, json
from flask_cors import CORS
import requests
import urllib.request

from flask import Blueprint

app_main = Blueprint('app_main', __name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_main)


def get_ip():
    try:
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except Exception:
        print("Unable to get Hostname and IP")
        exit(-1)


class KeepConnectionThread(threading.Thread):

    def run(self):

        # config

        if IS_DEBUG:
            master_ip = "127.0.0.1"
        else:
            master_ip = "35.228.95.170"

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
            except Exception:
                pass
            time.sleep(5)


IS_DEBUG = False

if __name__ == '__main__':

    print("Thread KeepConnectionThread starting...")
    keep_connection_thread = KeepConnectionThread(name="KeepConnectionThread")
    keep_connection_thread.start()

    converter = Converter()
    converter.start_rabbitmq()

    if IS_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=5002)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)


@app_main.route('/')
def main_route():
    return "Split node " + get_ip()


@app_main.route('/isActive', methods=['POST'])
def main_is_active():
    return "convert node " + get_ip()
