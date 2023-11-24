from lxml import html
import re

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

def fetch_list_app_deb(list_ignored):
	repo_url = get_repo_url()
	request = get_dl(repo_url, timeout=10)

	if request.status_code == 200:
		html_tree = html.fromstring(request.content.decode("utf-8"))
		entries = html_tree.xpath('//tr')
		the_app_list = []

		for entry in entries:
			app_title = entry.xpath('.//td[@class="package"]/text()')[0]
			if app_title not in list_ignored:
				the_app_list.append([
					app_title,  # Name
					entry.xpath('.//td[@class="description"]/text()')[0],  # Description
					entry.xpath('.//td[@class="version"]/text()')[0],  # Version
					entry.xpath('.//td[@class="section"]/text()')[0],  # Category
					1,  # State
					app_title,  # "ID" (package name)
					0,  # Type (.deb in this case)
				])

		return the_app_list
	else:
		print(f"Flatpak app list fetch request has failed with status code {request.status_code}")
		return []
