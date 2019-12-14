import unittest
import time

import requests

from .. import tor_wrapper

_path = 'D:/portable/work/dewa_petir'
tor_wrapper.tor_open(_path)


time.sleep(10)



class TestTorWrapper(unittest.TestCase):
	
	def setUp(self):
		self.path = _path
	def test_open_tor(self):
		tor_wrapper.tor_open(self.path)

	def test_open_config(self):
		tor_wrapper.generate_config(self.path)

	def test_request(self):
		original = requests.get('http://ifconfig.me/ip')
		original.close()

		proxy = {
			'http': 'socks5://127.0.0.1:9050',
			'https': 'socks5://127.0.0.1:9050'
		}

		proxified = requests.get('http://ifconfig.me/ip', proxies=proxy)
		proxified.close()

		print("""
				original ip : {}
				proxy ip : {}

			""".format(original.text, proxified.text))

		self.assertNotEqual(original.text, proxified.text)

		
	

if __name__ == '__main__':
	unittest.main()