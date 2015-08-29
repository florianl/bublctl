import websocket
import httplib
import json

def takePhoto(ws):
	while True:
		response = ws.recv()
		print(len(response.split(":")))
		print(response)
		kind = response.split(":")[0]
		if kind == 1:
			print("1")
			continue
		elif kind == str("5"):
			print("5")
			jobj = json.loads(response.split(":::")[1])
			if jobj["name"] == "init":
				# try to get a token
				ws.send("5:1+::{\"name\":\"1\",\"args\":[\"bublctl\"]}")
		elif kind == str("6"):
			print("6")
		else:
			print("don't know "+str(kind))

if __name__ == "__main__":
	connection = httplib.HTTPConnection("192.168.0.100:3000")
	connection.request("GET", "/socket.io/1/")
	response = connection.getresponse()
	key = response.read().split(":")[0]
	websocket.enableTrace(True)
	ws = websocket.create_connection("ws://192.168.0.100:3000/socket.io/1/websocket/"+key)
	try:
		takePhoto(ws)
	except KeyboardInterrupt:
		ws.close()
