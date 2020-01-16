import threading
import time
import requests
from flask import Flask, json
import os


MASTER_IP = "35.228.95.170" #REAL DEAL

class WorkLoadGenerator:



    def __init__(self):
        self.atomic_workers_running = self.AtomicInteger()
        self.nr_work_success = self.AtomicInteger()
        self.nr_work_fail = self.AtomicInteger()


    def create_workload(self, nr_workers, post_intervall):

        thread_list = []
        for i in range(nr_workers):
            thread = threading.Thread(target=self.worker_load, args=(self.atomic_workers_running, self.nr_work_success, self.nr_work_fail))
            thread_list.append(thread)
            thread.start()
            time.sleep(post_intervall)

        for thread in thread_list:
            thread.join()
        print("Thread has finished")



    def worker_load(self, atomic_workers_running, nr_work_success, nr_work_fail):
        #atomic_workers_running.increase_value()

        request_connect = "http://" + MASTER_IP + ":5000/client/connect"
        request_retrieve = "http://" + MASTER_IP + ":5000/client/retrieve"


        print("Connecting to master...")
        res = requests.post(request_connect)
        if res.status_code == 200:
            print("Successfully connected to master!")
            data = res.json()
        else:
            print("Error on master response")
            return
        slip_ip = data["ip"]
        print("ip: " + slip_ip)
        request_workload = "http://" + slip_ip + ":5000/client/split_workload"
        res = requests.post(request_workload)


        print(res.status_code)
        if res.status_code == 200:
            print("Successfully connected split_workload!")
            data = res.json()
            print("uuid: " + data["id"])
            uuid_name = data["id"]
        else:
            print("Error on split_workload response")
            return
        res = requests.post(request_retrieve, data={"id": uuid_name})
        print(res.status_code)
        print(res)
        if res.status_code == 200:
            print("Successfully connected retrieve!")
            data = res.json()
            print("downloadUrl: " + data["downloadUrl"])
        else:
            print("Error on retrieve response")
            return



	'''#1

	ip = requests.get(request_url_1, null)

	#2

	id = requests.post(request_url_2, null)
	
	#3

	url = requests.post(request_url_3, id)'''

	


        #
        # print("Thread KeepConnectionThread started!")
        # request_url = "http://" + MASTER_IP + ":5000/worker/connect"
        # request_data = {"ip": get_ip()}
        # print("Connecting to master...")
        # print("Sent: " + json.dumps(request_data) + " to " + request_url)
        # res = requests.post(request_url, json=request_data)
        # res = res.status_code
        # print("Received: " + str(res))
        #
        #
        # if res == 200:
        #     print("Successfully connected!")
        #     nr_work_success.increase_value()
        # else:
        #     print("Received: ")
        #     nr_work_fail.increase_value()
        #
        # atomic_workers_running.decrease_value()





    class AtomicInteger(object):
        """
        Class representing an atomic integer.
        Creates an thread safe integer, set and get must be used to be thread safe.
        """

        def __init__(self):
            self.value = 0
            self.atomic_lock = threading.Lock()

        def increase_value(self):
            """
            Increase value by one
            :param value: Wanted value
            """
            self.atomic_lock.acquire()
            self.value += 1
            self.atomic_lock.release()

        def decrease_value(self):
            """
            Decrease value by one
            :param value: Wanted value
            """
            self.atomic_lock.acquire()
            self.value -= 1
            self.atomic_lock.release()

        def set_value(self, value):
            """
            Changes the value of atomic integer
            :param value: Wanted value
            """
            self.atomic_lock.acquire()
            self.value = value
            self.atomic_lock.release()

        def get_value(self):
            """
            Returns the atomic integer.
            :return: The atomic integer.
            """
            self.atomic_lock.acquire()
            temp = self.value
            self.atomic_lock.release()
            return temp
