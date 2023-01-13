#!/usr/bin/env python3
from deepinesStore.store import run_gui
from deepinesStore.svg import threading_svg
from deepinesStore.core import get_dl, get_res, write, get_deepines_uri


def download_control():
	ignore_index = get_dl(get_deepines_uri('/store/config/excluidos.txt'))
	if ignore_index.status_code == 200:
		write(ignore_index, to=get_res('excluidos', 'config', '.txt'))

	deepines_index = get_dl(get_deepines_uri('/store/config/deepines.txt'))
	if deepines_index.status_code == 200:
		write(deepines_index, to=get_res('deepines', 'config', '.txt'))


def main():
	threading_svg()
	download_control()
	run_gui()
