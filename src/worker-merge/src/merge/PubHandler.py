import os
import uuid

from google.cloud import pubsub_v1
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import storage
from google.oauth2 import service_account


class PubHandler:

    def __init__(self):


        self.project_name = 'testproject-261510'
        self.topic_name = 'projects/testproject-261510/topics/pub-test'
        #self.topic_name = 'projects/testproject-261510/topics/pub-test' + str(uuid.uuid1())
        dirname = os.path.dirname(__file__)
        resource_path = os.path.join(dirname, 'credentials.json')

        self.publisher = pubsub_v1.PublisherClient.from_service_account_json(resource_path)
        #self.topic_path = self.publisher.topic_path(self.project_name, self.topic_name)
        #self.publisher.create_topic(self.topic_name)

        print("init ok")
        self.push_messages()


    def push_messages(self):
        data = "test-messages-2"
        data = data.encode("utf-8")
        future = self.publisher.publish(self.topic_name, data=data)