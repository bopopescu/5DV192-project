import threading
import time
from flask import Flask, json, request
from flask_cors import CORS
import requests
import urllib.request

from merge.merge import Merge

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')

def get_ip():
    try:
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except Exception:
        print("Unable to get Hostname and IP")
        exit(-1)

@app.route('/')
def main_route():
    return "Merge node " + get_ip()


@app.route('/isActive', methods=['POST'])
def main_is_active():
    return "merge node " + get_ip()

class KeepConnectionThread(threading.Thread):

    def run(self):

        # config

        if IS_DEBUG:
            main_ip = "127.0.0.1"
            service_registry_port = "5005"
        else:
            main_ip = "35.228.95.170"
            service_registry_port = "5005"

        # runtime
        url_service_registry = "http://" + main_ip + ":" + service_registry_port + "/worker/connect/merge"
        request_data = {"ip": get_ip()}

        while 1:
            try:

                res = requests.post(url_service_registry, json=request_data, timeout=5)
                res = res.status_code

                if res == 200:
                    print("Successfully connected service registry!")
                else:
                    print("Received: " + str(res))

            except Exception:
                print("Error connecting to main and/or service registry")
                pass
            time.sleep(5)


class KeepMergeThread(threading.Thread):

    def run(self):
        merge = Merge()
        merge.start_rabbitMQ()

IS_DEBUG = False

if __name__ == '__main__':

    keep_connection_thread = KeepConnectionThread(name="KeepConnectionThread")
    keep_connection_thread.start()

    merge_thread = KeepMergeThread(name="keepMergeThread")
    merge_thread.start()

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5003)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)



