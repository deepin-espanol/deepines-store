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

	dpkg_cmd = os.popen("dpkg-query -W -f='${Package}\\t${Version}\\n'")
	installed_debs = {}
	for line in dpkg_cmd.read().splitlines():
		parts = line.split('\t')
		if len(parts) == 2:
			installed_debs[parts[0]] = parts[1]
	dpkg_cmd.close()

	for app_item in list_app_deb:
		if app_item.id in installed_debs:
			list_installed.append(app_item)
			app_item.state = AppState.INSTALLED
			app_item.process = ProcessType.UNINSTALL
			app_item.version = installed_debs[app_item.id]

	# Only attempt to query Flatpak if we have Flatpak apps and the
	# demoted environment (DEF) is defined. This avoids errors on
	# platforms where `DEF` isn't available (e.g., Windows) or when
	# AppStream/Flatpak data is missing.
	installed_ids = []
	installed_info = {}
	if list_app_flatpak and hasattr(demoted, 'DEF'):
		try:
			flatpak_proc = demoted.run_cmd(demoted.DEF, cmd=['flatpak', 'list', '--columns=application,version'])
			for line in flatpak_proc.stdout.readlines():
				parts = line.rstrip("\n").split("\t")
				if len(parts) >= 1:
					installed_info[parts[0]] = parts[1] if len(parts) > 1 else ""
		except Exception:
			pass

	for installed_id, installed_version in installed_info.items():
		for app_item in list_app_flatpak:
			if installed_id == app_item.id:
				list_installed.append(app_item)
				indice = list_app_flatpak.index(app_item)
				list_app_flatpak[indice].state = AppState.INSTALLED
				list_app_flatpak[indice].process = ProcessType.UNINSTALL
				if installed_version:
					list_app_flatpak[indice].version = installed_version

	return(list_installed)

