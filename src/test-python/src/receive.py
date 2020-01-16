#!/usr/bin/env python
import pika
import time
# For durablilty to work inside docker, the docker needs to be using a volume.


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='35.228.95.170'))
channel = connection.channel()

channel.queue_declare(queue='test_queue', durable=True)  # durable=True -> queue is now marked durable


def callback(ch, method, properties, body):
    streng = str(1)
    if streng == str(body.decode('UTF-8')):
        print("\nfound you\n")
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag) #delivery ack
    #ch.basic_reject(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1) # don't dispatch a new message to a worker until it has processed and acknowledged the previous one.
channel.basic_consume(
    queue='test_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()