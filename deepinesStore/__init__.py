#!/usr/bin/env python3
from deepinesStore.tienda import ejecutar
from deepinesStore.svg import ThreadingSvg
from os.path import join, abspath, dirname
from requests import get

EXCLUIDOS = 'https://repositorio.deepines.com/pub/deepines/store/config/excluidos.txt'
DEEPINES = 'https://repositorio.deepines.com/pub/deepines/store/config/deepines.txt'
LOCAL_PATH = abspath(join(dirname(__file__)))
PATH_CONTROL = join(LOCAL_PATH, 'config')

def download_control():
  excluidos = get(EXCLUIDOS)
  open(join(PATH_CONTROL, 'excluidos.txt'), 'w').write(excluidos.text)
  deepines = get(DEEPINES)
  open(join(PATH_CONTROL, 'deepines.txt'), 'w').write(deepines.text)

def main():
    ThreadingSvg()
    download_control()
    ejecutar()