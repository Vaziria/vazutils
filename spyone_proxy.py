import re
import random

import requests


class SpyOne:

	proxies = []
	key_port = {}


	def get(self, jum = 1):
		url = "http://spys.one/en/http-proxy-list/"
		payload = {
		    'xpp': jum,
		    'xf1': 0,
		    'xf2': 0,
		    'xf4': 0,
		    'xf5': 0,
		}

		req = requests.post(url, data = payload)
		if req.status_code:

			self.parse_port_key(req.text)
			self.parse_proxy(req.text)		

			return True

		return False

	def parse_proxy(self, response):
		pattern = '<tr class=spy1x(.*?)</tr>'

		rawbaris = re.findall(pattern, response)

		for baris in rawbaris:
			ip = self.get_ip(baris)
			if not ip:
				continue

			proc_type = self.get_proc_type(baris)
			port = self.get_port(baris)
			
			proxy = {
				'ip': ip,
				'type': proc_type,
				'port': port
			}

			self.proxies.append(proxy)


	def get_port(self, text):
		pattern = '<script type="text/javascript">(.*?)</script>'

		rawport = re.findall(pattern, text)[0]
		rawport = re.findall('\+\((.*?)\)', rawport)

		hasil = ''
		for item in rawport:

			item = item.split('^')
			item = self.key_port[item[0]] ^ self.key_port[item[1]]
			hasil += str(item)			
		
		return hasil



	def get_proc_type(self, text):
		if text.find('en/https-ssl-proxy/') == -1:
			return 'https'
		else:
			return 'http'

	def get_ip(self, text):
		hasil = re.findall('([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})', text)

		if hasil.__len__() == 0:
			return False

		return hasil[0]


	def parse_port_key(self, response):

		pattern = '<script type="text/javascript">(.*?)</script>'

		rawkey = re.findall(pattern, response)[0]

		for keys in rawkey.split(';'):

			if keys.strip() == '':
				continue

			keys = keys.split('=')

			try:
				self.key_port[keys[0]] = int(keys[1])
			except ValueError as e:
				
				if keys[1].find('^') != -1:
					values = keys[1].split('^')
					self.key_port[keys[0]] = int(values[0]) ^ self.key_port[values[1]]


	def get_proxy(self):
		prox = random.choice(self.proxies)

		proxies = {
		 "http": "{type}://{ip}:{port}".format(**prox),
		 "https": "{type}://{ip}:{port}".format(**prox),
		}

		return proxies



if __name__ == '__main__':

	test = SpyOne()
	test.get()
	prox = test.get_proxy() 
	print(prox)
	req = requests.get('https://ifconfig.me/ip', proxies = prox)

	print(req.text)








