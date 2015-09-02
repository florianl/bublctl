import websocket
import httplib
import json
import time
import argparse

AUTHENTICATE						= 1
SETTING_GET_LIVESTREAM_URL			= 31
CAMERA_GET_VERSION					= 35
CAMERA_GET_FIRMWARE_VERSIONS		= 36
CAMERA_TAKE_PIC						= 39
CAMERA_GET_BATTERY					= 45

class SocketIOPkg(object):
	def __init__(self, ref="", dest="", data=None):
		self.ref	= ref
		self.dest	= dest
		self.data	= data

	def getRef(self):
		return self.ref

	def getData(self):
		return self.data

class ConnectPkg(SocketIOPkg):
	typ = "1"

class HeartbeatPkg(SocketIOPkg):
	typ = "2"

class EventPkg(SocketIOPkg):
	typ = "5"

class AckPkg(SocketIOPkg):
	typ = "6"

def extractToken(msg):
	data = msg.split("+")[1]
	jobj = json.loads(data)
	return jobj[0]['data']['token']

def checkCount(count, data):
	if data is count:
		return True
	else:
		return False

def parseResponse(msg):
	parts = msg.split(":", 3)
	typ = parts[0]
	ref = parts[1]
	dest = parts[2]
	if len(parts) == 4:
		data = parts[3]
	else:
		data = None
	print("typ: "+ str(typ))
	print("ref: "+ str(ref))
	print("dest: "+ str(dest))
	return {
		"1": ConnectPkg,
		"2": HeartbeatPkg,
		"5": EventPkg,
		"6": AckPkg,}[typ](ref, dest, data)

def getToken(ws, count):
	while True:
		ws.send("5:"+ str(count) +"+::{\"name\":\""+ str(AUTHENTICATE) +"\",\"args\":[\"bublctl\"]}")
		response = ws.recv()
		packet = parseResponse(response)
		if isinstance(packet, AckPkg):
				return extractToken(packet.getData())
		else:
			# do not flood the bublcam with packages
			time.sleep(1)

def handleResponse(ws, action, count):
	response = ws.recv()
	package = parseResponse(response)
	return count+1

def takeAction(ws, actions):
	count = 1

	response = ws.recv()
	token = getToken(ws, count)
	count += 1
	for action in actions:
		# do not flood the bublcam with packages
		time.sleep(1)
		ws.send("5:"+ str(count) +"+::{\"name\":\""+ str(action) +"\",\"args\":[\""+ token.replace('"', '\\"') +"\"]}")
		count = handleResponse(ws, action, count)
	ws.close()

def arguments():
	parser = argparse.ArgumentParser(description="simple tool to control your bublcam")
	parser.add_argument('--livestreamURL', action='append_const', const=SETTING_GET_LIVESTREAM_URL, dest="actions", help='get the livestream URL')
	parser.add_argument('--getVersion', action='append_const', const=CAMERA_GET_VERSION, dest="actions", help='get the version of the bublcam')
	parser.add_argument('--getFirmwareversion', action='append_const', const=CAMERA_GET_FIRMWARE_VERSIONS, dest="actions", help='get the Version of the firmware')
	parser.add_argument('--takePicture', action='append_const', const=CAMERA_TAKE_PIC, dest="actions", help='take a picture')
	parser.add_argument('--getBattery', action='append_const', const=CAMERA_GET_BATTERY, dest="actions", help='get the status of the battery')
	return parser

if __name__ == "__main__":

	parser = arguments()
	args = parser.parse_args()
	
	if args.actions is None:
		parser.print_usage()
		exit()

	connection = httplib.HTTPConnection("192.168.0.100:3000")
	connection.request("GET", "/socket.io/1/")
	response = connection.getresponse()
	key = response.read().split(":")[0]
	websocket.enableTrace(True)
	ws = websocket.create_connection("ws://192.168.0.100:3000/socket.io/1/websocket/"+key)
	try:
		takeAction(ws, args.actions)
	except KeyboardInterrupt:
		ws.close()
