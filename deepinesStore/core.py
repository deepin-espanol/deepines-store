from os import environ as env, name
import argparse
import json


def get_ver():
	version = '[VERSION]'
	if "VERSION" in version:
		import subprocess
		version = subprocess.check_output(["git", "describe", "--dirty"]).strip().decode("utf-8")
	return version


STORE_VERSION = get_ver()
BASE_URI = 'https://repositorio.deepines.com'


def get_res(res_name, dir='resources', ext='.svg'):
	from os.path import join, abspath, dirname
	return abspath(join(dirname(__file__), dir, res_name + ext))


def get_app_icon():
	from PyQt5.QtGui import QIcon
	return QIcon.fromTheme('deepines', QIcon(get_res('deepines')))


def get_dl(uri, params=None, **kwargs):
	from requests import get
	try:
		response = get(uri, params=params, **kwargs)
		response.raise_for_status()
		return response
	except Exception as e:
		from sys import stderr
		print(f'DL ERROR: {type(e).__name__}, URI: {uri}', file=stderr)

		class DummyResponse:
			status_code = None
			content = b''
			text = ''
			def json(self): return {}
		return DummyResponse()


def uri_join(base_uri, *args):
	base_uri = base_uri.rstrip('/')
	relative_paths = list(map(lambda x: x.lstrip('/'), args))
	return f"{base_uri}/{'/'.join(relative_paths)}"


def get_deepines_uri(rel_uri):
	return uri_join(BASE_URI, 'pub', 'deepines', rel_uri)

def get_text_link(text, uri=None, additional_style='color: #004EE5;'):
	if uri is None:
		if text.startswith("@"):
			uri = f"https://t.me/{text[1:]}"
		else:
			uri = f"https://{text}"
	return f"<a href='{uri}' style='text-decoration: none; {additional_style}'>{text}</a>"

def tr(m, txt, disambiguation=None, n=-1):
	from PyQt5.QtCore import QCoreApplication
	return QCoreApplication.translate(m.__class__.__name__, txt, disambiguation, n)

def set_blur(win):
	import platform
	if platform.system() == 'Windows':
		pass
	else:  # Linux?, maybe more later...
		from os import system
		system('xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {}'.format(int(win.winId())))


def write(b, to):
	with open(to, 'wb') as ftw:
		ftw.write(b.content)


if name == 'nt':
	try:
		from ctypes import windll
		windll.shell32.SetCurrentProcessExplicitAppUserModelID('Deepines Store')
	except AttributeError:
		# Not available?
		pass

parser = argparse.ArgumentParser()
parser.add_argument("--env", help="Serialized user environment as JSON")
args = parser.parse_args()

default_env = env.copy()

if args.env:
	new_env = json.loads(args.env)
	default_env.update(new_env)
	env.update({k: v for k, v in default_env.items() if k != 'XDG_RUNTIME_DIR'})