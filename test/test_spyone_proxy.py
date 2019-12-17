import unittest

from ..spyone_proxy import SpyOne

class TestSpyOne(unittest.TestCase):
	def  setUp(self):

		self.proxy = SpyOne()

	def test_flow_normal(self):

		self.proxy.get()

		self.assertEqual(self.proxy.proxies.__len__(), 100)




