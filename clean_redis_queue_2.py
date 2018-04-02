#!/usr/bin/env python

# UniPi Python Control Panel
# clean_redis_queue_2.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 26.03.2018

import time
from RedisQueue import RedisQueue

if __name__ == '__main__':
    print("clean_redis_queue_2 started")
    q = RedisQueue('ws_2')    
    while not q.empty():
        message = q.get()
        print(message)
    print("redis_queue_2 cleaned")   




