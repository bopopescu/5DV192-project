import os

from google.cloud import pubsub_v1
from google.api_core.exceptions import DeadlineExceeded
from google.cloud import storage
from google.oauth2 import service_account


class SubHandler:

    def __init__(self):

        self.project_name = 'testproject-261510'
        self.subscriber_name = 'projects/testproject-261510/subscriptions/super-test'
        dirname = os.path.dirname(__file__)
        resource_path = os.path.join(dirname, 'credentials.json')
        self.subscriber = pubsub_v1.SubscriberClient.from_service_account_json(resource_path)
        self.subscriber_path = self.subscriber.subscription_path(self.project_name, self.subscriber_name)
        print("init ok")
        self.pull_messages()


    def callback(self, message):
        print("Received message: {}".format(message))
        #message.ack()


    def pull_messages(self):
        streaming_pull_future = self.subscriber.subscribe(
            'projects/testproject-261510/subscriptions/super-test', callback=self.callback
        )

        print("Listening for messages on {}..\n".format('projects/testproject-261510/topics/pub-test'))

        # result() in a future will block indefinitely if `timeout` is not set,
        # unless an exception is encountered first.
        try:
            streaming_pull_future.result(timeout=6)
            streaming_pull_future.cancel()
        except:  # noqa
            print("Timeout")
        print("done")







    # def pull_messages(self,number_of_messages):
    #
    #     try:
    #         response = self.subscriber.pull(self.subscriber_path, max_messages = number_of_messages)
    #         received_messages = response.received_messages
    #     except DeadlineExceeded as e:
    #         received_messages = []
    #         print('No messages caused error')
    #     return received_messages
    #
    #
    # def ack_messages(self,message_ids):
    #
    #     if len(message_ids) > 0:
    #         self.subscriber.acknowledge(self.subscriber_path, message_ids)
    #         return True