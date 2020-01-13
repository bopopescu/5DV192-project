import subprocess
from datetime import timedelta

import pika
import time
import os
from merge.views import GoogleBucket

from merge.RabbitMQ import RabbitMQ
from google.cloud._helpers import UTC

RABBITMQ_IP = "35.228.95.170"
APP_PATH = os.path.dirname(__file__) + "/../"

    #Hämta jobb från rabbitMQ
    #Går det ej att jobba lägg tillbaka i KÖ
    #Är jobbet ok merge ta sen bort jobb
    #OM jobbet är förgammal - ta bort från list (delete files?)
class Merge:

    def start_rabbitMQ(self):
        bucket_name = "umu-5dv192-project-eka"
        self.check_merge(bucket_name, "0232c6fc-32f8-11ea-a64d-54bf646b5835")
        # convert_queue -> merge_queue -> finished_queue
        #
        # upload_folder = os.path.join(APP_PATH, "download_dir")
        # self.merge_movie_from_uuid(bucket_name, upload_folder, "0232c6fc-32f8-11ea-a64d-54bf646b5835")

        # rabbitMQ = RabbitMQ(RABBITMQ_IP)
        # rabbitMQ.create_channel('task_queue')
        # rabbitMQ.set_callback('task_queue', self.convert_movie)
        # rabbitMQ.start_queueing()


    def check_merge(self, bucket_name, uuid_name):
        bucket = GoogleBucket(bucket_name)
        folder_path = "merged/" + uuid_name
        file_name = uuid_name + ".txt"
        save_path = APP_PATH + "download_dir"
        bucket.download_blob(bucket_name, folder_path, file_name, save_path)
        qbfile = open(save_path + "/" + file_name, "r")

        self.file_has_expired(bucket_name, folder_path + "/" + file_name, 60)

        start = "file './"
        end = "'"
        for aline in qbfile:
            movie_name = aline[aline.find(start) + len(start):aline.rfind(end)]
            if not bucket.file_exist(bucket_name, folder_path, movie_name):
                print("Merge: Missing file in bucket for merge")
                qbfile.close()
                return 1
        qbfile.close()
        print("Merge: All files exist in bucket for merge")
        return 0



    def file_has_expired(self,bucket_name, file_path, time_to_live_min):
        import datetime
        bucket = GoogleBucket(bucket_name)
        now = datetime.datetime.utcnow().replace(tzinfo=UTC)
        g_time = bucket.get_blob_time_created(bucket_name, file_path)
        expired_time = g_time + timedelta(minutes=time_to_live_min)
        return expired_time < now



    def merge_movie_from_uuid(self, bucket_name, upload_folder, uuid_name):

        bucket = GoogleBucket(bucket_name)
        save_path = os.path.join(APP_PATH, "download_dir", uuid_name)
        bucket.download_files_in_folder(bucket_name, "split/" + uuid_name + "/", save_path)
        text_file_path = save_path + "/" + uuid_name + ".txt"
        merge_movie_path = save_path + "/" + uuid_name + ".mp4"
        self.merge_files_in_folder(upload_folder, text_file_path, merge_movie_path)

    def merge_files_in_folder(self, upload_folder, merge_file_path, save_file_path):
        path_script = os.path.join(upload_folder, "merge.sh")
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
