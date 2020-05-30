import os
import json

_dir = 'data/external_session'

if not os.path.exists(_dir):
	os.makedirs(_dir)

def save(name, data):
	with open('{}/{}.json'.format(_dir, name), 'w+') as out:
		out.write(json.dumps(data))

def find_and_get(name):
	path = "{}/{}.json".format(_dir, name)

	if os.path.exists(path):
		with open(path, 'r') as out:
			data = json.load(out)

		return data

		return hasil

	return False

if __name__ == '__main__':

	hasil = find_and_get('vaziria')
	print(hasil)
