import subprocess
from datetime import timedelta

import pika
import time
import os
from merge.google_bucket import GoogleBucket

from merge.rabbit_mq import RabbitMQ
from google.cloud._helpers import UTC

RABBITMQ_IP = "35.228.95.170" #REAL DEAL
#RABBITMQ_IP = "35.222.244.93" #Eriks rabbitmq
APP_PATH = os.path.dirname(__file__) + "/../"
BUCKET_NAME = "umu-5dv192-project-eka"

class Merge:

    def __init__(self, host):
        self.bucket = None


    def start_rabbitMQ(self):
        self.bucket = GoogleBucket(BUCKET_NAME)
        rabbitMQ = RabbitMQ(RABBITMQ_IP)

        while (True):
            try:
                print("Trying to connect to RabbitMQ...")
                rabbitMQ.create_channel('merge_queue')
                rabbitMQ.set_callback('merge_queue', self.merge_movie)
                try:
                    print("Connected to RabbitMQ")
                    rabbitMQ.start_queueing()
                except KeyboardInterrupt:
                    rabbitMQ.close_connection()
                    break

            except pika.exceptions.ConnectionClosedByBroker:
                # Uncomment this to make the example not attempt recovery
                # from server-initiated connection closure, including
                # when the node is stopped cleanly
                #
                # break
                time.sleep(10)
                continue
                # Do not recover on channel errors
            except pika.exceptions.AMQPConnectionError:
                print("Connection was closed, retrying...")
                time.sleep(10)
                continue

    def merge_movie(self, ch, method, properties, body):

        save_folder = os.path.join(APP_PATH, "download_dir")
        uuid_name = str(body, 'utf-8')
        print("Message: " + uuid_name)
        gcloud_folder_path = "transcoded/" + uuid_name

        file_name = uuid_name + ".txt"
        if self.check_merge(gcloud_folder_path, file_name):
            save_file_path = self.merge_movie_from_uuid(save_folder, uuid_name)
            self.upload_finished_file(save_file_path, uuid_name)
            #Remove all the movies locally
            path_script = os.path.join(APP_PATH, "download_dir", "removeMovies.sh")
            movie_folder = os.path.join(APP_PATH, "download_dir", uuid_name)
            text_file = os.path.join(APP_PATH, "download_dir", uuid_name + ".txt")

            subprocess.check_call([path_script, text_file, movie_folder])
        ch.basic_ack(delivery_tag=method.delivery_tag)



    def check_merge(self, gcloud_folder_path, file_name):
        save_path = APP_PATH + "download_dir"
        self.bucket.download_blob(BUCKET_NAME, gcloud_folder_path, file_name, save_path)
        qbfile = open(save_path + "/" + file_name, "r")

        if self.file_has_expired(BUCKET_NAME, gcloud_folder_path + "/" + file_name, 60*100):
            print("Merge: File has expired")
            #remove movie????
            return False


        start = "file './"
        end = "'"
        for aline in qbfile:
            movie_name = aline[aline.find(start) + len(start):aline.rfind(end)]
            if not self.bucket.file_exist(BUCKET_NAME, gcloud_folder_path, movie_name):
                print("Merge: Missing file in bucket for merge")
                qbfile.close()
                return False
        qbfile.close()
        print("Merge: All files exist in bucket for merge")
        return True



    def file_has_expired(self, gcloud_folder_path, time_to_live_min):
        import datetime
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        g_time = self.bucket.get_blob_time_created(BUCKET_NAME, gcloud_folder_path)
        expired_time = g_time + timedelta(minutes=time_to_live_min)
        return expired_time < now

    def upload_finished_file(self, source_file_name, uuid):

        destination_blob_name = "finished/" + uuid + "/" + uuid + ".mp4"
        self.bucket.upload_blob(BUCKET_NAME, source_file_name, destination_blob_name)

    def merge_movie_from_uuid(self, save_folder, uuid_name):
        save_path = os.path.join(APP_PATH, "download_dir", uuid_name)
        self.bucket.download_files_in_folder(BUCKET_NAME, "transcoded/" + uuid_name + "/", save_path)
        text_file_path = save_path +"/" + uuid_name + ".txt"
        save_file_path = save_path + "/" + uuid_name + ".mp4"
        self.merge_files_in_folder(save_folder, text_file_path, save_file_path)
        return save_file_path

    def merge_files_in_folder(self, save_folder, merge_file_path, save_file_path):
        path_script = os.path.join(save_folder, "merge.sh")
        subprocess.check_output([path_script, merge_file_path, save_file_path])

    def save_file_locally(self, file, folder, filename):
        dirname = os.path.dirname(__file__)
        target = os.path.join(dirname, folder)
        if not os.path.isdir(target):
            os.mkdir(target)
        destination = "/".join([target, filename])
        file.save(destination)
