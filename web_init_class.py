# UniPi Python Control Panel
# web_init_class.py
# uses Python 3.5 up
# Author: Johannes Untiedt
# Version 10.0 vom 24.03.2018

from UniPi_interface_class import *

class web_init(object):

    def __init__(self,host,port):
        self._ui = unipi_interface(host,port)
    
    def get_init_data(self):
        data = {}
        data['event'] = "init"
        data['t1'] = self._ui.get_temp(1)
        data['t2'] = self._ui.get_temp(2)
        data['t3'] = self._ui.get_temp(3)
        data['t4'] = self._ui.get_temp(4)
        data['t5'] = self._ui.get_temp(5)
        data['t6'] = self._ui.get_temp(6)
        #
        data['h1'] = self._ui.get_humidity()
        data['tp'] = self._ui.get_taupunkt()
        data['wm'] = self._ui.get_wasserm3()
        #
        data['l1'] = self._ui.get_intensity()
        data['vi'] = self._ui.get_vis()
        #    
        data['r1'] = self._ui.get_relay(1)
        data['r2'] = self._ui.get_relay(2)
        data['r3'] = self._ui.get_relay(3)
        data['r4'] = self._ui.get_relay(4)
        data['r5'] = self._ui.get_relay(5)
        data['r6'] = self._ui.get_relay(6)
        data['r7'] = self._ui.get_relay(7)
        data['r8'] = self._ui.get_relay(8)    
        #
        data['di1'] = self._ui.get_input(1)
        data['di2'] = self._ui.get_input(2)
        data['di3'] = self._ui.get_input(3)
        data['di4'] = self._ui.get_input(4)
        data['di5'] = self._ui.get_input(5)
        data['di6'] = self._ui.get_input(6)
        data['di7'] = self._ui.get_input(7)
        data['di8'] = self._ui.get_input(8)
        data['di9'] = self._ui.get_input(9)
        data['di10'] = self._ui.get_input(10)
        data['di11'] = self._ui.get_input(11)
        data['di12'] = self._ui.get_input(12)
        #
        data['ai1'] = self._ui.get_ai(1)
        data['ai2'] = self._ui.get_ai(2)
        #
        data['ao'] = self._ui.get_ao()
        #
        data['p0'] = self._ui.get_pressure()
        data['pr'] = self._ui.get_rel_pressure()
        
        return data
                                  
#----------------------------------------------------------------------