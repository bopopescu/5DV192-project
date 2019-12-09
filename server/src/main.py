import os
from flask import Flask, request, json, jsonify
from flask_cors import CORS
from werkzeug.datastructures import ImmutableMultiDict

UPLOAD_FOLDER = 'upload'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/transcode/request', methods=['POST'])
def form_example():

    print("----------------------------------")
    print("TRANSCODE REQUEST")
    print("----------------------------------")

    if request.method == 'POST':

        print(">>> RECEIVED:")

        file = request.files['file']
        form = request.form

        print(file)
        print(form)

        save_file(file, form)

        response = {"status": "success"}
        response_code = 200

    else:

        response = {"error": "invalid method"}
        response_code = 201

    print(">>> SENT:")
    response = app.response_class(response=json.dumps(response), status=response_code, mimetype='application/json')
    return response


def save_file(file, form):

    form_data = form.to_dict(flat=True)

    target = os.path.join(app.root_path, UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, form_data.get("input-filename")])
    file.save(destination)


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
