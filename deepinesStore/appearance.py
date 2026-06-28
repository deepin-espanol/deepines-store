import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage
from deepinesStore.demoted_actions import DEF

class AppearanceManager(QObject):
	"""
	Singleton DBus listener that monitors org.deepin.dde.Appearance1
	and broadcasts signals when the system window radius changes.
	"""
	_instance = None
	radius_changed = pyqtSignal(int)

	@classmethod
	def get_instance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		super().__init__()
		self.radius = 4
		address = DEF.env.get("DBUS_SESSION_BUS_ADDRESS")

		# Bypass DBus root rejection by temporarily adopting the user's Effective UID
		original_euid = os.geteuid()
		if original_euid == 0 and DEF.uid != 0:
			os.seteuid(DEF.uid)

		if address:
			self.bus = QDBusConnection.connectToBus(address, "deepines_store_appearance_session")
		else:
			self.bus = QDBusConnection.sessionBus()

		# Restore root privileges immediately after authentication
		if original_euid == 0 and DEF.uid != 0:
			os.seteuid(original_euid)

		if not self.bus.isConnected():
			print(f"Warning: AppearanceManager failed. Error: {self.bus.lastError().message()}")
			return

		self._fetch_initial()

		# Listen for changes
		self.bus.connect(
			"org.deepin.dde.Appearance1",
			"/org/deepin/dde/Appearance1",
			"org.deepin.dde.Appearance1",
			"Changed",
			self.on_changed
		)

	def _fetch_initial(self):
		prop_iface = QDBusInterface(
			"org.deepin.dde.Appearance1",
			"/org/deepin/dde/Appearance1",
			"org.freedesktop.DBus.Properties",
			self.bus
		)

		# Fetch radius
		msg_radius = prop_iface.call("Get", "org.deepin.dde.Appearance1", "WindowRadius")
		if msg_radius.type() != QDBusMessage.ErrorMessage and msg_radius.arguments():
			self.radius = int(msg_radius.arguments()[0])

	@pyqtSlot(QDBusMessage)
	def on_changed(self, msg: QDBusMessage):
		args = msg.arguments()
		if len(args) == 2:
			key = str(args[0])
			val = args[1]

			if key == "WindowRadius":
				try:
					self.radius = int(val)
					self.radius_changed.emit(self.radius)
				except (ValueError, TypeError):
					pass
