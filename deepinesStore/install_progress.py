# TODO: Localize for 1.4.1
import apt
import apt.progress.base
import subprocess as sp
from PyQt5.QtCore import QThread, pyqtSignal
from deepinesStore.app_info import AppType, ProcessType

class ProgressHandler(apt.progress.base.AcquireProgress):
	def __init__(self, update_signal):
		super().__init__()
		self.update_signal = update_signal

	def pulse(self, owner):
		current = self.current_bytes / 1024 / 1024  # Convert to MB
		total = self.total_bytes / 1024 / 1024  # Convert to MB
		if total > 0:
			percent = int(current / total * 100)
			self.update_signal.emit(f"Downloading... {percent}% ({current:.2f}/{total:.2f} MB)")
		return True

	def start(self):
		self.update_signal.emit("Starting download...")

	def stop(self):
		self.update_signal.emit("Download completed")

class UpdateProgress(apt.progress.base.OpProgress):
	def __init__(self, update_signal):
		super().__init__()
		self.update_signal = update_signal

	def update(self, percent=None):
		if percent:
			self.update_signal.emit(f"Updating cache... {percent:.2f}%")
		else:
			self.update_signal.emit("Updating cache...")

class InstallProgressHandler(apt.progress.base.InstallProgress):
	def __init__(self, update_signal, process_type):
		super().__init__()
		self.update_signal = update_signal
		self.process_type = process_type

	def status_change(self, pkg, percent, status):
		if self.process_type == ProcessType.INSTALL:
			process = "Installing"
		else:
			process = "Uninstalling"
		self.update_signal.emit(f"{process}: {status} - {percent}%")

class InstallThread(QThread):
	update_signal = pyqtSignal(str)
	name_process_signal = pyqtSignal(str)
	finished_signal = pyqtSignal(bool)

	def __init__(self, package_list):
		super().__init__()
		self.package_list = package_list
		self._is_running = True
		self.first_update = True

	def run(self):
		try:
			for package in self.package_list:
				self.package_process = package.process
				if not self._is_running:
					break
				if package.type == AppType.DEB_PACKAGE:
					if self.first_update:
						cache = apt.Cache()
						self.name_process_signal.emit("Updating package list...")
						self.update_signal.emit("Updating package list...")
						try:
							cache.update(fetch_progress=ProgressHandler(self.update_signal))
						except apt.cache.FetchFailedException as e:
							error_msg = f"Error during cache update: {str(e)}"
							self.update_signal.emit(error_msg)
							self.finished_signal.emit(False)
							return
						self.first_update = False
					cache.open(progress=UpdateProgress(self.update_signal))
					package_name = package.id

					if self.package_process == ProcessType.INSTALL:
						if not self._install_package(cache, package_name):
							return  # Stop execution if installation fails
					elif self.package_process == ProcessType.UNINSTALL:
						if not self._uninstall_package(cache, package_name):
							return  # Stop execution if uninstallation fails

				elif package.type == AppType.FLATPAK_APP:
					app_id = package.id
					if self.package_process == ProcessType.INSTALL:
						if not self._install_flatpak(app_id):
							return  # Stop execution if installation fails
					elif self.package_process == ProcessType.UNINSTALL:
						if not self._uninstall_flatpak(app_id):
							return  # Stop execution if uninstallation fails

			if self._is_running:
				self.finished_signal.emit(True)

		except Exception as e:
			import traceback
			error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)

	def stop(self):
		self._is_running = False
		self.wait()

	def _install_package(self, cache, package_name):
		self.name_process_signal.emit(f'Installing: {package_name} from Deepines repository')
		self.update_signal.emit(f"Searching for package {package_name}...")
		if package_name not in cache:
			error_msg = f"Package {package_name} not found"
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		pkg = cache[package_name]
		if pkg.is_installed:
			self.update_signal.emit(f"{package_name} is already installed.")
		else:
			try:
				self.update_signal.emit(f"Marking {package_name} for installation...")
				pkg.mark_install()
			except apt.cache.DependencyError as e:
				error_msg = f"Dependency error for {package_name}: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False

			self.update_signal.emit(f"Downloading and installing {package_name}...")
			try:
				cache.commit(fetch_progress=ProgressHandler(self.update_signal),
							install_progress=InstallProgressHandler(self.update_signal, self.package_process))

				# Check if the package was installed correctly
				cache.open(progress=UpdateProgress(self.update_signal))
				if cache[package_name].is_installed:
					self.update_signal.emit(f"{package_name} has been installed successfully.")
				else:
					error_msg = f"{package_name} could not be installed correctly, possibly due to dependency errors."
					self.update_signal.emit(error_msg)
					self.finished_signal.emit(False)
					return False
			except apt.cache.LockFailedException as e:
				error_msg = f"Lock error during installation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchFailedException as e:
				error_msg = f"Download error during installation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchCancelledException as e:
				error_msg = f"Download cancelled: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except SystemError as e:
				error_msg = f"System error during installation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except Exception as e:
				error_msg = f"Unexpected error: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False

		return True

	def _uninstall_package(self, cache, package_name):
		self.name_process_signal.emit(f'Uninstalling: {package_name}.')
		self.update_signal.emit(f"Searching for package {package_name}...")
		if package_name not in cache:
			error_msg = f"Package {package_name} not found"
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		pkg = cache[package_name]
		if not pkg.is_installed:
			self.update_signal.emit(f"{package_name} is not installed.")
		else:
			self.update_signal.emit(f"Marking {package_name} for removal...")
			pkg.mark_delete()

			self.update_signal.emit(f"Uninstalling {package_name}...")
			try:
				cache.commit(fetch_progress=ProgressHandler(self.update_signal),
							install_progress=InstallProgressHandler(self.update_signal, self.package_process))

				# Check if the package was uninstalled correctly
				cache.open(progress=UpdateProgress(self.update_signal))
				if not cache[package_name].is_installed:
					self.update_signal.emit(f"{package_name} has been uninstalled successfully.")
				else:
					error_msg = f"{package_name} could not be uninstalled correctly."
					self.update_signal.emit(error_msg)
					self.finished_signal.emit(False)
					return False
			except apt.cache.LockFailedException as e:
				error_msg = f"Lock error during uninstallation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchFailedException as e:
				error_msg = f"Download error during uninstallation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.InstallFailedException as e:
				error_msg = f"Error during uninstallation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except SystemError as e:
				error_msg = f"System error during uninstallation: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except Exception as e:
				error_msg = f"Unexpected error: {str(e)}"
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False

		return True

	def _install_flatpak(self, app_id):
		self.name_process_signal.emit(f"Installing {app_id} from Flathub...")
		self.update_signal.emit(f"Installing {app_id} from Flathub...")

		process = sp.Popen(['flatpak', 'install', '-y', 'flathub', app_id], stdout=sp.PIPE, stderr=sp.PIPE, text=True)

		while True:
			if not self._is_running:
				process.terminate()
				break
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				self.update_signal.emit(output.strip())

		stderr = process.communicate()[1]
		if stderr:
			self.update_signal.emit(stderr.strip())

		if process.returncode == 0:
			self.update_signal.emit(f"{app_id} has been installed successfully.")
		else:
			error_msg = f"Error installing {app_id}: {stderr}"
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		return True

	def _uninstall_flatpak(self, app_id):
		self.name_process_signal.emit(f"Uninstalling {app_id} from Flathub...")
		self.update_signal.emit(f"Uninstalling {app_id} from Flathub...")

		process = sp.Popen(['flatpak', 'uninstall', '-y', app_id], stdout=sp.PIPE, stderr=sp.PIPE, text=True)

		while True:
			if not self._is_running:
				process.terminate()
				break
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				self.update_signal.emit(output.strip())

		stderr = process.communicate()[1]
		if stderr:
			self.update_signal.emit(stderr.strip())

		if process.returncode == 0:
			self.update_signal.emit(f"{app_id} has been uninstalled successfully.")
		else:
			error_msg = f"Error uninstalling {app_id}: {stderr}"
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		return True