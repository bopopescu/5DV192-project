
from . import app_google
from app import app
import os
from flask import request
from werkzeug.utils import secure_filename
from .views import GoogleBucket
from app_main.utils import json_response
import subprocess


@app_google.route('/google-bucket/upload', methods=['POST', 'GET'])
def form_example():
    #appGooglepath = os.path.join(app.root_path, "app_google")
    #credentials = os.path.join(appGooglepath, "credentials.json")


    #subprocess.check_call([path_script, credentials, foldername_to_upload])

    path = os.path.join(app.root_path, "filmen")
    path_script = os.path.join(path, "splitter.sh")
    path_file = os.path.join(path, "film.mkv")

    foldername_to_upload = subprocess.check_output([path_script, path_file])

    google_storage = GoogleBucket('umu-5dv192-project-eka')
    #print(google_storage.list_buckets_names())
    #print(foldername_to_upload)


        #
        #
        # file = request.files['file']
        # form = request.form
        #
        # form_data = form.to_dict(flat=True)
        # form_data.get("input-filename")
        #
        # print(file)
        # print(form)
        #
        # if 'file' not in request.files:
        #     print('Error: no file found')
        #     return json_response({"error": "invalid file"}, 201)
        #
        # file = request.files['file']
        #
        # if file.filename == '':
        #     return json_response({"error": "invalid file name"}, 201)
        #
        # file.filename = secure_filename(file.filename)
        #
        # url = google_storage.upload_file(
        #     file.read(),
        #     file.filename,
        #     file.content_type
        # )
        #
        # print(url)
        path_script = os.path.join(app.root_path, "uploadToBucket.sh")
        path = os.path.join(app.root_path, "app_google")
        credentials = os.path.join(path, "credentials.json")
        print(credentials)
        #print(path)
        subprocess.check_call([path_script, credentials, foldername_to_upload])


        return json_response({"status": "success"}, 200)
