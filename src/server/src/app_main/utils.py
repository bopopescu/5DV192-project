import os

from flask import json
from app import app


def json_response(message, status):
    return app.response_class(response=json.dumps(message), status=status, mimetype='application/json')


def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)
