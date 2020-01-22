import threading
import time
from flask import Flask, json, request
from flask_cors import CORS
import requests
import urllib.request

from convert.converter import Converter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def get_ip():
    try:
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except Exception:
        print("Unable to get Hostname and IP")
        exit(-1)

def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')

@app.route('/')
def main_route():
    return "Converter node " + get_ip()


@app.route('/isActive', methods=['POST'])
def main_is_active():
    return "convert node " + get_ip()

class KeepConnectionThread(threading.Thread):

    def run(self):

        # config

        if IS_DEBUG:
            master_ip = "127.0.0.1"
            service_registry_port = "5005"
        else:
            master_ip = "35.228.95.170"
            service_registry_port = "5005"

        # runtime

        url_service_registry = "http://" + master_ip + ":" + service_registry_port + "/worker/connect/converter"
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
                print("Error connecting to master and/or service registry")
                pass
            time.sleep(5)


class KeepConvertThread(threading.Thread):

    def run(self):
        converter = Converter()
        converter.start_rabbitmq()


IS_DEBUG = False

if __name__ == '__main__':

    keep_connection_thread = KeepConnectionThread(name="KeepConnectionThread")
    keep_connection_thread.start()

    converter_thread = KeepConvertThread(name="KeepConvertThread")
    converter_thread.start()


    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5002)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)




