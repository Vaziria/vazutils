import gevent
from gevent import Greenlet
import subprocess
import os
import shutil
from zipfile import ZipFile
from itertools import cycle
import os

from . import commongit


def get_version(force = False):
	version = 'versi anonim'
	path = 'data/version'
	if os.path.exists(path) and (not force):
		with open(path, 'r') as out:
			version = out.read().strip('\t').strip('\n')

	else:
		version = commongit.get_latest_tag()
		with open(path, 'w+') as out:
			out.write(version)


	return version



class Builder(object):

	dist_path = './dist/'


	def __init__(self, dist_path):
		self.dist_path = dist_path

	def empty_dist(self, ignore = []):
		dist_path = self.dist_path

		for file_object in os.listdir(dist_path):
			file_object_path = os.path.join(dist_path, file_object)
			if os.path.isfile(file_object_path):

				if file_object_path.split('/')[-1] in ignore:
					continue
				else:
					os.unlink(file_object_path)
			else:
				shutil.rmtree(file_object_path)

	def copy_file(self, files):

		for file in files:
			print("copy %s"%file)
			if file[-11:] == '.production':
				distfile = self.dist_path + file[:-11]
			else:
				distfile = self.dist_path + file

			newPath = shutil.copy(file, distfile)

	def copy_folder(self, folders):
		for folder in folders:
			shutil.copytree(folder, self.dist_path + '/' + folder)


	def create_dir_structure(self, folders):
		for folder in folders:
			print("copy %s"%folder)
			os.makedirs(self.dist_path + "/" + folder)

	def create_empty_file(self, files):
		for file in files:
			with open(self.dist_path + '/' + file, 'w+') as out:
				pass

	def zipping_file(self, filename):

		with ZipFile(self.dist_path + filename, 'w') as ziper:

			comment = "Commit Integrity: \n\n{0}".format(self.get_git_revision_hash().decode('utf8'))

			ziper.comment = comment.encode("utf8")

			for root, dirnames, filenames in os.walk(self.dist_path):
				root = root.replace(self.dist_path, '')

				if root != '':
					ziper.write(self.dist_path + '/' + root, root)

				for file in filenames:

					if file == filename:
						continue

					ziper.write(self.dist_path + '/' + root + '/' + file, root + '/' + file)

	def build_exe(self, file_specs, thread = False):

		for file in file_specs:

			dest = None
			if isinstance(file, list):
				dest = file[1]
				file = file[0]

			print("\n\nbuilding %s"%file)

			command = ["pyinstaller", "--onefile", file]
			if thread:
				buildexe = subprocess.call(command, creationflags = subprocess.CREATE_NEW_CONSOLE)
			else:
				buildexe = subprocess.call(command)

			if buildexe == 1:
				print("build %s gagal.."%file)
				return False

			if bool(dest):
				src = self.dist_path + file.replace('.spec', '').replace('.py', '') + '.exe'
				shutil.move(src, self.dist_path + dest)

		return True

	def build_exe_thread(self, files, count):
		params = [[] for _ in range(0, count)]

		point = cycle(params)

		for file in files:
			next(point).append(file)

		params = map(lambda x: gevent.spawn(self.build_exe, x, thread = True), params)

		hasil = map(lambda x: x.value, gevent.joinall(params))

		if False in hasil:
			exit()







	def get_git_revision_hash(self):
		hasil = subprocess.check_output(['git', 'rev-parse', 'HEAD'])
		return hasil

	def get_git_revision_short_hash(self):
		return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

	def build_frontend(self, path):
		oldpath = os.getcwd()
		os.chdir(path)
		command = [
			"ng build --prod=true",

			

		]
		command = " ".join(command)

		hasil = subprocess.call(command, shell=True)
		if hasil == 1:
			print("build frontend gagal")
			exit()

		os.chdir(oldpath)
		print(path + '/dist/' + path.split('/')[-1])
		shutil.copytree(path + '/dist/' + path.split('/')[-1], self.dist_path + 'frontend/')
		self.delete_all('frontend')
		os.removedirs('frontend')
		shutil.copytree(path + '/dist/' + path.split('/')[-1], 'frontend')


	def delete_all(self, path, ignore=[]):
		for file_object in os.listdir(path):
			file_object_path = os.path.join(path, file_object)
			if os.path.isfile(file_object_path):

				if file_object_path.split('/')[-1] in ignore:
					continue
				else:
					os.unlink(file_object_path)
			else:
				shutil.rmtree(file_object_path)