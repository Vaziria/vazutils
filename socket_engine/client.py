import websocket
import collections

from ..logger import Logger
from .packet import Packet

logger = Logger(__name__)






websocket.enableTrace(True)


class Client:
	socket = None
	handler = {}
	callbacks = {}

	def _open_socket(self, *args, **kwargs):
		self.socket = websocket.WebSocketApp(*args, **kwargs)
		self.socket.on_open = self._on_open
		self.socket.on_message = self._recieve_packet
		self.socket.run_forever()

	def _on_open(self):
		pass


	def _recieve_packet(self, data):
		print(data)
		packet = Packet(raw = data)

		if packet.pkt_type == 0:
			self.get_event('connect')()
		elif packet.pkt_type == 2:
			self.socket.send("2")
		elif packet.pkt_type == 3:
			self.get_event('pong')()
		elif packet.pkt_type == 4:
			if packet.callbackid:
				callback = self.callbacks.get(str(packet.callbackid))
				if callback:
					callback(packet.data[0])

			elif packet.event_name:
				self.get_event(packet.event_name)(packet.data)


	def on(self, name, eventcall):
		self.handler[name] = eventcall

	def emit(self, event, data, callback = None):
		packet = Packet(
			pkt_type = 4,
			event_name = event,
			data = data
		)

		if isinstance(callback, collections.Callable):
			callid = "0"
			self.callbacks[callid] = callback
			payload = packet.encode(callid)
		else:
			payload = packet.encode()

		logger.debug('emitting {}'.format(payload))
		self.socket.send(payload)

	def get_event(self, name):
		return self.handler.get(name, self._no_handler)

	def disconnect(self):
		self.socket.send("1")


	def _no_handler(self, *args, **kwrags):
		print('no handler')

