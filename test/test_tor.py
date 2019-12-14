import unittest
import os

from ..tor import Tor

class TestTor(unittest.TestCase):

	def setUp(self):
		self.tor = Tor()
	
	def test_open(self):

		self.tor.run()
		self.assertTrue(self.tor.running)

	def test_change_relay(self):
		self.tor.run()
		self.tor.change_relay()

	def test_run_two_service(self):
		# self.tor.run()
		tor1 = Tor(port = 9056, controll_port = 9057, fconfig = 'tor1')
		tor2 = Tor(port = 9052, controll_port = 9053, fconfig = 'tor2')

		tor1.run()
		tor2.run()

		tor1.check_ip()
		tor2.check_ip()

		tor1.close()
		tor2.close()

		os.remove('tor1')
		os.remove('tor2')

	def test_timeout_sedikit(self):

		self.tor.timeout = 1

		self.run()



	def  tearDown(self):

		self.tor.close()





if __name__ == '__main__':
	unittest.main()