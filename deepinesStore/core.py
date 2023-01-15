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

# https://github.com/Peticali/PythonBlurBehind/blob/main/blurWindow/blurWindow.py
import platform
if platform.system() == 'Windows':
	import ctypes
	from ctypes.wintypes import DWORD, BOOL, HRGN, HWND
	user32 = ctypes.windll.user32
	dwm = ctypes.windll.dwmapi

	class ACCENTPOLICY(ctypes.Structure):
		_fields_ = [
			("AccentState", ctypes.c_uint),
			("AccentFlags", ctypes.c_uint),
			("GradientColor", ctypes.c_uint),
			("AnimationId", ctypes.c_uint)
		]

	class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
		_fields_ = [
			("Attribute", ctypes.c_int),
			("Data", ctypes.POINTER(ctypes.c_int)),
			("SizeOfData", ctypes.c_size_t)
		]

	class DWM_BLURBEHIND(ctypes.Structure):
		_fields_ = [
			('dwFlags', DWORD),
			('fEnable', BOOL),
			('hRgnBlur', HRGN),
			('fTransitionOnMaximized', BOOL)
		]

	class MARGINS(ctypes.Structure):
		_fields_ = [("cxLeftWidth", ctypes.c_int),
					("cxRightWidth", ctypes.c_int),
					("cyTopHeight", ctypes.c_int),
					("cyBottomHeight", ctypes.c_int)
					]

	SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
	SetWindowCompositionAttribute.argtypes = (
		HWND, WINDOWCOMPOSITIONATTRIBDATA)
	SetWindowCompositionAttribute.restype = ctypes.c_int


def hex2rgba(HEX: str):
	color = int(HEX[1:], 16)
	return (color & 0xff000000) | ((color & 0xff0000) >> 16) | (color & 0xff00) | ((color & 0xff) << 16)


def win_blur(hwnd, hexColor=False, Acrylic=False, Dark=False):
	accent = ACCENTPOLICY()
	accent.AccentState = 3  # Default window Blur #ACCENT_ENABLE_BLURBEHIND

	gradientColor = 0

	if hexColor != False:
		gradientColor = hex2rgba(hexColor)
		accent.AccentFlags = 2  # Window Blur With Accent Color #ACCENT_ENABLE_TRANSPARENTGRADIENT

	if Acrylic:
		accent.AccentState = 4  # UWP but LAG #ACCENT_ENABLE_ACRYLICBLURBEHIND
		if hexColor == False:  # UWP without color is translucent
			accent.AccentFlags = 2
			gradientColor = hex2rgba('#12121240')  # placeholder color

	accent.GradientColor = gradientColor

	data = WINDOWCOMPOSITIONATTRIBDATA()
	data.Attribute = 19  # WCA_ACCENT_POLICY
	data.SizeOfData = ctypes.sizeof(accent)
	data.Data = ctypes.cast(ctypes.pointer(
		accent), ctypes.POINTER(ctypes.c_int))

	SetWindowCompositionAttribute(int(hwnd), data)

	if Dark:
		data.Attribute = 26  # WCA_USEDARKMODECOLORS
		SetWindowCompositionAttribute(int(hwnd), data)


def set_blur(win):
	if platform.system() == 'Windows':
		win_blur(win.winId(), False, True, True)
	else:  # Linux?, maybe more later...
		from os import system
		system('xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {}'.format(int(win.winId())))


def write(b, to):
	# wb should work with text and binary, keeps newlines.
	open(to, 'wb').write(b.content)
