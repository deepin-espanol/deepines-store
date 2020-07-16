#!/usr/bin/env python3

from os.path import join, abspath, dirname, isfile
from os import system, listdir
from bs4 import BeautifulSoup

#js-navigation-open link-gray-dark
#deepinesStore/resources/apps/apps

def get_svg():
  BASE = abspath(join(dirname(__file__)))
  PATH = abspath(join(BASE, 'resources/apps'))
  URL_HTML = abspath(join(BASE, 'apps'))
  URL_GITHUB = "https://raw.githubusercontent.com/s384/store_deepines/tree/master/deepinesStore/resources/apps/"

  archivo = open(URL_HTML, "r")
  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(archivo, 'html.parser')
  
  entradas = html.find_all('div')
  lista = list()

  # Obtener los nombres de las apps
  for i, entrada in enumerate(entradas):
    busqueda = entrada.find('a', {'class': 'js-navigation-open link-gray-dark'})
    if busqueda: 
      svg = busqueda.getText()
      if svg not in lista: lista.append(svg)

  # Obtener las imgs ya descargadas
  onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]

  for elemento in lista:
    if elemento not in onlyfiles:
      system("wget -nc -b -P {} {}". format(PATH, join(URL_GITHUB, elemento)))

if __name__ == '__main__':
  get_svg()