import apt
import apt.progress.base
import subprocess as sp
import os
from PyQt5.QtCore import QThread, pyqtSignal
from deepinesStore.app_info import AppType, ProcessType
from deepinesStore.core import tr

class ProgressHandler(apt.progress.base.AcquireProgress):
	def __init__(self, update_signal):
		super().__init__()
		self.update_signal = update_signal

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def pulse(self, owner):
		current = self.current_bytes / 1024 / 1024  # Convert to MB
		total = self.total_bytes / 1024 / 1024  # Convert to MB
		if total > 0:
			percent = int(current / total * 100)
			self.update_signal.emit(self.__tr("Downloading... {percent}% ({current:.2f}/{total:.2f} MB)").format(percent=percent, current=current, total=total))
		return True

	def start(self):
		self.update_signal.emit(self.__tr("Starting download..."))

	def stop(self):
		self.update_signal.emit(self.__tr("Download completed"))

class UpdateProgress(apt.progress.base.OpProgress):
	def __init__(self, update_signal):
		super().__init__()
		self.update_signal = update_signal

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def update(self, percent=None):
		if percent:
			self.update_signal.emit(self.__tr("Updating cache... {percent:.2f}%").format(percent=percent))
		else:
			self.update_signal.emit(self.__tr("Updating cache..."))

class InstallProgressHandler(apt.progress.base.InstallProgress):
	def __init__(self, update_signal, process_type):
		super().__init__()
		self.update_signal = update_signal
		self.process_type = process_type

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def status_change(self, pkg, percent, status):
		if self.process_type == ProcessType.INSTALL:
			process = self.__tr("Installing")
		elif self.process_type == ProcessType.UPDATE:
			process = self.__tr("Updating")
		else:
			process = self.__tr("Uninstalling")
		self.update_signal.emit(self.__tr("{process}: {status} - {percent}%").format(process=process, status=status, percent=percent))

class InstallThread(QThread):
	update_signal = pyqtSignal(str)
	name_process_signal = pyqtSignal(str)
	finished_signal = pyqtSignal(bool)

	def __init__(self, package_list):
		super().__init__()
		self.package_list = package_list
		self._is_running = True
		self.first_update = True

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def run(self):
		try:
			for package in self.package_list:
				self.package_process = package.process
				if not self._is_running:
					break
				if package.type == AppType.DEB_PACKAGE:
					if self.first_update:
						cache = apt.Cache()
						self.name_process_signal.emit(self.__tr("Updating package list..."))
						self.update_signal.emit(self.__tr("Updating package list..."))
						import warnings
						try:
							with warnings.catch_warnings(record=True) as w:
								warnings.simplefilter("always")
								cache.update(fetch_progress=ProgressHandler(self.update_signal))

								if w:
									warning_msgs = [str(warn.message) for warn in w]
									# Emit warnings but don't fail if it's just warnings and update succeeded
									# Wait, if an exception is raised, it's handled below
						except apt.cache.FetchFailedException as e:
							error_str = str(e).strip()
							# Check if we caught any warnings that provide more context
							if 'w' in locals() and w:
								error_str = "\n".join([str(warn.message) for warn in w])
							if not error_str:
								error_str = self.__tr("Failed to fetch repositories. Check network connection.")
							error_msg = self.__tr("Error during cache update: {error}").format(error=error_str)
							self.update_signal.emit(error_msg)
							self.finished_signal.emit(False)
							return
						self.first_update = False
					cache.open(progress=UpdateProgress(self.update_signal))
					package_name = package.id

					if self.package_process == ProcessType.INSTALL:
						if not self._install_package(cache, package_name):
							return  # Stop execution if installation fails
					elif self.package_process == ProcessType.UPDATE:
						if not self._update_package(cache, package_name):
							return  # Stop execution if update fails
					elif self.package_process == ProcessType.UNINSTALL:
						if not self._uninstall_package(cache, package_name):
							return  # Stop execution if uninstallation fails

				elif package.type == AppType.FLATPAK_APP:
					app_id = package.id
					if self.package_process == ProcessType.INSTALL:
						if not self._install_flatpak(app_id):
							return  # Stop execution if installation fails
					elif self.package_process == ProcessType.UPDATE:
						if not self._update_flatpak(app_id):
							return  # Stop execution if update fails
					elif self.package_process == ProcessType.UNINSTALL:
						if not self._uninstall_flatpak(app_id):
							return  # Stop execution if uninstallation fails

			if self._is_running:
				self.finished_signal.emit(True)

		except Exception as e:
			import traceback
			error_msg = self.__tr("Error: {error}\n{traceback}").format(error=str(e), traceback=traceback.format_exc())
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)

	def stop(self):
		self._is_running = False
		self.wait()

	def _install_package(self, cache, package_name):
		self.name_process_signal.emit(self.__tr('Installing: {package} from Deepines repository').format(package=package_name))
		self.update_signal.emit(self.__tr("Searching for package {package}...").format(package=package_name))
		if package_name not in cache:
			error_msg = self.__tr("Package {package} not found").format(package=package_name)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		pkg = cache[package_name]
		if pkg.is_installed:
			self.update_signal.emit(self.__tr("{package} is already installed.").format(package=package_name))
		else:
			try:
				self.update_signal.emit(self.__tr("Marking {package} for installation...").format(package=package_name))
				pkg.mark_install()
			except apt.cache.DependencyError as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Unmet dependencies.")
				error_msg = self.__tr("Dependency error for {package}: {error}").format(package=package_name, error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False

			self.update_signal.emit(self.__tr("Downloading and installing {package}...").format(package=package_name))
			try:
				cache.commit(fetch_progress=ProgressHandler(self.update_signal),
							install_progress=InstallProgressHandler(self.update_signal, self.package_process))

				# Check if the package was installed correctly
				cache.open(progress=UpdateProgress(self.update_signal))
				if cache[package_name].is_installed:
					self.update_signal.emit(self.__tr("{package} has been installed successfully.").format(package=package_name))
				else:
					error_msg = self.__tr("{package} could not be installed correctly, possibly due to dependency errors.").format(package=package_name)
					self.update_signal.emit(error_msg)
					self.finished_signal.emit(False)
					return False
			except apt.cache.LockFailedException as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Apt is locked by another process.")
				error_msg = self.__tr("Lock error during installation: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchFailedException as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Failed to download package. Check your network.")
				error_msg = self.__tr("Download error during installation: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchCancelledException as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Cancelled.")
				error_msg = self.__tr("Download cancelled: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except SystemError as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Unknown system error.")
				error_msg = self.__tr("System error during installation: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except Exception as e:
				error_msg = self.__tr("Unexpected error: {error}").format(error=str(e))
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False

		return True

	def _update_package(self, cache, package_name):
		self.name_process_signal.emit(self.__tr('Updating: {package}').format(package=package_name))
		self.update_signal.emit(self.__tr("Searching for package {package}...").format(package=package_name))
		if package_name not in cache:
			error_msg = self.__tr("Package {package} not found").format(package=package_name)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		pkg = cache[package_name]
		if not pkg.is_installed:
			self.update_signal.emit(self.__tr("{package} is not installed, cannot update.").format(package=package_name))
			self.finished_signal.emit(False)
			return False

		if not pkg.is_upgradable:
			self.update_signal.emit(self.__tr("{package} is already at the latest version.").format(package=package_name))
			return True

		try:
			self.update_signal.emit(self.__tr("Marking {package} for upgrade...").format(package=package_name))
			pkg.mark_upgrade()
		except apt.cache.DependencyError as e:
			error_str = str(e).strip() if str(e).strip() else self.__tr("Unmet dependencies.")
			error_msg = self.__tr("Dependency error for {package}: {error}").format(package=package_name, error=error_str)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		self.update_signal.emit(self.__tr("Downloading and updating {package}...").format(package=package_name))
		try:
			cache.commit(fetch_progress=ProgressHandler(self.update_signal),
						install_progress=InstallProgressHandler(self.update_signal, self.package_process))

			# Verify the update
			cache.open(progress=UpdateProgress(self.update_signal))
			if not cache[package_name].is_upgradable:
				self.update_signal.emit(self.__tr("{package} has been updated successfully.").format(package=package_name))
			else:
				error_msg = self.__tr("{package} could not be updated correctly.").format(package=package_name)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
		except apt.cache.LockFailedException as e:
			error_str = str(e).strip() if str(e).strip() else self.__tr("Apt is locked by another process.")
			error_msg = self.__tr("Lock error during update: {error}").format(error=error_str)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False
		except apt.cache.FetchFailedException as e:
			error_str = str(e).strip() if str(e).strip() else self.__tr("Failed to download package. Check your network.")
			error_msg = self.__tr("Download error during update: {error}").format(error=error_str)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False
		except apt.cache.FetchCancelledException as e:
			error_str = str(e).strip() if str(e).strip() else self.__tr("Cancelled.")
			error_msg = self.__tr("Download cancelled: {error}").format(error=error_str)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False
		except SystemError as e:
			error_str = str(e).strip() if str(e).strip() else self.__tr("Unknown system error.")
			error_msg = self.__tr("System error during update: {error}").format(error=error_str)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False
		except Exception as e:
			error_str = str(e).strip() if str(e).strip() else self.__tr("Unknown error.")
			error_msg = self.__tr("Unexpected error: {error}").format(error=error_str)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		return True

	def _uninstall_package(self, cache, package_name):
		self.name_process_signal.emit(self.__tr('Uninstalling: {package}.').format(package=package_name))
		self.update_signal.emit(self.__tr("Searching for package {package}...").format(package=package_name))
		if package_name not in cache:
			error_msg = self.__tr("Package {package} not found").format(package=package_name)
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		pkg = cache[package_name]
		if not pkg.is_installed:
			self.update_signal.emit(self.__tr("{package} is not installed.").format(package=package_name))
		else:
			self.update_signal.emit(self.__tr("Marking {package} for removal...").format(package=package_name))
			pkg.mark_delete()

			self.update_signal.emit(self.__tr("Uninstalling {package}...").format(package=package_name))
			try:
				cache.commit(fetch_progress=ProgressHandler(self.update_signal),
							install_progress=InstallProgressHandler(self.update_signal, self.package_process))

				# Check if the package was uninstalled correctly
				cache.open(progress=UpdateProgress(self.update_signal))
				if not cache[package_name].is_installed:
					self.update_signal.emit(self.__tr("{package} has been uninstalled successfully.").format(package=package_name))
				else:
					error_msg = self.__tr("{package} could not be uninstalled correctly.").format(package=package_name)
					self.update_signal.emit(error_msg)
					self.finished_signal.emit(False)
					return False
			except apt.cache.LockFailedException as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Apt is locked by another process.")
				error_msg = self.__tr("Lock error during uninstallation: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchFailedException as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Failed to download package. Check your network.")
				error_msg = self.__tr("Download error during uninstallation: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except apt.cache.FetchCancelledException as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Cancelled.")
				error_msg = self.__tr("Download cancelled: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except SystemError as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Unknown system error.")
				error_msg = self.__tr("System error during uninstallation: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False
			except Exception as e:
				error_str = str(e).strip() if str(e).strip() else self.__tr("Unknown error.")
				error_msg = self.__tr("Unexpected error: {error}").format(error=error_str)
				self.update_signal.emit(error_msg)
				self.finished_signal.emit(False)
				return False

		return True

	def _install_flatpak(self, app_id):
		installing_msg = self.__tr("Installing {app} from Flathub...").format(app=app_id)
		self.name_process_signal.emit(installing_msg)
		self.update_signal.emit(installing_msg)

		# Prefer system-wide install if system Flathub appstream exists
		use_system = os.path.exists('/var/lib/flatpak/appstream/flathub')
		if use_system:
			# If already running as root, run flatpak --system directly, otherwise elevate with pkexec
			if os.geteuid() == 0:
				cmd = ['flatpak', 'install', '--system', '-y', 'flathub', app_id]
			else:
				cmd = ['/usr/bin/pkexec', '/usr/bin/flatpak', 'install', '--system', '-y', 'flathub', app_id]
		else:
			cmd = ['flatpak', 'install', '-y', 'flathub', app_id]
		process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, text=True)

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
			success_msg = self.__tr("{app} has been installed successfully.").format(app=app_id)
			self.update_signal.emit(success_msg)
		else:
			error_msg = self.__tr("Error installing {app}: {error}").format(app=app_id, error=stderr.strip())
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		return True

	def _uninstall_flatpak(self, app_id):
		uninstalling_msg = self.__tr("Uninstalling {app} from Flathub...").format(app=app_id)
		self.name_process_signal.emit(uninstalling_msg)
		self.update_signal.emit(uninstalling_msg)

		# Prefer system-wide uninstall when system Flathub appstream exists
		use_system = os.path.exists('/var/lib/flatpak/appstream/flathub')
		if use_system:
			if os.geteuid() == 0:
				cmd = ['flatpak', 'uninstall', '--system', '-y', app_id]
			else:
				cmd = ['/usr/bin/pkexec', '/usr/bin/flatpak', 'uninstall', '--system', '-y', app_id]
		else:
			cmd = ['flatpak', 'uninstall', '-y', app_id]
		process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, text=True)

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
			success_msg = self.__tr("{app} has been uninstalled successfully.").format(app=app_id)
			self.update_signal.emit(success_msg)
		else:
			error_msg = self.__tr("Error uninstalling {app}: {error}").format(app=app_id, error=stderr.strip())
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		return True

	def _update_flatpak(self, app_id):
		updating_msg = self.__tr("Updating {app} from Flathub...").format(app=app_id)
		self.name_process_signal.emit(updating_msg)
		self.update_signal.emit(updating_msg)

		# Prefer system-wide update when system Flathub appstream exists
		use_system = os.path.exists('/var/lib/flatpak/appstream/flathub')
		if use_system:
			if os.geteuid() == 0:
				cmd = ['flatpak', 'update', '--system', '-y', app_id]
			else:
				cmd = ['/usr/bin/pkexec', '/usr/bin/flatpak', 'update', '--system', '-y', app_id]
		else:
			cmd = ['flatpak', 'update', '-y', app_id]
		process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, text=True)

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
			success_msg = self.__tr("{app} has been updated successfully.").format(app=app_id)
			self.update_signal.emit(success_msg)
		else:
			error_msg = self.__tr("Error updating {app}: {error}").format(app=app_id, error=stderr.strip())
			self.update_signal.emit(error_msg)
			self.finished_signal.emit(False)
			return False

		return True