


class NoteUrl:
	file = None

	def __init__(self, filename, mode = 'a+'):
		self.file = open(filename, mode, encoding = 'utf8')

	def add(self, data):
		if self.find(data):
			return False

		self.file.seek(0, 2)

		self.file.write(data + '\n')

		return True

	def find(self, data):
		self.file.seek(0, 0)

		line = self.file.readline()

		while line:
			if line.replace('\n', '') == data:
				return True

			line = self.file.readline()

		return False

	def first(self):
		self.file.seek(0, 0)
		return self.file.readline().replace('\n', '')


	def pop(self):

		first = self.first()

		if not first:
			return False

		self.delete(first)
		return first


	def delete(self, data):
		self.file.seek(0, 0)

		line = self.file.readline()

		batas = [0, 0]
		getline = False
		lines = []

		while line:
			if line.replace('\n', '') == data:
				batas[0] = self.file.tell()
				batas[1] = line.__len__()
				getline = True

			if getline:
				lines.append(line)

			line = self.file.readline()

		self.file.seek(batas[0] - batas[1], 0)

		for line in lines[1:]:
			self.file.write(line)
