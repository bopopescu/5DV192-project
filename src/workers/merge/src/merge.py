from .utils import RabbitMQ
from utils import GoogleBucket

def upload_rabbitMQ(host, dir_name, work_list):
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


def sub_rabbitMQ(host, queue):
    rabbit_mq = RabbitMQ(host)
    rabbit_mq.create_channel(queue)
    rabbit_mq.set_callback(queue, callback)
    rabbit_mq.start_queueing()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack

def merge():
    bucket_name = "umu-5dv192-project-eka"
    bucket = GoogleBucket(bucket_name)


if __name__ == '__main__':
    sub_rabbitMQ("ip", "merge_queue")
