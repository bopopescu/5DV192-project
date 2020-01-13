from flask import request

from app_main.utils import json_response
from . import app_main


@app_main.route('/')
def worker_root():
    return "Hello World from Flask!"


@app_main.route('/worker/connect', methods=['POST'])
def route_worker_connect():

    if request.method == 'POST':

        print(request)

    return json_response({"status": "success"}, 200)
