import os

from . import commongit

def get_version(force = False):
	path = 'app/version.py'
	version = commongit.get_latest_tag()
	with open(path, 'w+') as out:
		version = "Version = '{}'".format(version)
		out.write(version)


	return version


if __name__ == '__main__':

	print(get_version())