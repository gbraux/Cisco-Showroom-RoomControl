#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib.request
from retrying import retry
#from six.moves import urllib
import xml.etree.ElementTree as ET

class RelayControl(object):
	def __init__(self, ip="192.168.11.72", port=80, username="admin", password="admin"):
		self._ip = ip
		self._port = port
		self._username = username
		self._password = password
		self._relay1State = None
		self._relay2State = None
		
		# authinfo = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		# authinfo.add_password(None, self._ip, self._username, self._password)
		# handler = urllib.request.HTTPBasicAuthHandler(authinfo)
		# myopener = urllib.request.build_opener(handler)
		# opened = urllib.request.install_opener(myopener)
		
		self._UpdateRelaysState()
		
	@property
	def relay1(self):
		self._UpdateRelaysState()
		return self._relay1State

	@relay1.setter
	def relay1(self, relay1val):
		self._SetRelay(1,relay1val)

	@property
	def relay2(self):
		self._UpdateRelaysState()
		return self._relay2State
		
	@relay2.setter
	def relay2(self, relay2val):
		self._SetRelay(2,relay2val)

	@retry
	def _UpdateRelaysState(self):
		
		print("--- Getting current relay states for  "+self._ip)
		
		response = urllib.request.urlopen("http://"+self._ip+"/status.xml")
		
		#print(response.read())
		tree = ET.parse(response)
		root = tree.getroot()
		#print(root)
		
		self._relay1State = bool(int(root[1].text))
		self._relay2State = bool(int(root[2].text))
		
		print(("--- Relay 1 state for "+self._ip+" : "+ str(self._relay1State)))
		print(("--- Relay 2 state for "+self._ip+" : "+ str(self._relay2State)))
		print("\r\n")

	@retry
	def _SetRelay(self, num_relay, state):
	
		self._UpdateRelaysState()
		
		print(("--- Setting new relay state for "+self._ip+"  (R"+str(num_relay)+" : "+str(state)+")"))
		
		if num_relay == 1:
			if state == self._relay1State:
				return
			else:
				self._relay1State = state
				
		if num_relay == 2:
			if state == self._relay2State:
				return
			else:
				self._relay2State = state
		
		response = urllib.request.urlopen("http://"+self._ip+"/relays.cgi?relay="+str(num_relay))
		
		print("--- Setting new relay state for "+self._ip+" OK")
		
		#self._UpdateRelaysState()
	
if __name__ == '__main__':
	relayMonet = RelayControl("192.168.11.72", 80, "admin", "admin")
	relayMonet.relay1 = False
	time.sleep(0.5)
	relayMonet.relay2 = False
	time.sleep(0.5)
	relayMonet.relay1 = True
	time.sleep(0.5)
	relayMonet.relay2 = True
	#test._SetRelay(1, True)
	#print(RelayControl.relay2)
	#print(test.relay2)
	#print(test.relay2)




