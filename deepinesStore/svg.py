#!/usr/bin/env python3

from os.path import join, abspath, dirname, isfile
from os import system, listdir
from bs4 import BeautifulSoup
import threading

#js-navigation-open link-gray-dark
#deepinesStore/resources/apps/apps



class ThreadingSvg(object):

  def __init__(self):
    self.BASE = abspath(join(dirname(__file__)))
    self.PATH = abspath(join(self.BASE, 'resources/apps'))
    self.URL_HTML = "https://github.com/s384/store_deepines/tree/Develop/deepinesStore/resources/apps"
    self.URL_GITHUB = "https://github.com/s384/store_deepines/raw/Develop/deepinesStore/resources/apps"
    self.HTML_PATH = abspath(join(self.BASE, 'apps'))

    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

  def run(self):
    system("wget -O {} -P {} {}". format(join(self.BASE, "apps"), self.BASE, self.URL_HTML))
    archivo = open(self.HTML_PATH, "r")
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
    onlyfiles = [f for f in listdir(self.PATH) if isfile(join(self.PATH, f))]
    for elemento in lista:
      if elemento not in onlyfiles:
        system("wget -q -nc -P {} {}". format(self.PATH, join(self.URL_GITHUB, elemento)))
        #subprocess.run(["wget", "-nc", "-P", self.PATH, join(self.URL_GITHUB, elemento)])
    