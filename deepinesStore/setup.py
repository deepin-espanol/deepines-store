import os
import deepinesStore.demoted_actions as demoted
from deepinesStore.app_info import AppState, ProcessType
from deepinesStore.core import get_res, get_dl, get_deepines_uri
from deepinesStore.demoted_actions import write_file, create_config_dir, config_dir

PATH_EXCLUIDOS = os.path.join(config_dir, 'excluidos.txt')
PATH_DEEPINES = os.path.join(config_dir, 'deepines.txt')


def download_control():
	create_config_dir()

	ignore_index = get_dl(get_deepines_uri('/store/config/excluidos.txt'))
	if ignore_index.status_code == 200:
		write_file(ignore_index, to=PATH_EXCLUIDOS)

	deepines_index = get_dl(get_deepines_uri('/store/config/deepines.txt'))
	if deepines_index.status_code == 200:
		write_file(deepines_index, to=PATH_DEEPINES)

def get_list_from_file(file_path):
	lista = list()
	try:
		with open(file_path, 'r') as file:
			for line in file:
				line = line.strip()  # Remove newline characters
				if line:  # Only add non-empty lines
					lista.append(line)
	except FileNotFoundError:
		print(f"File {file_path} not found.")
	return lista

#		Lista aplicaciones excluidas		  #
def Get_App_Exclude():
	return get_list_from_file(PATH_EXCLUIDOS)

#		Lista aplicaciones deepines		  #
def Get_App_Deepines():
	return get_list_from_file(PATH_DEEPINES)

def get_installed_apps(list_app_deb, list_app_flatpak):
	list_installed = list()

	dpkg_cmd = os.popen("dpkg --get-selections")
	installed_debs = [line.split()[0] for line in dpkg_cmd.read().splitlines() if line.split()[1] == "install"]
	dpkg_cmd.close()

	for installed_deb in installed_debs:
		for app_item in list_app_deb:
			if installed_deb == app_item.id:
				list_installed.append(app_item)
				indice = list_app_deb.index(app_item)
				list_app_deb[indice].state = AppState.INSTALLED
				list_app_deb[indice].process = ProcessType.UNINSTALL

	# Only attempt to query Flatpak if we have Flatpak apps and the
	# demoted environment (DEF) is defined. This avoids errors on
	# platforms where `DEF` isn't available (e.g., Windows) or when
	# AppStream/Flatpak data is missing.
	installed_ids = []
	if list_app_flatpak and hasattr(demoted, 'DEF'):
		try:
			flatpak_proc = demoted.run_cmd(demoted.DEF, cmd=['flatpak', 'list', '--columns=application'])
			installed_ids = [line.rstrip("\n") for line in flatpak_proc.stdout.readlines()]
		except Exception:
			installed_ids = []

	for installed_id in installed_ids:
		for app_item in list_app_flatpak:
			if installed_id == app_item.id:
				list_installed.append(app_item)
				indice = list_app_flatpak.index(app_item)
				list_app_flatpak[indice].state = AppState.INSTALLED
				list_app_flatpak[indice].process = ProcessType.UNINSTALL

	return(list_installed)

def get_updatable_apps(list_app_deb, list_app_flatpak):
	list_updatable = list()

	# Check for deb updates via apt
	try:
		import apt
		cache = apt.Cache()
		cache.open()
		for app_item in list_app_deb:
			if app_item.state == AppState.INSTALLED:
				if app_item.id in cache:
					pkg = cache[app_item.id]
					if pkg.is_upgradable:
						app_item.available_version = pkg.candidate.version
						app_item.state = AppState.UPDATABLE
						app_item.process = ProcessType.UPDATE
						list_updatable.append(app_item)
	except Exception as e:
		print(f"Error checking deb updates: {e}")

	# Check for Flatpak updates
	if list_app_flatpak and hasattr(demoted, 'DEF'):
		try:
			flatpak_proc = demoted.run_cmd(demoted.DEF, cmd=['flatpak', 'remote-ls', '--updates', '--columns=application,version'])
			lines = flatpak_proc.stdout.readlines()
			update_map = {}
			for line in lines:
				parts = line.strip().split('\t')
				if len(parts) >= 2:
					update_map[parts[0]] = parts[1]
				elif len(parts) == 1 and parts[0]:
					update_map[parts[0]] = None

			for app_item in list_app_flatpak:
				if app_item.id in update_map and app_item.state == AppState.INSTALLED:
					app_item.available_version = update_map[app_item.id]
					app_item.state = AppState.UPDATABLE
					app_item.process = ProcessType.UPDATE
					list_updatable.append(app_item)
		except Exception as e:
			print(f"Error checking Flatpak updates: {e}")

	return list_updatable
