import io
import threading
import time
from flask import Flask, json, request
from flask_cors import CORS
import requests
from app_google.urls import app_google
from app_main import app_main
import urllib.request

from app_main.utils import json_response

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_main)
app.register_blueprint(app_google)


workers_split = []
workers_convert = []
workers_merge = []

IS_DEBUG = True


def get_ip():
    try:
        return urllib.request.urlopen('https://ident.me').read().decode('utf8')
    except Exception:
        print("Unable to get Hostname and IP")
        exit(-1)

@app_main.route('/')
def main_route():
    return "service registry"


@app_main.route('/worker/connect/split', methods=['POST'])
def route_workers_split():
    global workers_split
    data = request.json
    if data['ip'] != 'null':
        if data and data['ip'] not in set(workers_split):
            workers_split.append(data['ip'])
    return json_response({"status": "success"}, 200)


@app_main.route('/worker/connect/converter', methods=['POST'])
def route_workers_convert():
    global workers_convert
    data = request.json
    if data['ip'] != 'null':
        if data and data['ip'] not in set(workers_convert):
            workers_convert.append(data['ip'])
    return json_response({"status": "success"}, 200)


@app_main.route('/worker/connect/merge', methods=['POST'])
def route_workers_merge():
    global workers_merge
    data = request.json
    if data['ip'] != 'null':
        if data and data['ip'] not in set(workers_merge):
            workers_merge.append(data['ip'])
    return json_response({"status": "success"}, 200)


@app_main.route('/service_registry', methods=['POST'])
def route_service_registry():

    global workers_split
    global workers_convert
    global workers_merge
    global IS_DEBUG

    print("-- start queue -- ")
    print(workers_split)
    print(workers_convert)
    print(workers_merge)
    print("-- end queue -- ")


    for ip in workers_split:
        if IS_DEBUG:
            request_url_split = "http://" + "localhost" + ":5001/isActive"
        else:
            request_url_split = "http://" + ip + ":5000/isActive"
        try:
            res = requests.post(request_url_split)
            if not res.status_code == 200:
                print("Status Code error")
                workers_split.remove(ip)
        except:
            print("Not able to connect")
            workers_split.remove(ip)

    for ip in workers_convert:
        if IS_DEBUG:
            request_url_convert = "http://" + "localhost" + ":5002/isActive"
        else:
            request_url_convert = "http://" + ip + ":5000/isActive"
        print(request_url_convert)
        try:
            res = requests.post(request_url_convert)
            if not res.status_code == 200:
                print("Status Code error")
                workers_convert.remove(ip)
        except:
            print("Not able to connect")
            workers_convert.remove(ip)

    for ip in workers_merge:
        if IS_DEBUG:
            request_url_merge = "http://" + "localhost" + ":5003/isActive"
        else:
            request_url_merge = "http://" + ip + ":5000/isActive"
        print(request_url_merge)

        try:
            res = requests.post(request_url_merge)
            if not res.status_code == 200:
                print("Status Code error")
                workers_merge.remove(ip)
        except:
            print("Not able to connect")
            workers_merge.remove(ip)

    return json_response({"status": "success"}, 200)



def check_service_registry():
    my_ip = get_ip()

    while(True):
        if IS_DEBUG:
            request_url = "http://" + "localhost" + ":5005/service_registry"
        else:
            request_url = "http://" + my_ip + ":5001/service_registry"
        res = requests.post(request_url)
        if not res.status_code == 200:
            print("ERROR: CAN't ping myself")
            return
        time.sleep(1)


def create_target_json(workers_split, workers_convert, workers_merge):
    workers_split = ["35.228.66.169"]
    workers_convert = ["35.228.66.169"]
    workers_merge = ["35.228.66.169"]

    json_list = []
    for ip in workers_split:
        split_json = {}
        split_json['labels'] = {"env": "prod", "job": "split"}
        split_json['targets'] = [ip + ":8080", ip + "8080"]
        json_list.append(split_json)


    for ip in workers_convert:
        convert_json = {}
        convert_json['labels'] = {"env": "prod", "job": "convert"}
        convert_json['targets'] = [ip + ":8080", ip + "8080"]
        json_list.append(convert_json)

    for ip in workers_merge:
        merge_json = {}
        merge_json['labels'] = {"env": "prod", "job": "merge"}
        merge_json['targets'] = [ip + ":8080", ip + "8080"]
        json_list.append(merge_json)


    print(json_list)
    with io.open('target.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_list, ensure_ascii=False))




if __name__ == '__main__':
    create_target_json()

    thread = threading.Thread(target=check_service_registry, args=())
    thread.start()

    if IS_DEBUG:
        app.run(debug=False, host='0.0.0.0', port=5005)
    else:
        app.run(debug=False, host='0.0.0.0', port=5001)
    thread.join()





