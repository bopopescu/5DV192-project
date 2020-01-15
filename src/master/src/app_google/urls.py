from .rabbit_mq import RabbitMQ
from app import app
import os


def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


def upload_rabbit_mq(host, dir_name, work_list):
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


def sub_rabbit_mq(host, queue):
    rabbit_mq = RabbitMQ(host)
    rabbit_mq.create_channel(queue)
    rabbit_mq.set_callback(queue, callback)
    rabbit_mq.start_queueing()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack


