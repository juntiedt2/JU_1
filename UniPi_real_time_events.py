#!/usr/bin/env python

# UniPi Python Control Panel
# UniPi_real_time_events.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 26.03.2018

import json
import math
import os.path
import threading
from time import *
from datetime import *
from RedisQueue import RedisQueue

owire = ["dummy",
    "28B01DC107000045",    # Sensor 1 DS18B20 Temperatur
    "282836C1070000DD",    # Sensor 2 DS18B20 Temperatur
    "2892844D07000012",    # Sensor 3 DS18B20 Temperatur
    "281893C00700005E",    # Sensor 4 DS18B20 Temperatur
    "266B64140200002D",    # Sensor 5 DS2438  Humidity
    "2616BF0A020000FC"]    # Sensor 6 DS2438  Light Intensity

def Taupunkt(t, h):
	a1 = 7.45
	b1 = 235
	dp = float(t)
	fw = float(h)
	x1=(a1*dp)/(b1+dp)
	e1=6.1*math.exp(x1*2.3025851)
	e2=e1*fw/100
	x2=e2/6.1
	x3=0.434292289*math.log(x2)
	dew=(235*x3)/(7.45-x3)*100
	dew=math.floor(dew)/100
	hum=(216.7*e2)/(273.15+dp)*100
	hum=round(hum)/100
	dew =  "%.2f" % (dew)
	hum =  "%.2f" % (hum)
	#dew = '{: >5}'.format(dew)
	#hum = '{: >5}'.format(hum)
	#print("dewpoint: "+dew+" °C (condensing)")
	#print("feu:      "+hum+" (g water per 1m³ air)")
	return dew,hum   

def unipi_emit(event, data):
    data['event'] = event
    #print(data, " ", type(data))
    with lock:
        q_out.put(data)

# Temperatur --------------------------------------------------------------
	
def action_temp_1(OBJ):
    val =  "%.2f" %(float(OBJ['value']))
    #print("action_temp1: " + val)        
    unipi_emit('change_temp1', {'data': val})
		
def action_temp_2(OBJ):
    val =  "%.2f" %(float(OBJ['value']))
    #print("action_temp2: " + val)        
    unipi_emit('change_temp2', {'data': val})
	
def action_temp_3(OBJ):
    val =  "%.2f" %(float(OBJ['value']))
    #print("action_temp3: " + val)        
    unipi_emit('change_temp3', {'data': val})	
	
def action_temp_4(OBJ):
    val =  "%.2f" %(float(OBJ['value']))
    #print("action_temp4: " + val)        
    unipi_emit('change_temp4', {'data': val})
    
def action_temp_5(OBJ):
    val =  "%.2f" %(float(OBJ['value']))
    #print("action_temp5: " + val)        
    unipi_emit('change_temp5', {'data': val})  

def action_temp_6(OBJ):
    val =  "%.2f" %(float(OBJ['value']))
    #print("action_temp6: " + val)        
    unipi_emit('change_temp6', {'data': val})         
	
# Humidity & Taupunkt & Wasser/m3 -----------------------------------------

def action_humidity(OBJ):
    #float stdHum = ((vad / vdd) - 0.16) / 0.0062
    #float trueHum = stdHum / (1.0546 - (0.00216 * temp))    
    vdd =  float(OBJ['vdd'])
    vad =  float(OBJ['vad'])
    temp = float(OBJ['temp'])
    stdhum = ((vad / vdd) - 0.16) / 0.0062
    truehum =  "%.2f" % (stdhum / (1.0546 - (0.00216 * temp)))
    t,w = Taupunkt(temp, truehum)        
    unipi_emit('change_humidity', {'data': str(truehum)})
    unipi_emit('change_taupunkt', {'data': str(t)}) 
    unipi_emit('change_wasserm3', {'data': str(w)})

# Intensity Light ---------------------------------------------------------

def action_intensity(self,OBJ):
    vis =  float(OBJ['vis'])
    #print("action_intensity: " + vis)          
    unipi_emit('change_intensity', {'data': vis})
    
# Relay -------------------------------------------------------------------

def action_relay_1(OBJ):
    val =  str(OBJ['value'])
    #print("action_relay_1: " + val)       
    unipi_emit('change_relay1', {'data': val})	

def action_relay_2(OBJ):
    #print("action_relay_2: " + val)
    val =  str(OBJ['value'])
    unipi_emit('change_relay2', {'data': val})
	
def action_relay_3(OBJ):
    val =  str(OBJ['value'])
    #print("action_relay_3: " + val)          
    unipi_emit('change_relay3', {'data': val})	
	
def action_relay_4(OBJ):
    #print("action_relay_4: " + val)
    val =  str(OBJ['value'])          
    unipi_emit('change_relay4', {'data': val})	

def action_relay_5(OBJ):
    val =  str(OBJ['value'])
    #print("action_relay_5: " + val)         
    unipi_emit('change_relay5', {'data': val})	

def action_relay_6(OBJ):
    val =  str(OBJ['value']) 
    #print("action_relay_6: " + val)
    unipi_emit('change_relay6', {'data': val})	
	
def action_relay_7(OBJ):
    val =  str(OBJ['value'])  
    #print("action_relay_7: " + val)
    unipi_emit('change_relay7', {'data': val})	
	
def action_relay_8(OBJ):
    val =  str(OBJ['value'])  
    #print("action_relay_8: " + val)
    unipi_emit('change_relay8', {'data': val})

# input -------------------------------------------------------------------

def action_input_1(OBJ):
    val =  str(OBJ['value'])  
    #print("action_input_1: " + val)
    unipi_emit('change_di1', {'data': val})	

def action_input_2(OBJ):
    val =  str(OBJ['value'])
    #print("action_input_2: " + val)          
    unipi_emit('change_di2', {'data': val})	
	
def action_input_3(OBJ):
    val =  str(OBJ['value'])
    #print("action_input_3: " + val)                  
    unipi_emit('change_di3', {'data': val})	
	
def action_input_4(OBJ):
    val =  str(OBJ['value'])    
    #print("action_input_4: " + val)
    unipi_emit('change_di4', {'data': val})	

def action_input_5(OBJ):
    val =  str(OBJ['value'])      
    #print("action_input_5: " + val)
    unipi_emit('change_di5', {'data': val})

def action_input_6(OBJ):
    val =  str(OBJ['value'])      
    #print("action_input_6: " + val)
    unipi_emit('change_di6', {'data': val})
	
def action_input_7(OBJ):
    val =  str(OBJ['value']) 
    #print("action_input_7: " + val)
    unipi_emit('change_di7', {'data': val})
	
def action_input_8(OBJ):
    val =  str(OBJ['value'])      
    #print("action_input_8: " + val)
    unipi_emit('change_di8', {'data': val})

def action_input_9(OBJ):
    val =  str(OBJ['value'])      
    #print("action_input_9: " + val)
    unipi_emit('change_di9', {'data': val})	

def action_input_10(OBJ):
    val =  str(OBJ['value'])      
    #print("action_input_10: " + val)
    unipi_emit('change_di10', {'data': val})	
	
def action_input_11(OBJ):
    val =  str(OBJ['value'])      
    #print("action_input_11: " + val)
    unipi_emit('change_di11', {'data': val})	
	
def action_input_12(OBJ):
    val =  str(OBJ['value'])  
    #print("action_input_12: " + val)
    unipi_emit('change_di12', {'data': val})	
	
# ai ---------------------------------------------------------------------

def action_ai_1(OBJ):
    val =  OBJ['value']
    #print("action_ai_1: " + val)        
    unipi_emit('change_ai1', {'data': val})	

def action_ai_2(OBJ):
    val =  OBJ['value']         
    #print("action_ai_2: " + val)
    unipi_emit('change_ai2', {'data': val})
	
# ai ---------------------------------------------------------------------

def action_ao(OBJ):
    val =  OBJ['value']         
    #print("action_ao: " + val)
    unipi_emit('change_ao', {'data': val})	

#--------------------------------------------------------------------------
# UniPi Receive/Sync-Functions
#--------------------------------------------------------------------------

def sync_relay(OBJ):
    cir = str(OBJ['circuit']) 
    if cir == "1":
        action_relay_1(OBJ)
    elif cir == "2":
        action_relay_2(OBJ)
    elif cir == "3":
        action_relay_3(OBJ)
    elif cir == "4":
        action_relay_4(OBJ)
    elif cir == "5":
        action_relay_5(OBJ)
    elif cir == "6":
        action_relay_6(OBJ)
    elif cir == "7":
        action_relay_7(OBJ)
    elif cir == "8":
        action_relay_8(OBJ)
    else:
        print("Achtung! - unbekanntes relay")             
           
def sync_ai(OBJ):
    cir = str(OBJ['circuit'])     
    if cir == "1":
        action_ai_1(OBJ)
    elif cir == "2":
        action_ai_2(OBJ)
    else:
        print("Achtung! - unbekannter analoger input")           
           
def sync_ao(OBJ):
    cir = str(OBJ['circuit'])    
    if cir == "1":
        action_ao(OBJ)
    else:
        print("Achtung! - unbekannter analoger output")  


def sync_temp(OBJ):
    cir = str(OBJ['circuit'])    
    if cir == owire[1]:
        action_temp_1(OBJ)
    elif cir == owire[2]:
        action_temp_2(OBJ)
    elif cir == owire[3]:
        action_temp_3(OBJ)
    elif cir == owire[4]:
        action_temp_4(OBJ)
    elif cir == owire[5]:
        action_temp_5(OBJ)
        action_humidity(OBJ)
    elif cir == owire[6]:
        action_temp_6(OBJ)
        action_intensity(OBJ)            
    else:
        print("Achtung! - unbekannter Temperatursensor")           

           
def sync_input(OBJ):
    cir = str(OBJ['circuit'])
    if cir == "1":
        action_input_1(OBJ)
    elif cir == "2":
        action_input_2(OBJ)
    elif cir == "3":
        action_input_3(OBJ)
    elif cir == "4":
        action_input_4(OBJ)
    elif cir == "5":
        action_input_5(OBJ)
    elif cir == "6":
        action_input_6(OBJ)
    elif cir == "7":
        action_input_7(OBJ)
    elif cir == "8":
        action_input_8(OBJ)
    elif cir == "9":
        action_input_9(OBJ)
    elif cir == "10":
        action_input_10(OBJ)
    elif cir == "11":
        action_input_11(OBJ)
    elif cir == "12":
        action_input_12(OBJ)
    else:
        print("Achtung! - unbekannter input")
    
#Reading Redis-queue----------------------------------------------------------------------------------
    
def unipi_change():
    print ("unipi_receiver started")
    while True:
        if os.path.isfile("/home/pi/eng-env/webapp/stop_server.txt"):
            print("UniPi_timed_events stopped")
            break      
        while not q_in.empty():
            #message = q_in.get().decode("utf-8")
            message = q_in.get()                
            #now = datetime.now().strftime('%H:%M:%S')				
            #print(now, " Output from Queue: ", message)
            #obj = json.dumbs(message)
            obj = json.loads(message)
            #print(obj)
            dev = str(obj['dev'])
            #print(dev)
            if dev == "ai":
                sync_ai(obj)
                continue
                #pass
            elif dev == "relay":
                sync_relay(obj)
                continue
                #pass
            elif dev == "input":
                sync_input(obj)
                continue
                #pass
            elif dev == "ao":
                sync_ao(obj)
                continue
                #pass
            elif dev == "temp":
                sync_temp(obj)
                continue
                #pass                    
            else:
                print("Achtung! - unbekanntes Device!")
        #print("Queue empty")
        #sleep(0.1)

#-----------------------------------------------------------------------------------------------------------
	
if __name__ == '__main__':
    print("UniPi_receiver started")
    lock = threading.Lock()
    q_in = RedisQueue('ws_1')
    q_out = RedisQueue('ws_2')    
    unipi_change()
    print("UniPi_real_time_events stopped")

#--------------------------------------------------------------------------  
