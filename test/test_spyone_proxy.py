import unittest

import requests

from ..spyone_proxy import SpyOne

class TestSpyOne(unittest.TestCase):
	def  setUp(self):

		self.proxy = SpyOne()

	def test_flow_normal(self):

		self.proxy.get()

		self.assertEqual(self.proxy.proxies.__len__(), 50)

		req = requests.get('https://ifconfig.me/ip', proxies = self.proxy.get_proxy())

		self.assertEqual(req.status_code, 200)

		req.close()




