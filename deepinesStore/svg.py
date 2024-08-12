#!/usr/bin/env python3

from os.path import join, abspath, dirname
from os import listdir, remove
from hashlib import md5
from deepinesStore.core import get_dl, write, get_deepines_uri
import threading


class threading_svg(object):

	def __init__(self):
		self.LOCAL_PATH = abspath(join(dirname(__file__)))
		self.PATH_SVG = join(self.LOCAL_PATH, 'resources/apps')
		self.PATH_TEMP = join(self.LOCAL_PATH, 'remote_svg.txt')
		self.LOCAL_CHECK = dict()
		self.REMOTE_CHECK = dict()
		self.LIST_SVG_REMOTE = list()
		self.STATUS = True

		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True  # Daemonize thread
		thread.start()  # Start it!

	def run(self):
		self.get_remote_checksum()
		if self.STATUS:
			self.get_local_checksum()
			self.compare_check()
			self.check_exists()
			remove(self.PATH_TEMP)

	# Getting the local list of SVGs and its checksums
	def get_local_checksum(self):
		for FILE in listdir(self.PATH_SVG):
			hash_md5 = md5()
			full_path_svg = join(self.PATH_SVG, FILE)
			with open(full_path_svg, "rb") as f:
				for chunk in iter(lambda: f.read(4096), b""):
					hash_md5.update(chunk)
			self.LOCAL_CHECK[FILE] = hash_md5.hexdigest()

	# Getting the remote list of SVGs and its checksums
	def get_remote_checksum(self):
		SVG_REMOTE = get_dl(get_deepines_uri('/store/config/svg_checksum'))

		status_code = SVG_REMOTE.status_code
		if status_code == 200:
			write(SVG_REMOTE, to=self.PATH_TEMP)
			with open(self.PATH_TEMP, 'r') as f:
				for line in f:
					line = line.replace('\n', '')
					(check, space, name) = line.split(' ')
					self.REMOTE_CHECK[name] = check
					self.LIST_SVG_REMOTE.append(name)
		else:
			self.STATUS = False

	# Comparing the checksums and downloading the different file
	# Don't delete for now the one that is in local and not in the repo
	def compare_check(self):
		for svg_name in self.LOCAL_CHECK:
			if svg_name not in self.LIST_SVG_REMOTE:
				#remove(join(self.PATH_SVG, svg_name))
				pass
			elif self.LOCAL_CHECK[svg_name] != self.REMOTE_CHECK[svg_name]:
				self.download_svg(svg_name)

	# Check if it exists, so download the file
	def check_exists(self):
		for svg_name in self.REMOTE_CHECK:
			if svg_name not in self.LOCAL_CHECK:
				self.download_svg(svg_name)

	def download_svg(self, name):
		dl_svg = get_dl(get_deepines_uri(f'/store/svg/{name}'))
		if dl_svg.status_code == 200:
			write(dl_svg, to=join(self.PATH_SVG, name))
