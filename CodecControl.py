import http.client
import base64
import Config

def SendXMLDataToCodec(codec,xml_data):
    
	print("Begin sending data to codec")
	
	if ((codec["user"] != None) & (codec["password"] != None)):
		authRealm = base64.b64encode(str.encode(codec["user"]+":"+codec["password"])).decode("ascii");
		print("Username/Pass SET")
	else:
		authRealm = Config.endpointGenericAuthRealm
		print("Using Default Passwords")
	
	conn = http.client.HTTPConnection(codec["ip"])

	print("Request :")
	payload = xml_data.encode('utf-8')
	print(payload)

	headers = {
		'authorization': "Basic "+authRealm,
		'content-type': "application/x-www-form-urlencoded",
		'cache-control': "no-cache",
		'postman-token': "b5f016ed-5e19-d311-563e-c6aa7fdaa591"
		}

	try:
		conn.request("POST", "/putxml", payload, headers)
		res = conn.getresponse()
		#data = res.read()
	except:
		print("Error sending data to codec")
		return
		

	print("\r\nResponse:")
	print(res.read().decode("utf-8"))
	print("End sending data to codec\r\n")

def GetXMLDataFromCodec(codec,target):
	
	print("Begin getting data from codec")
	
	if (("user" in codec) & ("password" in codec)):
		authRealm = base64.b64encode(str.encode(codec["user"]+":"+codec["password"])).decode("ascii");
	else:
		authRealm = Config.endpointGenericAuthRealm
	
	conn = http.client.HTTPConnection(codec["ip"])

	print("Codec Target Requested :"+target)

	headers = {
		'authorization': Config.endpointGenericAuthRealm,
		'cache-control': "no-cache",
		'postman-token': "e8ea19b6-0870-01fb-dfd0-7205dfcac5cd"
		}

	try:
		conn.request("GET", "/getxml?location="+target, headers=headers)
		res = conn.getresponse()
		
	except:
		print("Error getting data from codec")
		return
		

	print("\r\nResponse:")
	data = res.read()
	print(data.decode("utf-8"))
	return data
	print("End getting data to codec\r\n")