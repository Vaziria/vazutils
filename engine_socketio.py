import websocket


class EngineSocket:
	socket = None

	def connect(self, *args, **kwargs):
		self.socket = websocket.WebSocketApp(*args, **kwargs)
		self.socket.run_forever()