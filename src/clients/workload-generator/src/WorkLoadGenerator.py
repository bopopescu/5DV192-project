import threading
import time
import requests
from flask import Flask, json
import os
import datetime
from datetime import timedelta
from google.cloud._helpers import UTC


DEBUG = False

class WorkLoadGenerator:



    def __init__(self):
        self.atomic_workers_running = self.AtomicInteger()
        self.nr_work_success = self.AtomicInteger()
        self.nr_work_fail = self.AtomicInteger()
        self.run_time = []
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

        avg_time = 0
        for temp in self.run_time:
            avg_time += temp
        print("Avg time: %.2f" % (avg_time / self.nr_work_success.get_value()))

        print("Thread has finished")



    def worker_load(self, atomic_workers_running, nr_work_success, nr_work_fail):
        atomic_workers_running.increase_value()

        request_connect = "http://" + self.master_ip + ":5000/client/connect"
        request_retrieve = "http://" + self.master_ip + ":5000/client/retrieve"

        start_time = time.time()
        expired_time_small = start_time + 5*60
        expired_time_big = start_time + 10*60

        while True:
            slip_ip = None
            uuid_name = None
            print("Stage 1")
            while True:
                try:
                    res = requests.get(request_connect)
                    if res.status_code == 200:
                        data = res.json()
                        slip_ip = data["ip"]
                        print("Success: Got split ip from master: " + slip_ip)
                        break
                    else:
                        print("Error: Retrying getting split ip")
                except:
                    print("Error: Retrying ip from master")
                if time.time() > expired_time_small:
                    break
                time.sleep(1)

            request_workload = "http://" + slip_ip + ":" + self.split_port + "/split_workload"

            print("Stage 2")
            try:
                res = requests.post(request_workload)
                if res.status_code == 200:
                    data = res.json()
                    uuid_name = data["id"]
                    print("Success: movie uploaded on split worker, uuid:" + uuid_name)
                else:
                    print("Error: Uploading movie to split worker ip: " + slip_ip)
            except:
                print("Error: Uploading movie to split worker ip: " + slip_ip)

            print("Stage 3")
            try:
                res = requests.post(request_retrieve, json=({'id': uuid_name}))
                if res.status_code == 200:
                    data = res.json()
                    print("Success: retrieved downloadUrl: " + data["downloadUrl"])
                    break
                else:
                    print("Error: on retrieved downloadUrl with uuid: " + uuid_name)
            except:
                print("Error: on retrieved downloadUrl with uuid: " + uuid_name)

            if time.time() > expired_time_small:
                nr_work_fail.increase_value()
                atomic_workers_running.decrease_value()
                break
            time.sleep(1)


            if time.time() > expired_time_big:
                nr_work_fail.increase_value()
                atomic_workers_running.decrease_value()
                return

        self.run_time.append(time.time() - start_time)
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

