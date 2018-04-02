#!/usr/bin/env python

# UniPi Python Control Panel
# UniPi_sender.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 24.03.2018

from UniPi_interface_class import *
from RedisQueue import RedisQueue

q = RedisQueue('ws_3')
ui = unipi_interface("10.0.0.52","8080")
print("UniPi_sender started")

while True:
    while not q.empty():
        msg = q.get()
        #print(msg, " ", type(msg))
        msg = eval(msg)
        #print(msg, " ", type(msg)) 
       
        if (msg['event'] == 'change_R1' and msg['data'] == 'on'): 
            ui.set_relay(1,1,0)
        elif msg['event'] == 'change_R1' and msg['data'] == 'off': 
            ui.set_relay(1,0,0)
        elif msg['event'] == 'change_R2' and msg['data'] == 'on': 
            ui.set_relay(2,1,0)
        elif msg['event'] == 'change_R2' and msg['data'] == 'off': 
            ui.set_relay(2,0,0)
        elif msg['event'] == 'change_R3' and msg['data'] == 'on': 
            ui.set_relay(3,1,0)
        elif msg['event'] == 'change_R3' and msg['data'] == 'off': 
            ui.set_relay(3,0,0)
        elif msg['event'] == 'change_R4' and msg['data'] == 'on': 
            ui.set_relay(4,1,0)
        elif msg['event'] == 'change_R4' and msg['data'] == 'off': 
            ui.set_relay(4,0,0)
        elif msg['event'] == 'change_R5' and msg['data'] == 'on': 
            ui.set_relay(5,1,0)
        elif msg['event'] == 'change_R5' and msg['data'] == 'off': 
            ui.set_relay(5,0,0) 
        elif msg['event'] == 'change_R6' and msg['data'] == 'on': 
            ui.set_relay(6,1,0)
        elif msg['event'] == 'change_R6' and msg['data'] == 'off': 
            ui.set_relay(6,0,0) 
        elif msg['event'] == 'change_R7' and msg['data'] == 'on': 
            ui.set_relay(7,1,0)
        elif msg['event'] == 'change_R7' and msg['data'] == 'off': 
            ui.set_relay(7,0,0)  
        elif msg['event'] == 'change_R8' and msg['data'] == 'on': 
            ui.set_relay(8,1,0)
        elif msg['event'] == 'change_R8' and msg['data'] == 'off': 
            ui.set_relay(8,0,0) 
        elif msg['event'] == 'change_ao':
            ui.set_ao(msg['data'])        
        else:
            print("Achtung! - unbekanntes Device!", msg)
    #print("Queue empty")
    #sleep(0.1)
    