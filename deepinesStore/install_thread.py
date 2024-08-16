import subprocess as sp
from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from deepinesStore.core import default_env
from deepinesStore.app_info import AppType
import deepinesStore.demoted_actions as demoted

class Code(Enum):
	NO_ERROR = 0
	UNHANDLED_ERROR = 1
	NO_INTERNET = 2
	FAIL_DEPS = 3
	APT_LOCKED = 4

# FIXME: Try to run this by elevate to root using set(0, 0)
class External(QObject):
	start = pyqtSignal(object)
	progress = pyqtSignal(object)
	finish = pyqtSignal(object)
	complete = pyqtSignal()
	update = pyqtSignal()
	error = pyqtSignal(Code)

	def __init__(self, app):
		super(External, self).__init__()
		self.app = app
		self.no_net = ('Cannot initiate the connection', 'Could not resolve', 'Temporary failure', 'Unable to fetch')
		self.no_dep = ('Unmet dependencies.', 'The following packages have unmet dependencies:')
		self.locked = ('Could not get lock', 'Unable to acquire the dpkg')
		self.errors = ('Err:', 'Ign:', '101: network is unreachable')

	def run_cmd(self, cmd):
		return sp.Popen(cmd, stdout=sp.PIPE, encoding='utf8', universal_newlines=True, env={**default_env, 'LANG': 'C', 'DEBIAN_FRONTEND': 'noninteractive'})

	def check_string(self, string: str, values: tuple):
		return any(value in string for value in values)

	@pyqtSlot()
	def run(self):
		if any(item.type == AppType.DEB_PACKAGE for item in self.app): # There's at least one Debian app!
			self.apt_update()

		for item in self.app:
			self.code = Code.NO_ERROR
			try: # Let's install!
				app_install_name = item.id
				self.start.emit(app_install_name)
				if item.type == AppType.DEB_PACKAGE:
					self.install_debian_app(app_install_name)
				else:
					self.install_flatpak_app(app_install_name)
			except:
				self.error.emit(Code.UNHANDLED_ERROR)
				return 0
		else: # End for loop.
			self.complete.emit()

	def apt_update(self):
		self.update.emit()
		update = self.run_cmd(["apt", "update"])
		try:
			while not update.poll():
				line = update.stdout.readline()
				if line != '\n':
					self.progress.emit(line)
				if not line:
					break
		except:
			self.error.emit(Code.UNHANDLED_ERROR)

	def install_debian_app(self, app_name: str):
		apt_install = self.run_cmd(["apt", "-q", "-y", "install", app_name, "-t" "stable"])
		while not apt_install.poll():
			line = apt_install.stdout.readline()
			if line:
				print(f"L: {line}", end="")
				if self.check_string(line, self.no_net):
					self.code = Code.NO_INTERNET
				if self.check_string(line, self.no_dep):
					self.code = Code.FAIL_DEPS
				if self.check_string(line, self.locked):
					self.code = Code.APT_LOCKED
				for err in self.errors:  # FIXME: What is this?
					if err in line:
						line = ""
				self.progress.emit(line)
			else:
				if self.code == Code.NO_ERROR:
					self.finish.emit(app_name)
				else:
					self.error.emit(self.code)
					return 0
				break

	def install_flatpak_app(self, app_id: str):
		flatpak_install = demoted.run_cmd(demoted.DEF, cmd=["flatpak", "install", "flathub", "-y", app_id])
		while not flatpak_install.poll():
			line = flatpak_install.stdout.readline()
			if line:
				print(f"L: {line}", end="")
				# FIXME: Handle flatpak errors here!!!
				self.progress.emit(line)
			else:
				if self.code == Code.NO_ERROR:
					self.finish.emit(app_id)
				else:
					self.error.emit(self.code)
					return 0
				break