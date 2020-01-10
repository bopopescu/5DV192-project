import subprocess

import pika
import time
import os

from merge.views import GoogleBucket

from merge.RabbitMQ import RabbitMQ

RABBITMQ_IP = "35.228.95.170"
APP_PATH = os.path.dirname(__file__) + "/../"

class Merge:

    def start_rabbitMQ(self):
        bucket_name = "umu-5dv192-project-eka"
        upload_folder = os.path.join(APP_PATH, "download_dir")
        self.merge_movie_from_uuid(bucket_name, upload_folder, "0232c6fc-32f8-11ea-a64d-54bf646b5835")

        #rabbitMQ = RabbitMQ(RABBITMQ_IP)
        #rabbitMQ.create_channel('task_queue')
        #rabbitMQ.set_callback('task_queue', self.convert_movie)
        #rabbitMQ.start_queueing()

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
