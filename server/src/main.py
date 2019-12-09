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

    if request.method == 'POST':

        # if request is ok, send back 200 response with token

        print("Received: 200")
        data = request.get_json(silent=True)

        print("----------------------------------")
        print("TRANSCODE REQUEST")
        print("----------------------------------")
        print(">>> RECEIVED FILE:")
        print(request.files['file'])
        print(">>> RECEIVED FORM DATA:")

        formData = request.form.to_dict(flat=True)
        print(formData)
        print(formData.get("output-filename"))

        target = os.path.join(app.root_path, UPLOAD_FOLDER)
        if not os.path.isdir(target):
            os.mkdir(target)

        file = request.files['file']

        destination = "/".join([target, formData.get("input-filename")])
        file.save(destination)

        data = {
            "token": "123",
        }

        print(">>> SENT 200")

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    print(">>> SENT 201")

    print("other method received")
    response = app.response_class(
        response=json.dumps({"error": "invalid method"}),
        status=201,
        mimetype='application/json'
    )
    return response



@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
