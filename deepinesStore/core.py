STORE_VERSION = '[VERSION]'  # TODO: Use Git Hash as fallback.
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
		return get(uri, params=params, **kwargs)
	except Exception as e:
		print(f'DL ERROR: {type(e).__name__}, URI: {uri}')

		class DummyResponse:
			status_code = None
			content = b''
			text = ''  # FIXME: Use some kind of fallback for this, a text file maybe?
		return DummyResponse()


def basic_uri_join(base_uri, *args):
	base_uri = base_uri.strip().rstrip('/')
	relative_paths = [path.strip().lstrip('/') for path in args]
	return f"{base_uri}/{'/'.join(relative_paths)}"


def get_deepines_uri(rel_uri):
	return basic_uri_join(BASE_URI, 'pub', 'deepines', rel_uri)


def tr(m, txt, disambiguation=None, n=-1):
	from PyQt5.QtCore import QCoreApplication
	return QCoreApplication.translate(m.__class__.__name__, txt, disambiguation, n)


def site():
	# FIXME: It copies the link, need to open browser instead.
	from PyQt5.QtWidgets import QApplication
	QApplication.clipboard().setText('https://deepinenespañol.org')


def set_blur(win):
	from os import system
	system('xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {}'.format(int(win.winId())))


def write(b, to):
	# wb should work with text and binary, keeps newlines.
	open(to, 'wb').write(b.content)
