import json


# (OPEN, CLOSE, PING, PONG, MESSAGE, UPGRADE, NOOP) = (0, 1, 2, 3, 4, 5, 6)
# packet_names = ['OPEN', 'CLOSE', 'PING', 'PONG', 'MESSAGE', 'UPGRADE', 'NOOP']


class Packet:
	pkt_type = None
	data = None
	event_name = None
	callbackid = None
	pkt_type_list = [0, 1, 2, 3, 4, 5, 6]
	pkt_names = ['OPEN', 'CLOSE', 'PING', 'PONG', 'MESSAGE', 'UPGRADE', 'NOOP']

	def __init__(self, pkt_type = None, data = None, event_name = None, raw = None):
		self.data = data
		self.pkt_type = pkt_type

		self.event_name = event_name

		if raw:
			self.decode(raw)

	def decode(self, raw):
		if int(raw[0]) in self.pkt_type_list:
			self.pkt_type = int(raw[0])

		encode_data = raw[1:]

		pos = 0
		for c in raw:
			try:
				num = int(c)
				pos = pos + 1
			except ValueError as e:
				break
		
		# decode callback
		callid = raw[:pos]
		if callid.__len__() == 3:
			self.callbackid = callid[2:]

		# decode message
		message = raw[pos:]
		if message != '':

			dec_msg = json.loads(message)

			if self.callbackid:
				dec_msg[0] = json.loads(dec_msg[0])
				self.data = dec_msg

			elif isinstance(dec_msg, list):
				self.event_name = dec_msg[0]
				self.data = dec_msg[1]



		
		
		# if str(encode_data).__len__() > 1:

		# 	try:
		# 		self.data = json.loads(encode_data)
		# 	except ValueError as e:
		# 		self.callbackid = encode_data[1]
		# 		self.data = json.loads(encode_data[2:])
		# 		self.data[0] = json.loads(self.data[0])




	def encode(self, callid = None):
		if not callid:
			callid = ''

		payload = [self.event_name, self.data]
		return "{}2{}{}".format(self.pkt_type, callid, json.dumps(payload))