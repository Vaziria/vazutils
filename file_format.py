

class FileFormat:
	
	data = []
	file = ''
	lineformat = []
	key = []

	def __init__(self, file, key, lineformat):

		self.file = file
		self.key = key
		self.lineformat = lineformat

		with open(file, 'r+') as out:
			self.parse(out.read())

	def parse(self, raw):

		keypair = {}

		for item in raw.split('\n'):
			if item.strip('\t').strip(" ").strip('\n') == '':
				continue

			if item[0] == '#':
				item = item.strip('\n').strip('\t')

				parse = item[1:]
				parse = parse.strip().lower().split(':')

				if parse[0] in self.key:
					keypair[parse[0]] = parse[1].upper().strip()


			else:
				if item.find('|') != -1:
					item = item.strip('\n').strip('\t')
					item = item.split('|')


				item = [item.strip('\n').strip('\t')]


				user = {}

				c = 0
				for index in self.lineformat:
					try:
						user[index] = item[c]
					except IndexError as out:
						pass

					c = c+1
				
				user.update(keypair)

				self.data.append(user)

		

if __name__ == '__main__':
	from pprint import pprint