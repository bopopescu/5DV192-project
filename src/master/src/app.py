from flask import Flask
from flask_cors import CORS
from app_google.urls import app_google
from app_main.urls import app_main

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload'
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(app_main)
app.register_blueprint(app_google)

IS_DEBUG = True

if __name__ == '__main__':
    if IS_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        app.run(debug=False, host='0.0.0.0', port=5000)
