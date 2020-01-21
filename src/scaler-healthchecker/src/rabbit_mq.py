import pika
import time


class RabbitMQ(object):

    def __init__(self, host):
        self.connection = None
        self.channel = None
        self.host = host

    def create_channel(self, queue):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=True)  # durable=True -> queue is now marked durable

    def set_callback(self, queue, callback_function):
        self.channel.basic_qos(
            prefetch_count=1)  # don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
        self.channel.basic_consume(queue= queue, on_message_callback=callback_function)

    def start_queueing(self):
        self.channel.start_consuming()

    def public_message(self, queue, message):
        self.channel.basic_publish(exchange="",
                              routing_key=queue,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent (message durable)
                              ))
        print(" [x] Sent %r" % message)

    def close_connection(self):
        print("Connection closed")
        self.connection.close()
