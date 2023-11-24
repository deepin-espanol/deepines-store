import deepinesStore.demoted_actions as actions
from deepinesStore.core import get_dl

# Categorias de app en flathub
categories = [
		"AudioVideo", "Development", "Education", "Games", "Game", "Productivity",
		"Graphics", "Network", "Office", "Science", "System", "Utility"
	]

# Obtenemos  las apps desde el api de flathub
def fetch_list_app_flatpak():
	api_url = "https://flathub.org/api/v1/apps"
	try:
		request = get_dl(api_url, timeout=20)
		app_list = list()
		for app in request.json():
			name = app['name']
			description = app['summary']
			category = "None"
			state = 1
			appID = app['flatpakAppId']
			app_info = [name, description, 'None', category, state, appID]
			app_list.append(app_info)
		
	except Exception as e:
		print("Error fetching apps:", e)
		return []
	return app_list


def fetch_apps_by_category(category):
	try:
		api_url = f"https://flathub.org/api/v1/apps/category/{category}"
		request = get_dl(api_url, timeout=20)
		return request.json() if request.status_code == 200 else []
	except Exception as e:
		print(f"Error fetching apps in category {category}:", e)
		return []

def two_columns_split(output: str):
	lines = output.split('\n')
	result = {}
	for line in lines:
		columns = line.split(maxsplit=1)
		if len(columns) == 2:
			result[columns[0]] = columns[1].strip()

	return result

app_id_ver_dict = two_columns_split(actions.get_flatpak_info_cmd())

def add_apps_dict_by_categories():
	app_data = {}
	for category in categories:
		app_data[category] = fetch_apps_by_category(category)
	return app_data

def apps_flatpak_in_categories():
	app_data = add_apps_dict_by_categories()
	lista = list()
	lista_agregados = list()
	for category in categories:
		for app in app_data[category]:
			if not app['flatpakAppId'] in lista_agregados: 
				titulo = app['name']
				descripcion = app['summary']
				categoria = category
				estado = 1
				install = app['flatpakAppId']
				version = app_id_ver_dict.get(install) or "No version"
				lista_origen = [titulo, descripcion, version, categoria, estado, install, 1]
				lista_agregados.append(install)
				lista.append(lista_origen)
	
	lista.sort()
	return lista