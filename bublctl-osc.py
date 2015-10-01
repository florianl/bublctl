import requests
import json

class bublctlosc:
	def __init__(self, ip="192.168.0.100", port="80"):
		self.ip		= ip
		self.port	= port
		self.sid	= None
		self.header	= {"User-Agent":"bublctlosc",
						"X-XSRF-Protected":"1"}
		self.sess	= requests.session()

	def start(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.startSession"})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		self.sid = (rep["results"]["sessionId"])
		return

	def update(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.updateSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def stop(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.closeSession", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def takePicture(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.takePicture", "parameters":{"sessionId":self.sid}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return (rep["results"]["fileUri"])

	def listPictures(self, count, size, thumbs):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.listImages", "parameters":{"entryCount":count, "maxSize":size, "includeThumb":bool(thumbs)}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def deletePicture(self, fileUri):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def getPicture(self, fileUri):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		print req
		return

	def getPictureMetadata(self, fileUri):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.delete", "parameters":{"fileUri":fileUri}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def getOptions(self, optionlist=["captureMode", "iso", "shutterSpeed", "aperture",
								"whiteBalance", "exposureCompensation", "fileFormat",
								"exposureDelay", "sleepDelay", "offDelay", "totalSpace",
								"remainingSpace", "gpsInfo", "hdr", "gyro",
								"imageStabilization", "wifiPassword"]):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.getOptions", "parameters":{"sessionId":self.sid, "optionNames":optionlist}})
		self.header["Content-Type"] = "application/json; charset=utf-8"
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def info(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/info"
		req = requests.get(url, headers=self.header)
		rep = req.json()
		print rep
		return

	def state(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/state"
		req = requests.post(url, headers=self.header)
		rep = req.json()
		print rep
		return


if __name__ == "__main__":

	con = bublctlosc()
	con.state()
	con.info()
	con.start()
	con.getOptions()
	con.stop()
