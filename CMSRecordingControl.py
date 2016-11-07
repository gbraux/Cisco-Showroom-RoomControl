import http.client
import xml.etree.ElementTree as etree
import Config
import ssl
import CodecControl

def GetCMSCallID(endpointUri):
	
	ssl._create_default_https_context = ssl._create_unverified_context
	conn = http.client.HTTPSConnection(Config.cmsFqdn)

	headers = {
		'authorization': Config.cmsGenericAuthRealm,
		'cache-control': "no-cache",
		'postman-token': "9620f24c-7e1e-36f2-cede-e016ef0641e4"
		}

	conn.request("GET", "/api/v1/calllegs", headers=headers)

	res = conn.getresponse()
	data = res.read()

	print(data.decode("utf-8"))

	tree = etree.fromstring(data)
	print(tree)

	callID = ""
	found = False
	for child in tree:
		for child2 in child:
		
			
		
			print(child2.tag)
			print(child2.attrib)
			print(child2.text)
			
			if ((child2.tag == "remoteParty") & (child2.text == endpointUri)):
				found = True 
				
			if ((child2.tag == "call") & (found == True)):
				return child2.text

def SetCMSRecording(callID, state):

	ssl._create_default_https_context = ssl._create_unverified_context
	conn = http.client.HTTPSConnection(Config.cmsFqdn)

	if (state == True):
		payload = "recording=true"
	else:
		payload = "recording=false"

	headers = {
		'authorization': Config.cmsGenericAuthRealm,
		'content-type': "application/x-www-form-urlencoded",
		'cache-control': "no-cache",
		'postman-token': "b5f016ed-5e19-d311-563e-c6aa7fdaa591"
		}

	conn.request("PUT", "/api/v1/calls/" + callID, payload, headers)

	res = conn.getresponse()
	data = res.read()

	print(data.decode("utf-8"))
	print("Recording Bit Set")

def GetEndpointSIPUri(ip):

	codec = {"ip": ip}

	data = CodecControl.GetXMLDataFromCodec(codec,"/Status/SIP/Registration/URI")

	# conn = http.client.HTTPConnection(ip)

	# payload = ""

	# headers = {
	# 	'authorization': Config.endpointGenericAuthRealm,
	# 	'content-type': "application/x-www-form-urlencoded",
	# 	'cache-control': "no-cache",
	# 	'postman-token': "e8ea19b6-0870-01fb-dfd0-7205dfcac5cd"
	# 	}

	# conn.request("GET", "/getxml?location=%2FStatus%2FSIP%2FRegistration%2FURI", payload, headers)

	# res = conn.getresponse()
	# data = res.read()

	print(data.decode("utf-8"))
	
	tree = etree.fromstring(data)
	#print(tree)
	
	print("URI Found : "+tree[0][0][0].text)
	return tree[0][0][0].text

def SetRecordingFromEpIP(ip, recState):

	epSipURI = GetEndpointSIPUri(ip)
	print("Endpoint SIP URI : "+epSipURI)

	callID = GetCMSCallID(epSipURI)
	if callID != None:
		SetCMSRecording(callID, recState)
	else:
		print("No ongoing CMS call for this endpoint")
	
def SetRecordingFromEpXMLNotif(xml_data, recState):
	root = etree.fromstring(str(xml_data))
	codecIP = root.find('Identification').find('IPAddress').text
	SetRecordingFromEpIP(codecIP,recState)

if __name__ == '__main__':
	SetRecordingFromEpIP("10.1.110.152", False)

		
	
	
	