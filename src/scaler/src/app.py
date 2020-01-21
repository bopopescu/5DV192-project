import json
import os
import threading
import time
from flask import Flask
from flask_cors import CORS
import requests

from rabbit_mq import RabbitMQ


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


class AutomaticScaling(threading.Thread):

    def run(self):

        rabbit_mq = RabbitMQ(RABBITMQ_IP)

        previous_length = 0

        while 1:

            current_length = 0

            # wait for 1 minute
            for i in range(0, 60):

                rabbit_mq.create_channel()
                current_length += rabbit_mq.get_queue_length('convert_queue')
                time.sleep(1)

            num_machines = current_length / previous_length

            if current_length > previous_length:
                self.scale_up(num_machines)
            else:
                self.scale_down(num_machines)

            previous_length = current_length
            time.sleep(180)

        rabbit_mq.close_connection()

    def scale_up(self):
        print("scale_up")

    def scale_down(self):
        print("scale down")


if __name__ == '__main__':

    '''keep_master_alive = KeepMasterAlive(name="KeepMasterAlive")
    keep_master_alive.start()'''

    automatic_scaling = AutomaticScaling(name="AutomaticScaling")
    automatic_scaling.start()

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5002)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)


@app.route('/')
def main_route():
    return "Converter node"


@app.route('/isActive', methods=['POST'])
def main_is_active():
    return "Scaler"




'''
 1. Hämta lista med convert noder from service-regeistry   (service-registry håller kolla på aktiva noder JUST NU)
 2. Kolla länge på list ger dig antalet aktiva convert noder som finns just nu
 3. Fråga rabbitMQ om convert queue length
 4. Är queue length längre än 10 starta ny nod
 5. Är queue length kortare än 5 och vi har mer än 3 noder ta bort en nod.  
'''