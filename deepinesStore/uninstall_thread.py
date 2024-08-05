import subprocess as sp
from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from deepinesStore.core import default_env
from deepinesStore.app_info import AppType
import deepinesStore.demoted_actions as demoted

class Code(Enum):
	NO_ERROR = 0
	UNHANDLED_ERROR = 1
	APT_LOCKED = 4

# FIXME: Try to run this by elevate to root using set(0, 0)
class ExternalUninstall(QObject):
	start = pyqtSignal(object)
	progress = pyqtSignal(object)
	finish = pyqtSignal(object)
	complete = pyqtSignal()
	update = pyqtSignal()
	error = pyqtSignal(Code)

	def __init__(self, app):
		super(ExternalUninstall, self).__init__()
		self.app = app
		self.locked = ('Could not get lock', 'Unable to acquire the dpkg')
		self.errors = ('Err:', 'Ign:', '101: network is unreachable')

	def run_cmd(self, cmd):
		return sp.Popen(cmd, stdout=sp.PIPE, encoding='utf8', universal_newlines=True, env={**default_env, 'LANG': 'C', 'DEBIAN_FRONTEND': 'noninteractive'})

	def check_string(self, string: str, values: tuple):
		return any(value in string for value in values)

	@pyqtSlot()
	def run(self):

		self.code = Code.NO_ERROR
		try: # Let's uninstall!
			app_uninstall_name = self.app.id
			self.start.emit(app_uninstall_name)
			if self.app.type == AppType.DEB_PACKAGE:
				self.uninstall_debian_app(app_uninstall_name)
			else:
				self.uninstall_flatpak_app(app_uninstall_name)
		except:
			self.error.emit(Code.UNHANDLED_ERROR)
			return 0
		self.complete.emit()

	def uninstall_debian_app(self, app_name: str):
		apt_uninstall = self.run_cmd(["apt", "-q", "-y", "purge", app_name])
		while not apt_uninstall.poll():
			line = apt_uninstall.stdout.readline()
			if line:
				print(f"L: {line}", end="")
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

	def uninstall_flatpak_app(self, app_id: str):
		flatpak_uninstall = demoted.run_cmd(demoted.DEF, cmd=["flatpak", "uninstall", "--delete-data", "-y", app_id])
		while not flatpak_uninstall.poll():
			line = flatpak_uninstall.stdout.readline()
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