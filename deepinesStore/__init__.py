#!/usr/bin/env python3
from deepinesStore.store import run_gui
from deepinesStore.svg import threading_svg
from deepinesStore.maing import get_res
from requests import get
EXCLUIDOS = 'https://raw.githubusercontent.com/deepin-espanol/deepines-store/nightly/deepinesStore/config/excluidos.txt'
DEEPINES = 'https://raw.githubusercontent.com/deepin-espanol/deepines-store/nightly/deepinesStore/config/deepines.txt'


def download_control():
	excluidos = get(EXCLUIDOS)
	open(get_res('excluidos', 'config', '.txt'), 'w', newline='\n').write(excluidos.text)
	deepines = get(DEEPINES)
	open(get_res('deepines', 'config', '.txt'), 'w', newline='\n').write(deepines.text)


def main():
	threading_svg()
	download_control()
	run_gui()
