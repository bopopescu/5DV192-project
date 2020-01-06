from .RabbitMQ import RabbitMQ
from . import app_google
from app import app
import os
import uuid
from flask import request
from werkzeug.utils import secure_filename
from .views import GoogleBucket
from app_main.utils import json_response
import subprocess


@app_google.route('/split', methods=['POST', 'GET'])
def form_example():
    #Dowload the movie from the bucket.
    uploadfolder = os.path.join(app.root_path, "download_dir")
    #path_script = os.path.join(app.root_path, "receiveFromBucket.sh")
    appGooglepath = os.path.join(app.root_path, "app_google")
    credentials = os.path.join(appGooglepath, "credentials.json")
    #subprocess.check_call([path_script, credentials, uploadfolder])

    if request.method == 'POST':

        file = request.files['file']
        form = request.form

        form_data = form.to_dict(flat=True)
        form_data.get("input-filename")

        print(file)
        print(form)

        if 'file' not in request.files:
            print('Error: no file found')
            return json_response({"error": "invalid file"}, 201)

        file = request.files['file']

        if file.filename == '':
            return json_response({"error": "invalid file name"}, 201)

        file.filename = secure_filename(file.filename)
        save_file_locally(file, uploadfolder, file.filename)

        uuid_filename = uuid.uuid1()  # random id using MAC address and time component.
        # Split the movie
        path_script = os.path.join(uploadfolder, "splitter.sh")
        path_file = os.path.join(uploadfolder, file.filename)
        foldername_to_upload = subprocess.check_output([path_script, path_file, str(uuid_filename)])


        #Upload all the splitted files to google bucket
        path_script = os.path.join(app.root_path, "uploadToBucket.sh")
        path = os.path.join(app.root_path, "app_google")
        credentials = os.path.join(path, "credentials.json")
        subprocess.check_call([path_script, credentials, foldername_to_upload])

        listpath = os.path.join(app.root_path, str(uuid_filename))
        print("\nPATH: " + str(listpath))
        mylist = os.listdir(listpath)
        for a in mylist:
            if a.endswith(".txt"):
               mylist.remove(a)
        print(mylist)


        #Remove all the movies locally
        path_script = os.path.join(app.root_path, "removeMovies.sh")
        subprocess.check_call([path_script, path_file, foldername_to_upload])
        return json_response({"status": "success"}, 200)


def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


def upload_work(work_list):
    rabbit_mq = RabbitMQ('35.226.3.153')

