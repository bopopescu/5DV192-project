import pika


class RabbitMQ(object):

    def __init__(self, host):
        self.connection = None
        self.channel = None
        self.host = host
        self.res = None

    def create_channel(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def get_queue_length(self, queue):
        self.res = self.channel.queue_declare(queue=queue, durable=True, auto_delete=False, passive=True)
        return self.res.method.message_count

    def close_connection(self):
        self.connection.close()




