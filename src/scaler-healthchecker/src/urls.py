from app import app
import os
import uuid
from flask import request
from werkzeug.utils import secure_filename
from utils import json_response
import subprocess

import subprocess

import pika
import time
import os

from rabbit_mq import RabbitMQ

RABBITMQ_IP = "35.228.95.170"

APP_PATH = os.path.dirname(__file__) + "/../"

def save_file_locally(file, folder, filename):

    target = os.path.join(app.root_path, folder)
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    file.save(destination)


def sub_rabbitMQ(host, queue):
    rabbit_mq = RabbitMQ(host)
    rabbit_mq.create_channel(queue)
    rabbit_mq.set_callback(queue, callback)
    rabbit_mq.start_queueing()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # delivery ack


class Converter:

    def start_rabbitmq(self):
        print("hej")
        rabbitMQ = RabbitMQ(RABBITMQ_IP)

        while(True):
            try:
                print("Trying to connect to RabbitMQ...")
                rabbitMQ.create_channel('convert_queue')
                try:
                    print("Connected to RabbitMQ")
                    rabbitMQ.start_queueing()
                except KeyboardInterrupt:
                    rabbitMQ.close_connection()
                    break

            except pika.exceptions.ConnectionClosedByBroker:

                print("Connection to RabbitMQ channel was closed, retrying...")
                time.sleep(10)
                continue
                # Do not recover on channel errors
            except pika.exceptions.AMQPConnectionError:
                print("Connection to RabbitMQ server was closed, retrying...")
                time.sleep(10)
                continue


    def upload_rabbit_mq(self, host, dir_name):
        rabbit_mq = RabbitMQ(host)
        if rabbit_mq is None:
            return 1
        rabbit_mq.create_channel("merge_queue")
        message = dir_name
        rabbit_mq.public_message("merge_queue", message)
        rabbit_mq.close_connection()
        return 0
