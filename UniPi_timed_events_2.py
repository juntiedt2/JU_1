#!/usr/bin/env python

# UniPi Python Control Panel
# UniPi_timed_events.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 26.03.2018

import threading
import time
import os.path
from datetime import *
from UniPi_interface_class import *
from RedisQueue import RedisQueue

intervall_temp = 59 # event alle 60 Sekunden
intervall_pres = 900 # event alle 15 Minuten
lock = threading.Lock()
timer_1 = None
timer_2 = None   
     
#-----------------------------------------------------------------------------------------------
    
def get_temp_data():
    global lock 
    global intervall_temp
    global timer_1
    data = {}
    data['event'] = "timed_event"
    data['t1'] = ui.get_temp(1)
    data['t2'] = ui.get_temp(2)
    data['t3'] = ui.get_temp(3)
    data['t4'] = ui.get_temp(4)
    data['t5'] = ui.get_temp(5)
    data['t6'] = ui.get_temp(6)
    #
    data['h1'] = ui.get_humidity()
    data['tp'] = ui.get_taupunkt()
    data['wm'] = ui.get_wasserm3()
    #
    data['l1'] = ui.get_intensity()
    #
    data['vi'] = ui.get_vis()
    #
    with lock: 
        q.put(data)
    #print(data)
    #    
    timer_1 = threading.Timer(intervall_temp, get_temp_data)
    timer_1.start()

def get_pressure_data():
    global lock
    global intervall_pres
    global last_pr
    global timer_2
    pr = ui.get_rel_pressure()
    prf = float(pr)
    if prf > last_pr:
        tendenz = "steigend"
    elif prf == last_pr:
        tendenz = "gleichbleibend"
    else:
        tendenz = "fallend"
    data = {}
    data['event'] = "pressure_event"
    data['pr'] = pr
    data['pt'] = tendenz
    last_pr = prf
    #
    with lock: 
        q.put(data)
    #print(data)
    #    
    timer_2 = threading.Timer(intervall_pres, get_pressure_data)
    timer_2.start()        

#-- Loop -------------------------------------------------------------------------------------
    
if __name__ == '__main__':
    ui = unipi_interface("10.0.0.52","8080")
    q = RedisQueue('ws_2')
    print("unipi_timed_events started")
    last_pr = float(ui.get_rel_pressure())
    get_temp_data()
    get_pressure_data()
    
    while True:
        if os.path.isfile("/home/pi/eng-env/webapp/stop_server.txt"):
            print("UniPi_timed_events stopped")
            break        
        time.sleep(0.5)        
    timer_1.cancel()
    timer_2.cancel()
    print("timed-events-2 stopped")
    #------------------------------------------------------------------------------------------------
