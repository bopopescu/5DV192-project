from .RabbitMQ import RabbitMQ
from .Converter import Converter
from . import app_google
from app import app
import os
import uuid
from flask import request
from werkzeug.utils import secure_filename
from .views import GoogleBucket
from app_main.utils import json_response
import subprocess


@app.before_first_request
def run_rabbitmq():
    Converter.start_rabbitMQ()


@app_google.route('/convert', methods=['POST', 'GET'])
def convert_movie():
    # Dowload the movie from the bucket.
    upload_folder = os.path.join(app.root_path, "download_dir")
    bucket_name = "umu-5dv192-project-eka"
    bucket = GoogleBucket(bucket_name)
    bucket.download_blob(bucket_name, "split/028cc1dc-3156-11ea-8f99-54bf646b5610",
                         "028cc1dc-3156-11ea-8f99-54bf646b5610_001.mp4", upload_folder)

    uuid_foldername = "028cc1dc-3156-11ea-8f99-54bf646b5610"
    uuid_filename = "028cc1dc-3156-11ea-8f99-54bf646b5610_001"

    movie_filename = "028cc1dc-3156-11ea-8f99-54bf646b5610_001.mp4"
    #  convert the movie
    path_script = os.path.join(upload_folder, "converter.sh")
    path_file = os.path.join(upload_folder, movie_filename)
    subprocess.check_output([path_script, path_file, uuid_foldername, uuid_filename])
    ###

    ###
    # Upload the converted file to google bucket

    movie_folder = os.path.join(app.root_path, uuid_foldername)
    destination_folder = "transcoded/" + uuid_foldername
    bucket.upload_folder(bucket_name, movie_folder, destination_folder)
    ###
    #
    #
    #
    # # listpath = os.path.join(app.root_path, uuid_filename)
    # # print("\nPATH: " + str(listpath))
    # # mylist = os.listdir(listpath)
    # # for a in mylist:
    # #     if a.endswith(".txt"):
    # #        mylist.remove(a)
    # #
    # # upload_rabbitMQ("34.68.43.153", uuid_filename, mylist)
    #
    ###
    # Remove all the movies locally
    path_script = os.path.join(app.root_path, "removeMovies.sh")
    subprocess.check_call([path_script, path_file, uuid_foldername])
    ###
    return json_response({"status": "success"}, 200)


def save_file_locally(file, folder, filename):
    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


def upload_rabbitMQ(host, dir_name, work_list):
    rabbit_mq = RabbitMQ(host)
    rabbit_mq.create_channel("convert_queue")
    for temp in work_list:
        message = "/".join([dir_name, temp])
        print(message)
        rabbit_mq.public_message("convert_queue", message)
    rabbit_mq.close_connection()


def sub_rabbitMQ(host, queue):
    rabbit_mq = RabbitMQ(host)
    rabbit_mq.create_channel(queue)
    rabbit_mq.set_callback(queue, callback)
    rabbit_mq.start_queueing()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack
