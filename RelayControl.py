#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib.request
from retrying import retry
import xml.etree.ElementTree as ET
import base64
import http.client

class RelayControl(object):
	def __init__(self, ip="192.168.11.72", port=80, username="admin", password="admin"):
		self._ip = ip
		self._port = port
		self._username = username
		self._password = password
		self._relay1State = None
		self._relay2State = None
		
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
		
		authRealm = base64.b64encode(str.encode(self._username+":"+self._password)).decode("ascii");
		conn = http.client.HTTPConnection(self._ip)
		
		headers = {
			'Authorization': "Basic "+authRealm,
			'cache-control': "no-cache"
			}

		try:
			conn.request("GET", "/status.xml", headers=headers)
			response = conn.getresponse()
			print(str(response))
			
			tree = ET.parse(response)
			root = tree.getroot()
			
			self._relay1State = bool(int(root[1].text))
			self._relay2State = bool(int(root[2].text))
			
			print(("--- Relay 1 state for "+self._ip+" : "+ str(self._relay1State)))
			print(("--- Relay 2 state for "+self._ip+" : "+ str(self._relay2State)))
			print("\r\n")
			
		except:
			print("Error setting relay state")
			return
		
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
		

		authRealm = base64.b64encode(str.encode(self._username+":"+self._password)).decode("ascii");
		conn = http.client.HTTPConnection(self._ip)

		headers = {
			'Authorization': "Basic "+authRealm,
			'cache-control': "no-cache"
			}

		try:
			conn.request("GET", "/relays.cgi?relay="+str(num_relay), headers=headers)
			print("--- Setting new relay state for "+self._ip+" OK")
			
		except:
			print("Error setting relay state")
			return

	
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




