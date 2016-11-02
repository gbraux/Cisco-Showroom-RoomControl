#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time

class KrammerControl(object):
	def __init__(self,ip="10.1.10.9",port=5000):
		self.ip = ip
		self.port = port
		self.KrammerState()
	

	def callTCP(self, message):
	
		socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		socke.connect((self.ip,self.port))
		
		socke.settimeout(10)
		
		socke.send(message.encode('ascii'))
		
		data = socke.recv(4096)
		
		print("On a envoyé "+ message)
		
		if data :
			print("La réponse reçu est "+data.decode('ascii'))
		else :
			print("Hahaha")
			
		socke.close()
			
	
	def KrammerState(self):
		print("Getting the state of the Krammer switch at the ip address "+self.ip)
		
		self.callTCP("#VID? * \r\n")
		
		#Get the input/output in a format "i1>o1,i2>o2...i8>o8" of the current configuration
		#We can reformat this output in this function

		
	def getInput(self,output):
		message = "#VID? "+str(input)+" \r\n"
		
		self.callTCP(message)
		#Get the output corresponding to the input
	
	def setInOut(self,input,output):
		message = "#VID "+str(input)+">"+str(output)+" \r\n"
		
		self.callTCP(message)
		#Set the output to the specific input
		
		
	def callPreset(self, presetnum):
		
		#Call the preset that has the number presetnum
		message = "#PRST-RCL "+str(presetnum)+" \r\n"
		
		self.callTCP(message)
		
	def savePreset(self, presetnum):
		message = "#PRST-STO "+str(presetnum)+" \r\n"
		
		self.callTCP(message)
		#Save the current current configuration in the preset that has the number presetnum

	

if __name__ == '__main__':
	kramkram = KrammerControl()