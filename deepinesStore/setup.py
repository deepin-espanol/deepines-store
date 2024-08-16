import os
import deepinesStore.demoted_actions as demoted
from deepinesStore.app_info import AppState, ProcessType
from deepinesStore.core import get_res, get_dl, write, get_deepines_uri

def download_control():
	ignore_index = get_dl(get_deepines_uri('/store/config/excluidos.txt'))
	if ignore_index.status_code == 200:
		write(ignore_index, to=get_res('excluidos', 'config', '.txt'))

	deepines_index = get_dl(get_deepines_uri('/store/config/deepines.txt'))
	if deepines_index.status_code == 200:
		write(deepines_index, to=get_res('deepines', 'config', '.txt'))

#		Lista aplicaciones excluidas		  #
def Get_App_Exclude():
	lista = list()
	ruta_excluidos = get_res('excluidos', ext='.txt', dir='config')
	excluidos = open(ruta_excluidos, 'r')

	for line in excluidos:
		line = line.replace('\n', '')
		lista.append(line)

	return lista

#		Lista aplicaciones deepines		  #
def Get_App_Deepines():
	lista = list()
	ruta_deepines = get_res('deepines', ext='.txt', dir='config')
	deepines = open(ruta_deepines, 'r')

	for line in deepines:
		line = line.replace('\n', '')
		lista.append(line)

	return lista

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

	flatpak_cmd = demoted.run_cmd(demoted.DEF, cmd=['flatpak', 'list', '--columns=application'])
	installed_ids = [line.rstrip("\n") for line in flatpak_cmd.stdout.readlines()]

	for installed_id in installed_ids:
		for app_item in list_app_flatpak:
			if installed_id == app_item.id:
				list_installed.append(app_item)
				indice = list_app_flatpak.index(app_item)
				list_app_flatpak[indice].state = AppState.INSTALLED
				list_app_flatpak[indice].process = ProcessType.UNINSTALL

	return(list_installed)
