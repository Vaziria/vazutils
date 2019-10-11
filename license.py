import os
from uuid import getnode as get_mac
import requests
import hashlib
import json
from datetime import datetime

def generate_key():
	date = datetime.utcnow().strftime('%Y-%m-%d|%I')
		
	hasher = hashlib.md5()
	hasher.update(date.encode('utf8'))
	
	cek = hasher.hexdigest()


	return cek

class License(object):
	
	url = 'http://68.183.129.244:8001/v1/login'
	
	def getPayload(self, username, password, bot_id = 1):
		payload = {
			'email': username,
			'password': password,
			'name': os.environ['COMPUTERNAME'],
			'mac': str(get_mac()),
			'bot_id': bot_id,
			
		}
		
		return payload
	
	def getData(self, payload):
		req = requests.post(self.url, headers = {'Content-Type': 'aplication/json', 'Accept': 'aplication/json'}, data=json.dumps(payload))
		
		return req.text
	
	def cek(self, data):
		date = datetime.utcnow().strftime('%Y-%m-%d|%I')
		
		hasher = hashlib.md5()
		hasher.update(date.encode('utf8'))
		
		cek = hasher.hexdigest()
		
		if cek == data:
			return True
		
	
		return False
	
	
		
		
		
		
		
		
		
_license = License()	
	
		
if __name__ == '__main__':
	
	payload = license.getPayload('chat@auth.com', 'password')

	print(json.dumps(payload))

	auth = license.getData(payload)
	print(auth.encode('utf-8'))
	print(license.cek(auth))
	
	