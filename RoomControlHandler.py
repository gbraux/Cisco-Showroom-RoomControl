#!/usr/bin/env python
# -*- coding: utf-8 -*-
import http.server
import http.client
import socketserver
import base64
import re
import sqlite3
import datetime
import urllib.parse
import json
import threading
import time
import sys
import signal
import logging
import cgi
import http.server
import urllib.request
import xml.etree.ElementTree as ET

# Librairies
import Config
import CMSRecordingControl
import RelayControl
import KrammerControl
import CodecControl


relayBox1 = None
relayBox2 = None
vanGoghAutoLight = True
vangoghAutoStores = False
proxixi = True
inputValue = 0
outputValue = 1
presetValue = 4
inputNames = ["Rien","Simon","Pierre","Fabien","Sarah","AppleTV","Chrome","Spycam","TrappeMX"]
outputNames = ["","TVDroite","TVCentre","TVGauche","MX300","MX800","Inexistant","Inexistant","Spycam"]

def startThread():
	
	
	server = ThreadedHTTPServer(('0.0.0.0', 1412), MyRequestHandler)
	print('Starting server, use <Ctrl-C> to stop')
	
	thread = threading.Thread(target = server.serve_forever)
	thread.deamon = False
	thread.start()
	
	print("--- WEB Server started (1235) ---")
	return server

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""
	
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
	
	def do_POST(self):
	
		print("POST RECEIVED")
		
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()
		content_len = int(self.headers.get("Content-Length"))
		post_body = self.rfile.read(content_len).decode("utf-8")
		print(post_body)
		
		CodecEventHandler(post_body)
		
	def log_message(self, format, *args):
		sys.stdout.write("%s --> [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))


def CodecEventHandler(xmlData):

	global vanGoghAutoLight
	global vangoghAutoStores
	global outputValue	
	global inputValue
	global presetValue
	global proxixi
	global codecs

	print("---- Handling Codec Event ----")
	print("XML RECU")
	print(xmlData)


	
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ((("CallSuccessful" in xmlData) and vanGoghAutoLight == True) or ("lightButton:on"  in xmlData)):
		print("Vangogh Call Connected")
		print("Allumer la lumiere ?")
		
		relayBox1.relay1 = True
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>on</Value>"
		"<WidgetId>lightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
			
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ((("CallDisconnect" in xmlData) and vanGoghAutoLight == True) or ("lightButton:off"  in xmlData)):
		print("VanGogh Call Disconnected")
		print("Eteindre la lumiere ?")
		
		relayBox1.relay1 = False
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>off</Value>"
		"<WidgetId>lightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
			
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("autoLightButton:on"  in xmlData):
		print("VanGogh Auto Light Enabled")
		
		vanGoghAutoLight = True
		
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>on</Value>"
		"<WidgetId>autoLightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("autoLightButton:off"  in xmlData):
		print("VanGogh Auto Light Disabled")
		
		vanGoghAutoLight = False
		
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>off</Value>"
		"<WidgetId>autoLightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))

	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("storeAutoButton:on"  in xmlData):
		print("VanGogh Auto Store Enabled")
		
		vangoghAutoStores = True
		
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>on</Value>"
		"<WidgetId>storeAutoButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("storeAutoButton:off"  in xmlData):
		print("VanGogh Auto Store Disabled")
		
		vangoghAutoStores = False
		
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>off</Value>"
		"<WidgetId>storeAutoButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))

	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("storeUpDown:increment"  in xmlData) and ("Pressed"  in xmlData):
		print("VG Baisse Store single ON")
		relayBox2.relay1 = True
		
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("storeUpDown:increment"  in xmlData) and ("Released"  in xmlData):
		print("VG Baisse Store single OFF")
		
		relayBox2.relay1 = False

	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("storeUpDown:decrement"  in xmlData) and ("Pressed"  in xmlData):
		print("VG Monte Store single ON")
		
		relayBox2.relay2 = True
			
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and ("storeUpDown:decrement"  in xmlData)  and ("Released"  in xmlData):
		print("VG Monte Store single OFF")
		
		relayBox2.relay2 = False

	if (Config.codecs["vangogh"]["mac"] in xmlData)  and (("storeFullUp"  in xmlData) and ("Pressed"  in xmlData) or (("CallDisconnect" in xmlData) and vangoghAutoStores == True)) :
		print("VG Monte Store Full ON")
		
		relayBox2.relay1 = True
		time.sleep(23)
		relayBox2.relay1 = False
		print("VG Monte Store Full Ended")
		
	if (Config.codecs["vangogh"]["mac"] in xmlData)  and (("storeFullDown"  in xmlData) and ("Pressed"  in xmlData)  or (("CallSuccessful" in xmlData) and vangoghAutoStores == True)) :
		print("VG Monte Store Full OFF")
		
		relayBox2.relay2 = True
		time.sleep(23)
		relayBox2.relay2 = False
		print("VG Baisse Store Full Ended")

	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and ("LoadValue" in xmlData):
		
		if ("LoadValue:1" in xmlData):
			krammer.callPreset(1)
		if("LoadValue:2" in xmlData):
			krammer.callPreset(2)
		if("LoadValue:3" in xmlData):
			krammer.callPreset(3)
		if("LoadValue:4" in xmlData):
			krammer.callPreset(4)
	
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and ("SaveValue" in xmlData):
		
		if ("SaveValue:1" in xmlData):
			presetValue = 1
		if("SaveValue:2" in xmlData):
			presetValue = 2
		if("SaveValue:3" in xmlData):
			presetValue = 3
		if("SaveValue:4" in xmlData):
			presetValue = 4
			
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and ("SavePreset" in xmlData):
		krammer.savePreset(presetValue)
	
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and (("InputChange:increment" in xmlData) or ("InputChange:decrement" in xmlData)) and ("Released" in xmlData) :
		
		if inputValue>0 and ("decrement" in xmlData) :
			inputValue -= 1
			
		if inputValue<8 and ("increment" in xmlData) :
			inputValue += 1
		
		name = inputNames[inputValue]
		
		CodecControl.SendXMLDataToCodec(Config.codecs["kandinsky"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>"+name+"</Value>"
		"<WidgetId>InputName</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
		CodecControl.SendXMLDataToCodec(Config.codecs["kandinskySpycam"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>"+name+"</Value>"
		"<WidgetId>InputName</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and (("OutputChange:increment" in xmlData) or ("OutputChange:decrement" in xmlData)) and ("Released" in xmlData) :
		
		if outputValue>1 and ("decrement" in xmlData) :
			outputValue -= 1
			
		if outputValue<8 and ("increment" in xmlData) :
			outputValue += 1
		
		name = outputNames[outputValue]
		
		
		CodecControl.SendXMLDataToCodec(Config.codecs["kandinsky"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>"+name+"</Value>"
		"<WidgetId>OutputName</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
		CodecControl.SendXMLDataToCodec(Config.codecs["kandinskySpycam"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>"+name+"</Value>"
		"<WidgetId>OutputName</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
			
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and ("Validation" in xmlData) :
		krammer.setInOut(inputValue,outputValue)	
		
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and ("Proxixi:off" in xmlData) :
		
		proxixi = False
		CodecControl.SendXMLDataToCodec(Config.codecs["kandinsky"],
		("<Configuration>"
		"<Proximity>"
		"<Mode>Off</Mode>"
		"</Proximity>"
		"</Configuration>"))
		
	if ((Config.codecs["kandinsky"]["mac"] in xmlData) or (Config.codecs["kandinskySpycam"]["mac"] in xmlData)) and ("Proxixi:on" in xmlData) :
		
		proxixi = True
		CodecControl.SendXMLDataToCodec(Config.codecs["kandinsky"],
		("<Configuration>"
		"<Proximity>"
		"<Mode>On</Mode>"
		"</Proximity>"
		"</Configuration>"))


	if (Config.codecs["kandinsky"]["mac"] in xmlData)  and (("startRecording_Button"  in xmlData) and ("<Pressed item=\"1\">"  in xmlData)):
		print("Recording Start Button Clicked")
		CMSRecordingControl.SetRecordingFromEpXMLNotif(xmlData,True)
		
		
	if (Config.codecs["kandinsky"]["mac"] in xmlData)  and (("endRecording_Button"  in xmlData) and ("<Pressed item=\"1\">"  in xmlData)):
		print("Recording Stop Button Clicked")
		CMSRecordingControl.SetRecordingFromEpXMLNotif(xmlData,False)
	

	
def SendCodecsFeedbackReg():
	feedbackRegMonet = ("<Command>"
		"<HttpFeedback>"
		"<Register command=\"True\">"
		"<FeedbackSlot>4</FeedbackSlot>"
		"<ServerUrl>http://10.1.20.21:1412</ServerUrl>"
		"<Expression item=\"1\">/Event/CallSuccessful</Expression>"
		"<Expression item=\"2\">/Event/CallDisconnect</Expression>"
		"<Expression item=\"3\">/Event/UserInterface/Extensions/Event</Expression>"
		"</Register>"
		"</HttpFeedback>"
		"</Command>")
		
	feedbackRegVangogh = ("<Command>"
		"<HttpFeedback>"
		"<Register command=\"True\">"
		"<FeedbackSlot>4</FeedbackSlot>"
		"<ServerUrl>http://10.1.20.21:1412</ServerUrl>"
		"<Expression item=\"1\">/Event/CallSuccessful</Expression>"
		"<Expression item=\"2\">/Event/CallDisconnect</Expression>"
		"<Expression item=\"3\">/Event/UserInterface/Extensions/Event</Expression>"
		"</Register>"
		"</HttpFeedback>"
		"</Command>")
		
	feedbackRegKandi = ("<Command>"
		"<HttpFeedback>"
		"<Register command=\"True\">"
		"<FeedbackSlot>4</FeedbackSlot>"
		"<ServerUrl>http://10.1.20.21:1412</ServerUrl>"
		"<Expression item=\"1\">/Event/CallSuccessful</Expression>"
		"<Expression item=\"2\">/Event/CallDisconnect</Expression>"
		"<Expression item=\"3\">/Event/UserInterface/Extensions/Event</Expression>"
		"</Register>"
		"</HttpFeedback>"
		"</Command>")
		
	feedbackRegSpycam = ("<Command>"
		"<HttpFeedback>"
		"<Register command=\"True\">"
		"<FeedbackSlot>4</FeedbackSlot>"
		"<ServerUrl>http://10.1.20.21:1412</ServerUrl>"
		"<Expression item=\"1\">/Event/CallSuccessful</Expression>"
		"<Expression item=\"2\">/Event/CallDisconnect</Expression>"
		"<Expression item=\"3\">/Event/UserInterface/Extensions/Event</Expression>"
		"</Register>"
		"</HttpFeedback>"
		"</Command>")
		
	print("Starting Codec HTTPFeedback Registration \r\n")
	#CodecControl.SendXMLDataToCodec(Config.codecs["monet"], feedbackRegMonet)
	CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"], feedbackRegVangogh)
	CodecControl.SendXMLDataToCodec(Config.codecs["kandinsky"], feedbackRegKandi)
	CodecControl.SendXMLDataToCodec(Config.codecs["kandinskySpycam"], feedbackRegSpycam)
	print("Feedback Codec HTTPFeedback Completed")
	
def UpdateExternalStates():

	# Etats Lumiere vanGogh
	
	if relayBox1.relay1 == True:
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>on</Value>"
		"<WidgetId>lightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
	else:
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>off</Value>"
		"<WidgetId>lightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
	
	#Etat Mode lumiere auto vanGogh
	
	if vanGoghAutoLight == True:
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>on</Value>"
		"<WidgetId>autoLightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
	else:
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>off</Value>"
		"<WidgetId>autoLightButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
	
	# Etat Mode Auto Stores VanGogh
	
	if vangoghAutoStores == True:
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>on</Value>"
		"<WidgetId>storeAutoButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
	else:
		CodecControl.SendXMLDataToCodec(Config.codecs["vangogh"],
		("<Command>"
		"<UserInterface>"
		"<Extensions>"
		"<Widget>"
		"<SetValue command=\"True\">"
		"<Value>off</Value>"
		"<WidgetId>storeAutoButton</WidgetId>"
		"</SetValue>"
		"</Widget>"
		"</Extensions>"
		"</UserInterface>"
		"</Command>"))
		
def signal_term_handler(signal, frame):
	print('got SIGTERM')
	sys.exit(0)
		
try:
	if __name__ == "__main__":
		
		relayBox1 = RelayControl.RelayControl("10.1.100.99", 80, "admin", "admin") #Relais Vangogh Lumieres
		relayBox2 = RelayControl.RelayControl("10.1.100.98", 80, "admin", "admin") #Relais Vangogh Stores
		krammer = KrammerControl.KrammerControl()
			
		signal.signal(signal.SIGTERM, signal_term_handler)
		server = startThread()
		
		ct = time.time()
		while True:
		
			# On update les état des dalles
			UpdateExternalStates()
			
			# On gere regulierement l'enregsitrement du feedback HTTP
			SendCodecsFeedbackReg()
	
			time.sleep(60)

except (KeyboardInterrupt, SystemExit):
	server.shutdown()
	print("--- WEB Server stopped ---")

	sys.exit(0)