#!/usr/bin/env python
import pika
import sys
##
#Marking messages as persistent doesn't fully guarantee that a message won't be lost. 
#Although it tells RabbitMQ to save the message to disk, there is still a short time window when RabbitMQ 
#has accepted a message and hasn't saved it yet. Also, RabbitMQ doesn't do fsync(2) for every message
##

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='35.222.244.93'))
channel = connection.channel()

channel.queue_declare(queue='merge_queue', durable=True) # durable=True -> never lose the queue
 
message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                      routing_key='merge_queue',
                      body='0232c6fc-32f8-11ea-a64d-54bf646b5835',
		      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent (message durable)
                      ))
print(" [x] Sent %r" % message)
connection.close()
