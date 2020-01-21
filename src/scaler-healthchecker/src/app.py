import threading
import time
from flask import Flask
from flask_cors import CORS
import requests
import urllib.request

from urls import Converter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

IS_DEBUG = True


class KeepConnectionThread(threading.Thread):

    def run(self):

        # config

        master_ip = "35.228.95.170"
        master_port = "5000"

        # runtime

        url_master = "http://" + master_ip + ":" + master_port + "/isActive"

        while 1:

            try:

                res = requests.post(url_master, json={})
                res = res.status_code

                if res == 200:
                    print("Successfully connected to master!")
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


if __name__ == '__main__':

    keep_connection_thread = KeepConnectionThread(name="KeepConnectionThread")
    keep_connection_thread.start()

    '''converter_thread = KeepConvertThread(name="KeepConvertThread")
    converter_thread.start()'''

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5002)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)


@app.route('/')
def main_route():
    return "Converter node"


@app.route('/isActive', methods=['POST'])
def main_is_active():
    return "scaler " + get_ip()

