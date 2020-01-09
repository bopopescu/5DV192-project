import pika
import time
import os

from convert.RabbitMQ import RabbitMQ
from convert.views import GoogleBucket



class Converter:

    def start_rabbitMQ(self):
        print("hej")

        rabbitMQ = RabbitMQ('34.69.27.205')
        rabbitMQ.create_channel('task_queue')
        rabbitMQ.set_callback('task_queue', self.convert_movie)
        rabbitMQ.start_queueing()

        #
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='34.69.27.205'))
        # channel = connection.channel()
        #
        # channel.queue_declare(queue='task_queue', durable=True)  # durable=True -> queue is now marked durable
        #
        # channel.basic_qos(
        #     prefetch_count=1)  # don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
        # channel.basic_consume(
        #     queue='task_queue', on_message_callback=convert_movie)
        #
        # print(' [*] Waiting for messages. To exit press CTRL+C')
        # channel.start_consuming()

        # def callback(ch, method, properties, body):
        #     print(" [x] Received %r" % body)
        #     time.sleep(body.count(b'.'))
        #     print(" [x] Done")
        #     ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack

    def convert_movie(self, ch, method, properties, body):
        # Dowload the movie from the bucket.
        print(" [x] Received %r" % body)

        unsplitted_data = str(body)
        splitted_data = unsplitted_data.split("/")
        ##print(data[0])
        # print(data[1])

        dirname = os.path.dirname(__file__)

        upload_folder = os.path.join(dirname, "../", "download_dir")
        bucket_name = "umu-5dv192-project-eka"
        bucket = GoogleBucket(bucket_name)
        bucket.download_blob(bucket_name, "split/028cc1dc-3156-11ea-8f99-54bf646b5610",
                                   "028cc1dc-3156-11ea-8f99-54bf646b5610_001.mp4", upload_folder)
        #bucket.download_blob(bucket_name, "split/" + splitted_data[0],
        #splitted_data[1], upload_folder)

        uuid_foldername = splitted_data[0]
        # uuid_filename = "028cc1dc-3156-11ea-8f99-54bf646b5610_001"

        movie_filename = splitted_data[1]
        #  convert the movie
        # path_script = os.path.join(upload_folder, "converter.sh")
        # path_file = os.path.join(upload_folder, movie_filename)
        # subprocess.check_output([path_script, path_file, uuid_foldername, movie_filename])
        # ###
        #
        # ###
        # # Upload the converted file to google bucket
        #
        # movie_folder = os.path.join("Converter/", uuid_foldername)
        # destination_folder = "transcoded/" + uuid_foldername
        # bucket.upload_folder(bucket_name, movie_folder, destination_folder)
        # ###
        # #
        # #
        # #
        # # # listpath = os.path.join(app.root_path, uuid_filename)
        # # # print("\nPATH: " + str(listpath))
        # # # mylist = os.listdir(listpath)
        # # # for a in mylist:
        # # #     if a.endswith(".txt"):
        # # #        mylist.remove(a)
        # # #
        # # # upload_rabbitMQ("34.68.43.153", uuid_filename, mylist)
        # #
        # ###
        # # Remove all the movies locally
        # path_script = os.path.join("Converter/", "removeMovies.sh")
        # subprocess.check_call([path_script, path_file, uuid_foldername])
        # ###
        ch.basic_ack(delivery_tag=method.delivery_tag)

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
