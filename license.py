import os
from uuid import getnode as get_mac
import requests
import hashlib
import json
from datetime import datetime

from .logger import Logger

logger = Logger(__name__)

_host_endpoint = 'https://pdcoke.com'

auth_mode = os.environ.get('godauth', False)
if auth_mode == 'local':
	_host_endpoint = 'http://localhost:8000'
elif auth_mode:
	_host_endpoint = auth_mode

_url = '{}/v1/login'.format(_host_endpoint)
_url_v2 = '{}/v2/login'.format(_host_endpoint)

def generate_key():
	date = datetime.utcnow().strftime('%Y-%m-%d|%I')
		
	hasher = hashlib.md5()
	hasher.update(date.encode('utf8'))
	
	cek = hasher.hexdigest()


	return cek

_flow_config = [
	'bot_config',
	'member_config',
]


class License(object):
	
	# url = 'http://pdcoke.com/v1/login'
	bot_id = None
	url = _url
	# url_v2 = 'http://pdcoke.com/v2/login'
	url_v2 = _url_v2
	version = "unofficial"
	latest_version = None
	config_data = {}
	headers = {'Content-Type': 'aplication/json', 'Accept': 'aplication/json'}

	session = requests.Session()


	def v2_login(self, username, password, bot_id = 1, version = 'unofficial'):
		self.version = version
		if bot_id:
			self.bot_id = bot_id

		payload = {
			'email': username,
			'password': password,
			'name': os.environ['COMPUTERNAME'],
			'mac': str(get_mac()),
			'bot_id': bot_id,
			'version': version
		}

		req = self.session.post(self.url_v2, headers = {'Content-Type': 'aplication/json', 'Accept': 'aplication/json'}, data=json.dumps(payload))

		if auth_mode == 'local':
			logger.info(req.text)

		if req.status_code == 200:

			hasil = json.loads(req.text)

			self.latest_version = hasil.get('latest_version')

			if hasil.get('checksum', False):
				if self.cek(hasil.get('checksum')):
					self.config_data.update(hasil)
					return hasil

		return False

	def get_config(self):
		hasil = {}

		for key in _flow_config:
			config = self.config_data.get(key, False)
			if config:
				try:
					config = json.loads(config)

					# cek sentry
					self.strict_sentry_latest_version(config)

					hasil.update(config)
				except json.decoder.JSONDecodeError as e:
					logger.error('SERVER CONFIG ERROR')


		return hasil


	def strict_sentry_latest_version(self, config):
		cek = config.get('sentry_strict', False)

		print(config.get('latest_version'))

		if cek and (self.version != self.latest_version):
			if 'sentry_dsn' in config:
				del config['sentry_dsn']

			if 'sentry' in config:
				del config['sentry']

	
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

	def me(self):

		url = 'http://{}/v2/member/me'.format(_host_endpoint)

		req = self.session.get(url, headers = {'Content-Type': 'aplication/json', 'Accept': 'aplication/json'})

		if req.status_code == 200:
			hasil = json.loads(req.text)

			return hasil

		return False

	def get_notif(self):
		url = 'http://{}/v1/notification?bot={}'.format(_host_endpoint, self.bot_id)

		req = self.session.get(url)

		if req.status_code == 200:
			hasil = json.loads(req.text)
			hasil = hasil.get('data')
			return hasil
		else:
			logger.error(req.text)

		return []

	def read_notif(self):
		url = 'http://{}/v2/notification/readall'.format(_host_endpoint)

		req = self.session.get(url, headers = self.headers)

		if req.status_code == 200:
			hasil = json.loads(req.text)
			return True
		else:
			logger.error(req.status_code)
			return False
	 
	
		
		
		
		
		
		
		
_license = License()	
	
		
if __name__ == '__main__':
	from pprint import pprint

	hasil = _license.v2_login('chat@auth.com', 'password', bot_id = 1)
	
	# pprint(_license.me())
	pprint(_license.read_notif())
	pprint(_license.get_notif())
	# pprint(_license.get_config())

	# payload = license.getPayload('chat@auth.com', 'password')

	# print(json.dumps(payload))

	# auth = license.getData(payload)
	# print(auth.encode('utf-8'))
	# print(license.cek(auth))
	
	