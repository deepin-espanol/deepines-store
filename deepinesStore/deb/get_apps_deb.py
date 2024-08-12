from typing import List
from lxml import html
import re

from deepinesStore.app_info import AppInfo
from deepinesStore.core import get_deepines_uri, get_dl


def get_repo_url():
	fallback_url = get_deepines_uri("/5/paquetes.html")
	repo_file = "/etc/apt/sources.list.d/deepines.list"
	try:
		repo_text = open(repo_file).read()
		url = re.search(
			"(?P<url>https?://[^\s]+)", repo_text).group("url") + "paquetes.html"
		return url
	except:
		return fallback_url


def fetch_list_app_deb(list_ignored: List[str]) -> List[AppInfo]:
	repo_url = get_repo_url()
	request = get_dl(repo_url, timeout=10)

	if request.status_code == 200:
		html_tree = html.fromstring(request.content.decode("utf-8"))
		entries = html_tree.xpath('//tr')
		deb_app_info = []

		def from_cell(entry, class_name: str):
			return entry.xpath(f'.//td[@class="{class_name}"]/text()')[0].strip()

		for entry in entries:
			app_title = from_cell(entry, 'package')
			if app_title not in list_ignored:
				app_info = AppInfo(app_title, app_title, from_cell(
					entry, 'description'), from_cell(entry, 'version'), from_cell(entry, 'section'))
				deb_app_info.append(app_info)

		return deb_app_info
	else:
		print(
			f"App list fetch request has failed with status code {request.status_code}")
		return []
