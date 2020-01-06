import pika
import time


class RabbitMQ(object):

    def __init__(self, host):
        self.connection = None
        self.channel = None
        self.host = host

    def create_channel(self, queue):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='35.226.3.153'))
        channel = connection.channel()
        channel.queue_declare(queue='task_queue', durable=True)  # durable=True -> queue is now marked durable

    def set_callback(self, callback_function):
        self.channel.basic_qos(
            prefetch_count=1)  # don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
        self.channel.basic_consume(queue='task_queue', on_message_callback=callback_function)

    def start_queueing(self):
        self.channel.start_consuming()

    def public_message(self, message):
        self.channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent (message durable)
                              ))
        print(" [x] Sent %r" % message)

    def close_connection(self):
        print("Connection closed")
        self.connection.close()
