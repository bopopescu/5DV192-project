
from . import app_google
from app import app
import os
from flask import request
from werkzeug.utils import secure_filename
from .views import GoogleBucket
from app_main.utils import json_response
import subprocess


@app_google.route('/split', methods=['POST', 'GET'])
def form_example():
    #Dowload the movie from the bucket.
    uploadfolder = os.path.join(app.root_path, "filmen")
    path_script = os.path.join(app.root_path, "receiveFromBucket.sh")
    appGooglepath = os.path.join(app.root_path, "app_google")
    credentials = os.path.join(appGooglepath, "credentials.json")


    #Split the movie
    subprocess.check_call([path_script, credentials, uploadfolder])

    path = os.path.join(app.root_path, "filmen")
    path_script = os.path.join(path, "splitter.sh")
    path_file = os.path.join(path, "input.mkv")

    foldername_to_upload = subprocess.check_output([path_script, path_file])


    #Upload all the splitted files to google bucket
    google_storage = GoogleBucket('umu-5dv192-project-eka')
    path_script = os.path.join(app.root_path, "uploadToBucket.sh")
    path = os.path.join(app.root_path, "app_google")
    credentials = os.path.join(path, "credentials.json")
    subprocess.check_call([path_script, credentials, foldername_to_upload])



    #Remove all the movies locally
    path_script = os.path.join(app.root_path, "removeMovies.sh")
    subprocess.check_call([path_script, path_file, foldername_to_upload])
    return json_response({"status": "success"}, 200)
