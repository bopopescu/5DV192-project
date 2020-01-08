
class Converter(object):

    def start_rabbitMQ(self):

        print("hej")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='35.232.13.40'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)  # durable=True -> queue is now marked durable

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            time.sleep(body.count(b'.'))
            print(" [x] Done")
            ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack

        channel.basic_qos(
            prefetch_count=1)  # don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
        channel.basic_consume(
            queue='task_queue', on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

