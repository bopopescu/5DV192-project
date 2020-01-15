import os
from google.cloud import pubsub_v1, exceptions


class SubHandler:
    #self.project_name = 'testproject-261510'
    #self.subscriber_name = 'projects/testproject-261510/subscriptions/finished-sub'
    def __init__(self, project_name, subscriber_name):
        self.message_exist = False
        self.uuid_search = None
        self.project_name = project_name
        self.subscriber_name = subscriber_name

    def set_up(self):
        resource_path = None
        try:
            try:
                dirname = os.path.dirname(__file__)
                resource_path = os.path.join(dirname, 'credentials.json')
            except:
                print("PubSub : Unable to find credentials")
                return False

            self.subscriber = pubsub_v1.SubscriberClient.from_service_account_json(resource_path)
            # self.subscriber_path = self.subscriber.subscription_path(self.project_name, self.subscriber_name)
        except:
            print("PubSub : Unable to connect")
            return False
        return True

    def callback(self, message):
        if message.data.decode('UTF-8') == self.uuid_search:
            self.message_exist = True
            print("found: " + message.data.decode('UTF-8'))
            #raise ValueError('Lungt: Ska kasta expetion när den hittar meddelande.')
            #message.ack()
        #print("Received message: {}".format(message))
        message.nack()

    def find_message(self, uuid, timeout):
        self.uuid_search = uuid
        streaming_pull_future = None
        print("wowo")
        try:
            streaming_pull_future = self.subscriber.subscribe(self.subscriber_name, callback=self.callback)
        except:
            print("PubSub: Unable to subscribe")
        try:
            streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.cancel()
        except:  # noqa
            None
        return self.message_exist


class PubHandler:
    # self.project_name = 'testproject-261510'
    # self.topic_name = 'projects/testproject-261510/topics/finished'

    def __init__(self, project_name, topic_name):

        self.project_name = project_name
        self.topic_name = topic_name

    def set_up(self):
        resource_path = None
        try:
            try:
                dirname = os.path.dirname(__file__)
                resource_path = os.path.join(dirname, 'credentials.json')
            except:
                print("PubSub : Unable to find credentials")
                return False

            self.publisher = pubsub_v1.PublisherClient.from_service_account_json(resource_path)
        except:
            print("PubSub : Unable to connect")
            return False
        return True

    # data = "super-messages-3"
    def push_messages(self, message):
        data = message
        data = data.encode("utf-8")
        try:
            self.publisher.publish(self.topic_name, data=data)
            return True
        except:
            print("PubSub : Unable to push message")
            return False