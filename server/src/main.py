from flask import Flask, request, json
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/transcode/request', methods=['POST'])
def form_example():

    if request.method == 'POST':

        # if request is ok, send back 200 response with token

        print("post request received")
        request.data

        data = {
            "token": "123",
        }


        # send response

        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response


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
