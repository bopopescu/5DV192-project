import subprocess

import pika
import time
import os


from convert.rabbit_mq import RabbitMQ
from convert.google_bucket import GoogleBucket

RABBITMQ_IP = "35.228.95.170"  #Real DEAL
#RABBITMQ_IP = "35.222.244.93"  #Eriks
APP_PATH = os.path.dirname(__file__) + "/../"


class Converter:

    def start_rabbitmq(self):
        print("hej")
        rabbitMQ = RabbitMQ(RABBITMQ_IP)

        while(True):
            try:
                print("Trying to connect to RabbitMQ...")
                rabbitMQ.create_channel('convert_queue')
                rabbitMQ.set_callback('convert_queue', self.convert_movie)
                try:
                    print("Connected to RabbitMQ")
                    rabbitMQ.start_queueing()
                except KeyboardInterrupt:
                    rabbitMQ.close_connection()
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
        bucket_name = "umu-5dv192-project-eka"
        bucket = GoogleBucket(bucket_name)

        bucket.download_blob(bucket_name, "split/" + uuid_name, movie_filename, save_folder)


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
        bucket.upload_blob(bucket_name, file_path, destination_folder)


        #bucket.upload_folder(bucket_name, movie_folder, destination_folder)
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
        # #
        self.upload_rabbit_mq(RABBITMQ_IP, str(uuid_name))
        #
        ###
        ###Remove all the movies locally
        path_script = os.path.join(dirname, "../", "removeMovies.sh")
        subprocess.check_call([path_script, path_file, uuid_name])
        ###
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def upload_rabbit_mq(self, host, dir_name):
        rabbit_mq = RabbitMQ(host)
        if rabbit_mq is None:
            return 1
        rabbit_mq.create_channel("merge_queue")
        message = dir_name
        rabbit_mq.public_message("merge_queue", message)
        rabbit_mq.close_connection()
        return 0
