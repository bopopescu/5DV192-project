import subprocess
from datetime import timedelta

import pika
import time
import os
from merge.views import GoogleBucket

from merge.RabbitMQ import RabbitMQ
from google.cloud._helpers import UTC

RABBITMQ_IP = "35.228.95.170" #REAL DEAL
#RABBITMQ_IP = "35.222.244.93" #Eriks rabbitmq
APP_PATH = os.path.dirname(__file__) + "/../"


class Merge:

    def start_rabbitMQ(self):
        rabbitMQ = RabbitMQ(RABBITMQ_IP)
        rabbitMQ.create_channel('merge_queue')
        rabbitMQ.set_callback('merge_queue', self.merge_movie)
        rabbitMQ.start_queueing()


    def merge_movie(self, ch, method, properties, body):
        bucket_name = "umu-5dv192-project-eka"
        save_folder = os.path.join(APP_PATH, "download_dir")
        uuid_name = str(body, 'utf-8')
        print("Message: " + uuid_name)
        gcloud_folder_path = "merged/" + uuid_name
        file_name = uuid_name + ".txt"
        if self.check_merge(bucket_name, gcloud_folder_path, file_name):
            save_file_path = self.merge_movie_from_uuid(bucket_name, save_folder, uuid_name)
            self.upload_finished_file(bucket_name, save_file_path, uuid_name)
            #Remove all the movies locally
            path_script = os.path.join(APP_PATH, "download_dir", "removeMovies.sh")
            movie_folder = os.path.join(APP_PATH, "download_dir", uuid_name)
            text_file = os.path.join(APP_PATH, "download_dir", uuid_name + ".txt")
            subprocess.check_call([path_script, text_file, movie_folder])
        ch.basic_ack(delivery_tag=method.delivery_tag)



    def check_merge(self, bucket_name, gcloud_folder_path, file_name):
        bucket = GoogleBucket(bucket_name)
        save_path = APP_PATH + "download_dir"
        bucket.download_blob(bucket_name, gcloud_folder_path, file_name, save_path)
        qbfile = open(save_path + "/" + file_name, "r")

        if self.file_has_expired(bucket_name, gcloud_folder_path + "/" + file_name, 60*100):
            print("Merge: File has expired")
            #remove movie????
            return False


        start = "file './"
        end = "'"
        for aline in qbfile:
            movie_name = aline[aline.find(start) + len(start):aline.rfind(end)]
            if not bucket.file_exist(bucket_name, gcloud_folder_path, movie_name):
                print("Merge: Missing file in bucket for merge")
                qbfile.close()
                return False
        qbfile.close()
        print("Merge: All files exist in bucket for merge")
        return True



    def file_has_expired(self,bucket_name, gcloud_folder_path, time_to_live_min):
        import datetime
        bucket = GoogleBucket(bucket_name)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        g_time = bucket.get_blob_time_created(bucket_name, gcloud_folder_path)
        expired_time = g_time + timedelta(minutes=time_to_live_min)
        return expired_time < now

    def upload_finished_file(self, bucket_name, source_file_name, uuid):
        bucket = GoogleBucket(bucket_name)
        destination_blob_name = "finished/" + uuid + "/" + uuid + ".mp4"
        bucket.upload_blob(bucket_name, source_file_name, destination_blob_name)

    def merge_movie_from_uuid(self, bucket_name, save_folder, uuid_name):

        bucket = GoogleBucket(bucket_name)
        save_path = os.path.join(APP_PATH, "download_dir", uuid_name)
        bucket.download_files_in_folder(bucket_name, "split/" + uuid_name + "/", save_path)
        text_file_path = save_path + "/" + uuid_name + ".txt"
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

    def upload_rabbitMQ(self, host, dir_name, work_list):
        rabbit_mq = RabbitMQ(host)
        if rabbit_mq is None:
            return 1
        rabbit_mq.create_channel("task_queue")
        for temp in work_list:
            message = "/".join([dir_name, temp])
        print(message)
        rabbit_mq.public_message("task_queue", message)
        rabbit_mq.close_connection()
        return 0

    def sub_rabbitMQ(self, host, queue):
        rabbit_mq = RabbitMQ(host)
        rabbit_mq.create_channel(queue)
        rabbit_mq.set_callback(queue, self.callback)
        rabbit_mq.start_queueing()


    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack
