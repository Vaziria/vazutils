import random
import os

class UserAgent(object):

	filetxt = None
	
	data = [
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
	]

	def __init__(self, filetxt = None):
		self.filetxt = filetxt

		if filetxt:
			self.txt_get(filetxt)

	def txt_get(self, fname):

		if os.path.exists(fname):
			
			with open(fname, 'r') as out:
				hasil = out.read()

			for item in hasil.split('\n'):
				item = item.strip('\n').strip('\t')
				if bool(item):
					self.data.append(item)

			return True

		else:
			return False


	def get(self):
		return random.choice(self.data)

_useragent = UserAgent(filetxt = 'data/user_agent.txt')


if __name__ == '__main__':

	hasil = _useragent.get()

	print(hasil)