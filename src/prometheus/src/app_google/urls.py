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

RABBITMQ_IP = "35.228.95.170"


@app_google.route('/split', methods=['POST', 'GET'])
def form_example():
    #Dowload the movie from the bucket.
    upload_folder = os.path.join(app.root_path, "download_dir")


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
        save_file_locally(file, upload_folder, file.filename)

        uuid_filename = str(uuid.uuid1())  # random id using MAC address and time component.
        ##
        #  Split the movie
        path_script = os.path.join(upload_folder, "splitter.sh")
        path_file = os.path.join(upload_folder, file.filename)
        subprocess.check_output([path_script, path_file, upload_folder, uuid_filename])

        ###
        # Upload all the splitted files to google bucket
        bucket_name = "umu-5dv192-project-eka"
        bucket = GoogleBucket(bucket_name)
        movie_folder = upload_folder + "/" + uuid_filename




        #Upload all the splitted file to split bucket
        destination_folder = "split/" + uuid_filename
        bucket.upload_folder(bucket_name, movie_folder, destination_folder)
        ###
        # Upload the textfile to the merge bucket
        path_to_textfile = movie_folder + "/" + uuid_filename + ".txt"
        destination_folder_textfile = "transcoded/" + uuid_filename + "/" + uuid_filename + ".txt"

        bucket.upload_blob(bucket_name, path_to_textfile,destination_folder_textfile)

        mylist = os.listdir(movie_folder)
        for a in mylist:
            if a.endswith(".txt"):
               mylist.remove(a)
        answer = upload_rabbitMQ(RABBITMQ_IP, uuid_filename, mylist)
        if answer == 1:
            print("Failed: to upload split to rabbit queue")
        else:
            print("Success: Uploaded split to rabbit queue")

        ###
        # Remove all the movies locally
        path_script = os.path.join(app.root_path, "removeMovies.sh")
        subprocess.check_call([path_script, path_file, movie_folder])

        ###
        return json_response({"status": "success"}, 200)




def merge_files_in_folder(upload_folder, merge_file_path, save_file_path):
    path_script = os.path.join(upload_folder, "merge.sh")
    subprocess.check_output([path_script, merge_file_path, save_file_path])





def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


def upload_rabbitMQ(host, dir_name, work_list):
    rabbit_mq = RabbitMQ(host)
    if rabbit_mq is None:
        return 1
    rabbit_mq.create_channel("convert_queue")
    for temp in work_list:
        message = "/".join([dir_name, temp])
        print(message)
        rabbit_mq.public_message("convert_queue", message)
    rabbit_mq.close_connection()
    return 0

def sub_rabbitMQ(host, queue):
    rabbit_mq = RabbitMQ(host)
    rabbit_mq.create_channel(queue)
    rabbit_mq.set_callback(queue, callback)
    rabbit_mq.start_queueing()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack


