import subprocess

import pika
import time
import os


from convert.rabbit_mq import RabbitMQ
from convert.google_bucket import GoogleBucket

RABBITMQ_IP = "35.228.95.170"  #Real DEAL
#RABBITMQ_IP = "35.222.244.93"  #Eriks
APP_PATH = os.path.dirname(__file__) + "/../"
BUCKET_NAME = "umu-5dv192-project-eka"


class Converter:

    def __init__(self):
        self.rabbitMQ_convert = None
        self.rabbitMQ_merge = None
        self.bucket = None
    def start_rabbitmq(self):
        print("hej")
        self.rabbitMQ_convert = RabbitMQ(RABBITMQ_IP)
        self.rabbitMQ_merge = RabbitMQ(RABBITMQ_IP)
        self.bucket = GoogleBucket(BUCKET_NAME)

        while(True):
            try:
                print("Trying to connect to RabbitMQ...")
                self.rabbitMQ_convert.create_channel('convert_queue')
                self.rabbitMQ_merge.create_channel('merge_queue')
                self.rabbitMQ_convert.set_callback('convert_queue', self.convert_movie)
                try:
                    print("Connected to RabbitMQ")
                    self.rabbitMQ_convert.start_queueing()
                except KeyboardInterrupt:
                    self.rabbitMQ_convert.close_connection()
                    self.rabbitMQ_merge.close_connection()
                    break

            except pika.exceptions.ConnectionClosedByBroker:

                print("Connection to RabbitMQ channel was closed, retrying...")
                time.sleep(10)
                continue
                # Do not recover on channel errors
            except pika.exceptions.AMQPConnectionError:
                print("Connection to RabbitMQ server was closed, retrying...")
                time.sleep(10)
                continue

    def convert_movie(self, ch, method, properties, body):
        # Dowload the movie from the bucket.
        # print(" [x] Received %r" % body)

        unsplitted_data = str(body, 'utf-8')

        splitted_data = unsplitted_data.split("/")

        uuid_name = splitted_data[0]
        movie_filename = splitted_data[1]
        dirname = os.path.dirname(__file__)

        save_folder = os.path.join(APP_PATH, "download_dir")


        self.bucket.download_blob(BUCKET_NAME, "split/" + uuid_name, movie_filename, save_folder)


        path_script = os.path.join(save_folder, "converter.sh")
        print("\n" + path_script + "\n")
        path_file = os.path.join(save_folder, movie_filename)
        subprocess.check_output([path_script, path_file, APP_PATH + "/" + uuid_name, movie_filename])
        ###

        ###
        # Upload the converted file to google bucket

        movie_folder = os.path.join(dirname, "../", uuid_name)
        destination_folder = "transcoded/" + uuid_name + "/" + movie_filename

        file_path = APP_PATH + uuid_name + "/" + movie_filename
        print("\n" + file_path + "\n")
        self.bucket.upload_blob(BUCKET_NAME, file_path, destination_folder)


        try:
            self.rabbitMQ_merge.public_message("merge_queue", str(uuid_name))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except:
            print("Failed uploading to rabbitMQ")

        finally:
            path_script = os.path.join(dirname, "../", "removeMovies.sh")
            subprocess.check_call([path_script, path_file, uuid_name])
