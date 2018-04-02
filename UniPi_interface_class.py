# UniPi Python Control Panel
# UniPi_interface_class.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 24.03.2018

import time
import json
import math
import threading
import http.client
import urllib.request

owire = ["dummy",
    "28B01DC107000045",    # Sensor 1 DS18B20 Temperatur
    "282836C1070000DD",    # Sensor 2 DS18B20 Temperatur
    "2892844D07000012",    # Sensor 3 DS18B20 Temperatur
    "281893C00700005E",    # Sensor 4 DS18B20 Temperatur
    "266B64140200002D",    # Sensor 5 DS2438  Humidity
    "2616BF0A020000FC",    # Sensor 6 DS2438  Light Intensity
    "28A2DC8400000366"]    # Sensor 7 DS18B20 Luftdruck
    
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
	dew =  "%2.2f" % (dew)
	hum =  "%2.2f" % (hum)
	dew = '{: >5}'.format(dew)
	hum = '{: >5}'.format(hum)
	#print("dewpoint: "+dew+" °C (condensing)")
	#print("feu:      "+hum+" (g water per 1m³ air)")
	return dew,hum   
    
    
class unipi_interface(object):

    def __init__(self, Host, Port):
        self._host = Host
        self._port = Port
        self._url = "ws://%s/ws" %(self._host)
        self._conn = None
        self._headers = { 'content-type': "application/json" }
        self._lock = threading.Lock()
        
    #----------------------------------------------------------------------------

    def get_all_devices(self,type):
        with self._lock:
            url_rest ="http://%s/rest/all" %(self._host)
            res = urllib.request.urlopen(url_rest).read()
            str = res.decode("utf-8")
        if type == "j":
            obj = json.loads(str)
            return obj
        return str

    #----------------------------------------------------------------------------
    
    def HTTP_post(self,DEVICE,CIRCUIT,PAYLOAD):
        with self._lock:          
            self._conn = http.client.HTTPConnection("%s:%s" %(self._host, self._port))
            self._conn.request("POST", "/json/%s/%s" %(DEVICE,str(CIRCUIT)), PAYLOAD, self._headers) 
            res = self._conn.getresponse()
            data = res.read()
            self._conn.close()
        return data
        
    def HTTP_get(self,DEVICE,CIRCUIT,PAYLOAD):
        with self._lock:          
            self._conn = http.client.HTTPConnection("%s:%s" %(self._host, self._port))		
            self._conn.request("GET", "/json/%s/%s" %(DEVICE,str(CIRCUIT)), PAYLOAD)
            res = self._conn.getresponse()
            obj = json.loads(res.read().decode("utf-8"))
            self._conn.close()
        obj = json.loads(json.dumps(obj['data']))
        return obj

    #----------------------------------------------------------------------------        
     
    def json_set_relay(self,CIRCUIT,VALUE,TIMEOUT):
        if TIMEOUT == 0:
            payload = '{"value":"%s"}' %(str(VALUE))
        else:
            payload = '{"value":"%s","timeout":"%s"}' %(str(VALUE),str(TIMEOUT))
        status = self.HTTP_post("relay",CIRCUIT,payload)    
            
    def set_relay(self,c,v,t):
        self.json_set_relay(c,v,t)
    
    def set_relay_all(self,v):
        for x in range (1, 9):
            time.sleep(0.01)
            self.set_relay(x,v,0)
    
    def get_relay(self,CIRCUIT):
        payload = "{}"
        obj = self.HTTP_get("relay",CIRCUIT,payload)
        return obj['value']
		
    def get_input(self,CIRCUIT):
        payload = "{}"
        obj = self.HTTP_get("input",CIRCUIT,payload)
        return obj['value']

#    def set_input(self,CIRCUIT):
#       payload = '{"debounce": 100, "mode": "Simple", "counter": 0, "counter_mode": "rising", "ds_mode": "Simple", "alias": "input_1"}'
#       status = self.HTTP_post("input",CIRCUIT,payload)		

    def set_input(self,CIRCUIT):
        payload = '{"counter_mode":"rising"}' 
        status = self.HTTP-post("input",CIRCUIT,payload) 	

    def set_ao(self,VALUE):
        payload = '{"value":%s}' %(str(VALUE))
        status = self.HTTP_post("ao",1,payload) 
        
    def get_ao(self):
        payload = "{}"
        obj = self.HTTP_get("ao",1,payload)
        return str("%.4f" %(float(obj['value'])))
		
    def get_ai(self,CIRCUIT):
        payload = "{}"
        obj = self.HTTP_get("ai",CIRCUIT,payload)
        return str("%.4f" %(float(obj['value'])))
 
    def get_temp_obj(self,NUM):
        CIRCUIT = owire[NUM]    
        payload = '{}'
        return self.HTTP_get("temp",CIRCUIT,payload)

    def get_temp(self,NUM):
        obj = self.get_temp_obj(NUM)
        if obj['typ'] == "DS2438":
            return str("%.2f" %(float(obj['temp'])))
        else:
            return str("%.2f" %(float(obj['value'])))            
       
    def get_humidity(self):
        obj = self.get_temp_obj(5)
        I1 =  float(obj['vdd'])
        I2 =  float(obj['vad'])
        I3 = float(obj['temp'])
        return str("%.2f" %(float((I2 - 0.16 * I1) / (I1 * (0.00654 - (0.00001302 * I3))))))
     
    def get_taupunkt(self):
         temp = self.get_temp(5)
         humidity = self.get_humidity()
         taupunkt, H2Om3 = Taupunkt(temp, humidity)
         #print("Taupunkt : "+taupunkt+" °C (condensing)")
         return str("%.2f" %(float(taupunkt)))
        
    def get_wasserm3(self):
         temp = self.get_temp(5)
         humidity = self.get_humidity()
         taupunkt, H2Om3 = Taupunkt(temp, humidity)
         #H2Om3 =  "%.4f" %(float(H2Om3))         
         return str("%.2f" %(float(H2Om3)))        
    
    def get_intensity(self):
        obj = self.get_temp_obj(6)
        intensity =float(obj['vis'])
        if intensity < 0:
            intensity = 100.00
        else:    
            intensity = intensity*100/0.25
        return str("%.2f" %(intensity))
        
    def get_pressure(self):
        obj = self.get_temp_obj(7)
        temp = float(str(obj['value']))
        pressure =(temp*3.2)+700
        return str("%.2f" %(pressure))
        
    def get_rel_pressure(self):
        P = float(self.get_pressure())
        Prel = P/(1-482/44330)**(5.255)
        return str("%.2f" %(Prel))
        
    def get_vis(self):
        obj = self.get_temp_obj(6)
        return str("%.3f" %(float(obj['vis'])))    
        

      
