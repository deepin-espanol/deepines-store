from os import environ as env, name
import argparse


def get_ver():
	version = '[VERSION]'
	if "VERSION" in version:
		import subprocess
		version = subprocess.check_output(["git", "describe"]).strip().decode("utf-8")
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


def tr(m, txt, disambiguation=None, n=-1):
	from PyQt5.QtCore import QCoreApplication
	return QCoreApplication.translate(m.__class__.__name__, txt, disambiguation, n)


def site():
	# FIXME: It copies the link, need to open browser instead.
	from PyQt5.QtWidgets import QApplication
	QApplication.clipboard().setText('https://deepinenespañol.org')


def set_blur(win):
	import platform
	if platform.system() == 'Windows':
		pass
	else:  # Linux?, maybe more later...
		from os import system
		system('xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {}'.format(int(win.winId())))


def write(b, to):
	# wb should work with text and binary, keeps newlines.
	open(to, 'wb').write(b.content)


if name == 'nt':
	try:
		from ctypes import windll
		windll.shell32.SetCurrentProcessExplicitAppUserModelID('Deepines Store')
	except AttributeError:
		# Not available?
		pass

parser = argparse.ArgumentParser()
parser.add_argument("-l", type=str)  # locale
parser.add_argument("-d", type=str)  # desktop
args = parser.parse_args()

if args.l:
	lang = args.l
else:
	import locale
	lang = locale.getdefaultlocale()[0]

if args.d:
	env['XDG_CURRENT_DESKTOP'] = args.d

default_env = env.copy()
