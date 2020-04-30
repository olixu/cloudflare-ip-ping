#!/usr/bin/env python
# -*- coding:utf-8 -*-

import  subprocess
import logging
import datetime
import time
import threading
from queue import Queue
import re

def set_logging_format():
    logging.basicConfig(level=logging.INFO,
        format='%(message)s',
        filename="ping_host.log",
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

# Push ip into the queue
def insert_ip_queue(hosts_list_path):
    IP_QUEUE = Queue()
    with open(hosts_list_path, "r") as f:
        for host in f.readlines():
            IP_QUEUE.put(host)
    return IP_QUEUE

# define a ping function
def ping_host(IP_QUEUE, THRESHOLD):
    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get().strip("\n")
        popen = subprocess.Popen('ping -c 1 -w 1 %s' %ip, stdout=subprocess.PIPE,shell=True)
        popen.wait()
        res = popen.stdout.read().decode('utf-8').strip('\n')
        if "1 received" in res:
            try:
                x = re.findall("time=\d+ ms", res)[0]
                x = re.findall(r"\d+", x)[0]
                if int(x)<THRESHOLD:
                    logging.info("%s  %s %s" % (ip," Latency is: ", x))
            except:
                pass

if __name__ == '__main__':
    set_logging_format()
    hosts_list_path  = "./input.txt"

    WORD_THREAD_NUM = 40
    THRESHOLD = 200
    IP_QUEUE = insert_ip_queue(hosts_list_path)
    threads = []
    for i in range(WORD_THREAD_NUM):
        thread = threading.Thread(target=ping_host,args=(IP_QUEUE,THRESHOLD))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
