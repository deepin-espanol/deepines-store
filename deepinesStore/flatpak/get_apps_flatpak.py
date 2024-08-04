import deepinesStore.demoted_actions as actions
from deepinesStore.app_info import AppInfo, AppType
from deepinesStore.core import get_dl_multi

# Categorias de app en flathub
categories = [
		"AudioVideo", "Development", "Education", "Games", "Game", "Productivity",
		"Graphics", "Network", "Office", "Science", "System", "Utility"
	]


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
	category_uris = [f"https://flathub.org/api/v1/apps/category/{category}" for category in categories]
	responses = get_dl_multi(category_uris, timeout=20)
	for category, response in zip(categories, responses):
		if response.status_code == 200:
			app_data[category] = response.json()
		else:
			app_data[category] = []
			print(f"Failed to fetch apps for category: {category}")
	return app_data

def apps_flatpak_in_categories() -> list[AppInfo]:
	app_data = add_apps_dict_by_categories()
	fp_app_info = list()
	already_added = list()
	for category in categories:
		for app in app_data[category]: # FIXME: This is not adding some "uncategorized" apps
			app_id = app['flatpakAppId']
			if not app_id in already_added: 
				version = app_id_ver_dict.get(app_id)
				app_info = AppInfo(app['name'], app_id, app['summary'], version, category, AppType.FLATPAK_APP)
				already_added.append(app_id)
				fp_app_info.append(app_info)
	
	return fp_app_info