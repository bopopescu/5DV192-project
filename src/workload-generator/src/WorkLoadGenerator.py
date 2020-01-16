import threading
import time
import requests
from flask import Flask, json
import os




DEBUG = True

class WorkLoadGenerator:



    def __init__(self):
        self.atomic_workers_running = self.AtomicInteger()
        self.nr_work_success = self.AtomicInteger()
        self.nr_work_fail = self.AtomicInteger()
        if not DEBUG:
            self.master_ip = "35.228.95.170"  # REAL DEAL
            self.split_port = "5000"
        else:
            self.master_ip = "localhost"
            self.split_port = "5001"



    def create_workload(self, nr_workers, post_intervall):

        thread_list = []
        for i in range(nr_workers):
            print("Starting thread one")
            thread = threading.Thread(target=self.worker_load, args=(self.atomic_workers_running, self.nr_work_success, self.nr_work_fail))
            thread_list.append(thread)
            thread.start()
            time.sleep(post_intervall)

        for thread in thread_list:
            thread.join()
        print("workers_running: " + self.atomic_workers_running.get_str())
        print("work_success: " + self.nr_work_success.get_str())
        print("work_fail: " + self.nr_work_fail.get_str())
        print("Thread has finished")



    def worker_load(self, atomic_workers_running, nr_work_success, nr_work_fail):
        atomic_workers_running.increase_value()

        request_connect = "http://" + self.master_ip + ":5000/client/connect"
        request_retrieve = "http://" + self.master_ip + ":5000/client/retrieve"


        print("Connecting to master...")
        print(request_connect)
        res = requests.get(request_connect)
        print(res.status_code)
        if res.status_code == 200:
            print("Successfully connected to master!")
            data = res.json()
        else:
            print("Error on master response")
            nr_work_fail.increase_value()
            return

        slip_ip = data["ip"]
        print("ip: " + slip_ip)
        request_workload = "http://" + slip_ip + ":" + self.split_port + "/split_workload"
        print(request_workload)
        res = requests.post(request_workload)

        if res.status_code == 200:
            print("Successfully connected split_workload!")
            data = res.json()
            print("uuid: " + data["id"])
            uuid_name = data["id"]
        else:
            print("Error on split_workload response")
            nr_work_fail.increase_value()
            return
        res = requests.post(request_retrieve, json=({'id': uuid_name}))

        if res.status_code == 200:
            print("Successfully connected retrieve!")
            data = res.json()
            print("downloadUrl: " + data["downloadUrl"])
        else:
            print("Error on retrieve response")
            nr_work_fail.increase_value()
            return

        nr_work_success.increase_value()
        atomic_workers_running.decrease_value()

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

        def get_str(self):
            self.atomic_lock.acquire()
            temp = str(self.value)
            self.atomic_lock.release()
            return temp

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

