#!/usr/bin/env python3

from os.path import join, abspath, dirname, exists
from os import listdir, remove
from pathlib import Path
from hashlib import md5
from deepinesStore.core import get_dl, get_deepines_uri
from deepinesStore.demoted_actions import config_dir, create_folder, write_file
import threading


class threading_svg(object):

	def __init__(self):
		# Create the config directory if it does not exist
		self.CONFIG_APPS_PATH = config_dir / 'apps'
		if not self.CONFIG_APPS_PATH.exists():
			create_folder(self.CONFIG_APPS_PATH)

		self.RO_APPS_PATH = abspath(join(dirname(__file__), 'resources', 'apps'))
		self.TEMP_PATH = config_dir / 'remote_svg.txt'

		self.RO_APPS_CHECK = dict()
		self.CONFIG_APPS_CHECK = dict()
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
			remove(self.TEMP_PATH)

	def compute_md5(self, file_path):
		hash_md5 = md5()
		with open(file_path, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()

	# Getting the local list of SVGs and its checksums
	def get_local_checksum(self):
		for svg_name in listdir(self.RO_APPS_PATH):
			if svg_name.endswith('.svg'):
				svg_path = join(self.RO_APPS_PATH, svg_name)
				self.RO_APPS_CHECK[svg_name] = self.compute_md5(svg_path)

		for svg_name in listdir(self.CONFIG_APPS_PATH):
			if svg_name.endswith('.svg'):
				svg_path = join(self.CONFIG_APPS_PATH, svg_name)
				self.CONFIG_APPS_CHECK[svg_name] = self.compute_md5(svg_path)

	# Getting the remote list of SVGs and its checksums
	def get_remote_checksum(self):
		SVG_REMOTE = get_dl(get_deepines_uri('/store/config/svg_checksum'))

		status_code = SVG_REMOTE.status_code
		if status_code == 200:
			write_file(SVG_REMOTE, to=self.TEMP_PATH)
			with open(self.TEMP_PATH, 'r') as f:
				for line in f:
					line = line.replace('\n', '')
					(check, space, name) = line.split(' ')
					self.REMOTE_CHECK[name] = check
					self.LIST_SVG_REMOTE.append(name)
		else:
			self.STATUS = False

	# Comparing the checksums and downloading the different file
	def compare_check(self):
		for svg_name in self.REMOTE_CHECK:
			remote_checksum = self.REMOTE_CHECK[svg_name]
			ro_checksum = self.RO_APPS_CHECK.get(svg_name)
			config_checksum = self.CONFIG_APPS_CHECK.get(svg_name)

			# If both exist, and RO_APPS is correct, but CONFIG_APPS is not, remove CONFIG_APPS version
			if ro_checksum == remote_checksum and config_checksum and config_checksum != remote_checksum:
				config_path = join(self.CONFIG_APPS_PATH, svg_name)
				if exists(config_path):
					remove(config_path)
			# If both are correct, remove the CONFIG_APPS version
			elif ro_checksum == remote_checksum and config_checksum == remote_checksum:
				config_path = join(self.CONFIG_APPS_PATH, svg_name)
				if exists(config_path):
					remove(config_path) # I mean... why are you even here? Maybe a new package was released...
			# If neither local copy matches remote, download
			elif (ro_checksum != remote_checksum) and (config_checksum != remote_checksum):
				self.download_svg(svg_name)

		# Remove any local SVGs from config that are not in the remote list
		for svg_name in list(self.CONFIG_APPS_CHECK.keys()):
			if svg_name not in self.REMOTE_CHECK:
				config_path = join(self.CONFIG_APPS_PATH, svg_name)
				# The file should exist as we are iterating keys from that dir,
				# but the check is kept for safety.
				if exists(config_path):
					remove(config_path)

	# Check if it exists in the remote list and download if not exists
	# in the local list
	def check_exists(self):
		for svg_name in self.REMOTE_CHECK:
			if svg_name not in self.RO_APPS_CHECK and svg_name not in self.CONFIG_APPS_CHECK:
				self.download_svg(svg_name)

	def download_svg(self, name):
		dl_svg = get_dl(get_deepines_uri(f'/store/svg/{name}'))
		if dl_svg.status_code == 200:
			write_file(dl_svg, to=join(self.CONFIG_APPS_PATH, name))
