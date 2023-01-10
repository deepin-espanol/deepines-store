#!/usr/bin/env python3
from deepinesStore.store import run_gui
from deepinesStore.svg import threading_svg
from deepinesStore.core import get_dl, get_res
EXCLUIDOS = 'https://mirror.deepines.com/pub/deepines/store/config/excluidos.txt'
DEEPINES = 'https://mirror.deepines.com/pub/deepines/store/config/deepines.txt'

def download_control():
	excluidos = get_dl(EXCLUIDOS)
	open(get_res('excluidos', 'config', '.txt'), 'w', newline='\n').write(excluidos.text)
	deepines = get_dl(DEEPINES)
	open(get_res('deepines', 'config', '.txt'), 'w', newline='\n').write(deepines.text)


def main():
	threading_svg()
	download_control()
	run_gui()
