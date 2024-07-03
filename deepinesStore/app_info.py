from enum import Enum


class AppType(Enum):
	DEB_PACKAGE = 0
	FLATPAK_APP = 1


class AppState(Enum):
	SELECTED = 0
	DEFAULT = 1
	INSTALLED = 2
	UNINSTALLED = 3
	UNINSTALL = 4

class ProcessType(Enum):
	INSTALL = 0
	UNINSTALL = 1

class AppInfo:
	def __init__(self, name: str, id: str, description: str, version = "0", category = "otros", type=AppType.DEB_PACKAGE, state=AppState.DEFAULT, process=ProcessType.INSTALL):
		self.name = name
		self.id = id
		self.description = description
		self.version = version
		self.category = category
		self.state = state
		self.type = type
		self.process = process