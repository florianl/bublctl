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

	def stop(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.closeSession", "parameters":{"sessionId":self.sid}})
		req = requests.post(url, data=data, headers=self.header)
		rep = req.json()
		print rep
		return

	def takePicture(self):
		url = "http://" + self.ip + ":" + self.port +"/osc/commands/execute"
		data = json.dumps({"name":"camera.takePicture", "parameters":{"sessionId":self.sid}})
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
	con.takePicture()
	con.stop()
