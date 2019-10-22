import subprocess
import os


def get_latest_tag():
	hasil = subprocess.check_output(['git', 'describe', '--abbrev=0', '--tags'])
	return hasil.decode('utf8').replace('\n', '')

if __name__ == '__main__':
	pass