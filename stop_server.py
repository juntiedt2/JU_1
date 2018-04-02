#!/usr/bin/env python

# UniPi Python Control Panel
# stop_server.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 26.03.2018

from RedisQueue import RedisQueue
import threading

if __name__ == '__main__':
    print("stop_server.py started")
    lock = threading.Lock() 
    q = RedisQueue('ws_2')
    payload = "close"
    with lock:
        q.put(payload)
    print("Stop_server.py send ", payload)


