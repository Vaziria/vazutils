import unittest

from ..note_url import NoteUrl


class TestNoteUrl(unittest.TestCase):

	def setUp(self):

		self.file = NoteUrl('test_note_url.txt', 'w+')

	def test_add_file(self):

		items = ['asd', 'asd2', 'asd3', 'asd4', 'asd5', 'asd5', 'asd1', 'end']

		for item in items:
			self.file.add(item)

		self.file.delete('asd2')

		for c in ['asdasd', 'asdasd', 'asdasd', 'asdasd', 'asdasd', 'asdasd', 'asdasd', 'asdasd', 'asdasd', 'asdasd']:
			self.file.file.write(c + '\n')

	def tearDown(self):
		self.file.file.close()



if __name__ == '__main__':

	unittest.main()