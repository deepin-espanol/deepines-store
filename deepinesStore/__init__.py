#!/usr/bin/env python3
from deepinesStore.tienda import run_gui
from deepinesStore.svg import ThreadingSvg
from deepinesStore.maing import getResource
from requests import get

EXCLUIDOS = 'https://mirror.deepines.com/pub/deepines/store/config/excluidos.txt'
DEEPINES = 'https://mirror.deepines.com/pub/deepines/store/config/deepines.txt'


def download_control():
    excluidos = get(EXCLUIDOS)
    open(getResource('excluidos', 'config', '.txt'), 'w').write(excluidos.text)
    deepines = get(DEEPINES)
    open(getResource('deepines', 'config', '.txt'), 'w').write(deepines.text)


def main():
    ThreadingSvg()
    download_control()
    run_gui()
