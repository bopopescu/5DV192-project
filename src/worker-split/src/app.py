import threading
import time
from flask import Flask, json
from flask_cors import CORS
import requests
from app_google.urls import app_google
from app_main import app_main
import urllib.request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_main)
app.register_blueprint(app_google)


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
            service_port = "5005"
        else:
            master_ip = "35.228.95.170"
            service_port = "5001"

        # runtime

        print("Thread KeepConnectionThread started!")
        request_url = "http://" + master_ip + ":5000/worker/connect"
        request_data = {"ip": get_ip()}

        while 1:
            try:
                print("Connecting to master...")
                #print("Sent: " + json.dumps(request_data) + " to " + request_url)
                res = requests.post(request_url, json=request_data)
                res = res.status_code
                if res == 200:
                    print("Successfully connected to master!")
                else:
                    print("Received: " + str(res))

                url = "http://" + master_ip + ":" + service_port + "/worker/connect/split"
                res = requests.post(url, json=request_data)
                res = res.status_code
                if res == 200:
                    print("Successfully connected service_port!")
                else:
                    print("Received: " + str(res))
            except Exception:
                pass
            time.sleep(5)


IS_DEBUG = True

if __name__ == '__main__':

    print("Thread KeepConnectionThread starting...")
    keep_connection_thread = KeepConnectionThread(name="KeepConnectionThread")
    keep_connection_thread.start()

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5001)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)


@app_main.route('/')
def main_route():
    return "Split node " + get_ip()


@app_main.route('/isActive', methods=['POST'])
def main_is_active():
    return "Split node " + get_ip()
