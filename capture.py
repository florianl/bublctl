import websocket
import httplib
import json
import time

AUTHENTICATE						= 1
CAMERA_TAKE_PIC						= 39

def photoDone(msg):
	jobj = json.loads(msg)
	if jobj['name'][0] == str("3"):
		return True
	else:
		return False

def extractToken(msg):
	data = msg.split("+")[1]
	jobj = json.loads(data)
	return jobj[0]['data']['token']

def checkCount(count, data):
	answer = int(data.split("+")[0])
	if answer is count:
		return True
	else:
		return False

def parseResponse(msg):
	parts = msg.split(":", 3)
	typ = parts[0]
	if len(parts) == 4:
		data = parts[3]
	else:
		data = None
	return (typ, data)

def getToken(ws, count):
	while True:
		ws.send("5:"+ str(count) +"+::{\"name\":\""+ str(AUTHENTICATE) +"\",\"args\":[\"bublctl\"]}")
		response = ws.recv()
		packet = parseResponse(response)
		if packet[0] == str("6"):
			if checkCount(count, packet[1]):
				return extractToken(packet[1])
			else:
				continue
		else:
			# do not flood the bublcam with packages
			time.sleep(1)

def takePhoto(ws):
	count = 1

	response = ws.recv()
	token = getToken(ws, count)
	count += 1
	ws.send("5:"+ str(count) +"+::{\"name\":\""+ str(CAMERA_TAKE_PIC) +"\",\"args\":[\""+ token.replace('"', '\\"') +"\"]}")
	while True:
		response = ws.recv()
		packet = parseResponse(response)
		if packet[0] == str("5"):
			if photoDone(packet[1]):
				ws.close()
				return

if __name__ == "__main__":
	connection = httplib.HTTPConnection("192.168.0.100:3000")
	connection.request("GET", "/socket.io/1/")
	response = connection.getresponse()
	key = response.read().split(":")[0]
#	websocket.enableTrace(True)
	ws = websocket.create_connection("ws://192.168.0.100:3000/socket.io/1/websocket/"+key)
	try:
		takePhoto(ws)
	except KeyboardInterrupt:
		ws.close()
