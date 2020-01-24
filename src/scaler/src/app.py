import json
import os
import subprocess
import threading
import time
from flask import Flask, request, g
from flask_cors import CORS
import requests
from rabbit_mq import RabbitMQ

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

IS_DEBUG = False
URL_RABBIT_MQ = "35.228.95.170"
URL_SERVICE_REGISTRY = "http://35.228.95.170:5005/worker/get/"
URL_MASTER = "http://35.228.95.170:5000"


def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')


def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


# gather metrics for 1 minute
def get_queue_metrics(queue_name):

    rabbit_mq = RabbitMQ(URL_RABBIT_MQ)
    queue_size = 0

    for i in range(0, 5):
        rabbit_mq.create_channel()
        try:
            queue_size += rabbit_mq.get_queue_length(queue_name + "_queue")
            print(queue_name + ": " + queue_size)
        except Exception:
            break
        time.sleep(1)
    rabbit_mq.close_connection()
    return queue_size


def scale(worker_type):

    queue_length_previous = 0

    while 1:

        queue_length = get_queue_metrics(worker_type)
        num_workers = get_workers(worker_type)
        new_num_workers = scale_algorithm(num_workers, queue_length, queue_length_previous)
        terraform_dir = "worker-" + worker_type

        if num_workers != new_num_workers:
            print("Scaling to " + str(new_num_workers) + " " + worker_type + " workers (" + terraform_dir + ")")
            terraform_write_variables(terraform_dir, new_num_workers)
            terraform_provision(terraform_dir)
            time.sleep(180)
        else:
            print("No scaling needed for " + worker_type)

        queue_length_previous = queue_length


def scale_algorithm(num_workers, queue_length, queue_length_previous):

    min_workers = 1
    max_workers = 3

    if num_workers == 0:

        return min_workers

    else:

        if queue_length > queue_length_previous:
            # scale up
            num_workers = max_workers
        elif queue_length == 0 or queue_length < queue_length_previous:
            # scale down
            num_workers -= 1

        if num_workers < min_workers:
            num_workers = min_workers

        if num_workers > max_workers:
            num_workers = max_workers

        return num_workers


def terraform_write_variables(path, num_workers):
    print("Writing new variables.tf file...")
    file = os.path.join(app.root_path, "../terraform/" + path + "/variables.tf")
    text = "variable \"num_workers\" { default = " + str(num_workers) + " }"
    f = open(file, "w")
    f.write(text)
    f.close()

def terraform_provision(path):

    path_script = os.path.join(app.root_path, "../terraform/" + path)

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


def get_workers(worker_type):

    code = 0
    num_convert_workers = 0

    while code != 200:
        try:
            res = requests.get(URL_SERVICE_REGISTRY, timeout=5)
            code = res.status_code
            if code == 200:
                data = res.json()
                num_convert_workers = len(data[worker_type])
        except Exception as e:
            print(e)
        time.sleep(1)
    return num_convert_workers


class ScaleMaster(threading.Thread):

    def run(self):

        print("Starting ScaleMaster...")

        while 1:

            try:
                res = requests.get(URL_MASTER, json={}, timeout=5)
                if res.status_code != 200:
                    print("Starting new master...")
                    terraform_provision("master")
                    time.sleep(120)
            except Exception as e:
                print(e)
                terraform_provision("master")
                time.sleep(120)

            time.sleep(1)


class ScaleSplit(threading.Thread):

    def run(self):

        print("Starting ScaleSplit...")

        # config

        min_workers = 3
        terraform_dir = "worker-split"

        # runtime

        while 1:

            num_upload_workers = get_workers('split')
            print("Split workers: " + str(num_upload_workers))

            if num_upload_workers != min_workers:
                print("Provisioning new split workers...")
                terraform_provision(terraform_dir)
                time.sleep(120)

            time.sleep(1)


class ScaleMerge(threading.Thread):

    def run(self):
        print("Starting ScaleMerge...")
        scale("merge")


class ScaleConvert(threading.Thread):

    def run(self):
        print("Starting ScaleConvert...")
        scale("convert")


@app.route('/')
def main_route():
    return "Scaler"


if __name__ == '__main__':

    t1 = ScaleMaster(name="ScaleMaster")
    t1.start()

    t2 = ScaleSplit(name="ScaleSplit")
    t2.start()

    t3 = ScaleConvert(name="ScaleConvert")
    t3.start()

    t4 = ScaleMerge(name="ScaleMerge")
    t4.start()

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5011)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)




