from PyQt5.QtCore import QThread, pyqtSignal
from deepinesStore.app_info import AppState, ProcessType
import deepinesStore.setup as setup
from deepinesStore.deb.get_apps_deb import fetch_list_app_deb
from deepinesStore.flatpak.get_apps_flatpak import app_list_flatpak

def _fetch_apt_updates(queue, force_refresh):
	try:
		import apt
		cache = apt.Cache()
		if force_refresh:
			try:
				cache.update()
			except apt.cache.FetchFailedException as update_err:
				print(f"Non-fatal fetch warning during apt update: {update_err}")
			except apt.cache.LockFailedException as lock_err:
				raise lock_err
			cache.open(None)
		upgradable = {p.name: p.candidate.version for p in cache if p.is_installed and p.is_upgradable}
		queue.put(upgradable)
	except Exception as e:
		queue.put(e)

class CheckUpdatesThread(QThread):
	finished_signal = pyqtSignal(list)
	error_signal = pyqtSignal(str)

	def __init__(self, list_app_deb, list_app_flatpak, force_refresh=False):
		super().__init__()
		self.list_app_deb = list_app_deb
		self.list_app_flatpak = list_app_flatpak
		self.force_refresh = force_refresh

	def run(self):
		list_updatable = list()

		# Check for deb updates via apt using a clean multiprocessing Process
		import multiprocessing
		queue = multiprocessing.Queue()
		p = multiprocessing.Process(target=_fetch_apt_updates, args=(queue, self.force_refresh))
		p.daemon = True
		p.start()
		p.join()

		if not queue.empty():
			result = queue.get()
			if isinstance(result, Exception):
				self.error_signal.emit(str(result))
				return # Abort update processing on fatal error
			else:
				for app_item in self.list_app_deb:
					if app_item.state in (AppState.INSTALLED, AppState.UPDATABLE):
						if app_item.id in result:
							app_item.available_version = result[app_item.id]
							app_item.state = AppState.UPDATABLE
							app_item.process = ProcessType.UPDATE
							list_updatable.append(app_item)
						elif app_item.state == AppState.UPDATABLE:
							app_item.state = AppState.INSTALLED
							app_item.process = ProcessType.UNINSTALL
							app_item.available_version = ""
		else:
			print("Error: apt update worker returned no data.")

		# Check for Flatpak updates
		import deepinesStore.demoted_actions as demoted
		if self.list_app_flatpak and hasattr(demoted, 'DEF'):
			try:
				if self.force_refresh:
					demoted.run_cmd(demoted.DEF, cmd=['flatpak', 'update', '--appstream'])
					cmd = ['flatpak', 'remote-ls', '--updates', '--columns=application,version']
				else:
					cmd = ['flatpak', 'remote-ls', '--updates', '--cached', '--columns=application,version']

				flatpak_proc = demoted.run_cmd(demoted.DEF, cmd=cmd)
				lines = flatpak_proc.stdout.readlines()
				update_map = {}
				for line in lines:
					parts = line.strip().split('\t')
					if len(parts) >= 2:
						update_map[parts[0]] = parts[1]
					elif len(parts) == 1 and parts[0]:
						update_map[parts[0]] = None

				for app_item in self.list_app_flatpak:
					if app_item.state in (AppState.INSTALLED, AppState.UPDATABLE):
						if app_item.id in update_map:
							app_item.available_version = update_map[app_item.id] or ""
							app_item.state = AppState.UPDATABLE
							app_item.process = ProcessType.UPDATE
							list_updatable.append(app_item)
						elif app_item.state == AppState.UPDATABLE:
							app_item.state = AppState.INSTALLED
							app_item.process = ProcessType.UNINSTALL
							app_item.available_version = ""
			except Exception as e:
				print(f"Error checking flatpak updates: {e}")

		self.finished_signal.emit(list_updatable)

class LoaderThread(QThread):
	progress = pyqtSignal(str)
	finished_data = pyqtSignal(list, list, list, list, list)

	def __init__(self, parent):
		super().__init__()
		self.parent = parent

	def run(self):
		self.progress.emit(self.parent.fetchingString)
		setup.download_control()
		list_app_deepines = setup.Get_App_Deepines()
		list_app_exclude = setup.Get_App_Exclude()
		self.progress.emit(self.parent.initializingString)
		list_app_deb = fetch_list_app_deb(list_app_exclude)
		list_app_flatpak = app_list_flatpak()
		self.progress.emit(self.parent.finalizingString)
		installed = setup.get_installed_apps(list_app_deb, list_app_flatpak)
		list_app_updatable = list()
		self.finished_data.emit(list_app_deepines, list_app_deb, list_app_flatpak, installed, list_app_updatable)
