import json
from deepinesStore.demoted_actions import config_dir, write_file

class SettingsManager:
	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.settings_file = config_dir / 'settings.json'
		self._data = {
			"auto_update": True,
			"geometry": None
		}
		self._load()

	def _load(self):
		if self.settings_file.exists():
			try:
				with open(self.settings_file, 'r') as f:
					data = json.load(f)
					self._data.update(data)
			except Exception as e:
				print(f"Failed to load settings: {e}")

	def save(self):
		try:
			json_bytes = json.dumps(self._data).encode('utf-8')
			dummy = type('obj', (object,), {'content': json_bytes})
			write_file(dummy, self.settings_file)
		except Exception as e:
			print(f"Failed to save settings: {e}")

	def get(self, key, default=None):
		return self._data.get(key, default)

	def set(self, key, value):
		self._data[key] = value
		self.save()
