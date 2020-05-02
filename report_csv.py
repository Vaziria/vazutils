import csv
import os

class ReportCsv:
	data = {}
	keys = []
	key = ''
	fname = ''

	def __init__(self, fname, key, keys):
		self.key = key
		self.keys = keys
		self.data = {}
		self.fname = fname


	def add(self, obj):
		idnya = obj[self.key]
		
		item = {}
		for key in self.keys:
			item[key] = obj.get(key, None)

		self.data[idnya] = item

	def save(self):
		h = True
		if os.path.exists(self.fname):
			h = False

		with open(self.fname, 'w+', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = self.keys)
			if h:
				writer.writeheader()

			for key, obj in self.data.items():
				writer.writerow(obj)



		

