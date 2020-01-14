#!/usr/bin/env python
import pika
import sys
##
#Marking messages as persistent doesn't fully guarantee that a message won't be lost. 
#Although it tells RabbitMQ to save the message to disk, there is still a short time window when RabbitMQ 
#has accepted a message and hasn't saved it yet. Also, RabbitMQ doesn't do fsync(2) for every message
##

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='35.228.95.170'))
channel = connection.channel()

channel.queue_declare(queue='test_queue', durable=True) # durable=True -> never lose the queue

count = 0
for x in range(0,1):
	
	count += 1
	message = str(count)
	channel.basic_publish(exchange='',
		              routing_key='test_queue',
		              body=message,
			      properties=pika.BasicProperties(
		                 delivery_mode = 2, # make message persistent (message durable)
		              ))
	print(" [x] Sent %r" % message)
connection.close()
