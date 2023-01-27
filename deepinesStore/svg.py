#!/usr/bin/env python3

from os.path import join, abspath, dirname
from os import listdir, remove
from hashlib import md5
from requests import get
import threading


class ThreadingSvg(object):

  def __init__(self):
    self.URL_REPO_SVG = 'https://repositorio.deepines.com/pub/deepines/store/svg/'
    self.URL_REMOTE_SUMS = 'https://repositorio.deepines.com/pub/deepines/store/config/svg_checksum'
    self.LOCAL_PATH = abspath(join(dirname(__file__)))
    self.PATH_SVG = join(self.LOCAL_PATH, 'resources/apps')
    self.RUTA_TEMP = join(self.LOCAL_PATH, 'remote_svg.txt')
    self.LOCAL_CHECK = dict()
    self.REMOTE_CHECK = dict()
    self.LIST_SVG_REMOTE = list()
    self.STATUS = True

    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

  def run(self):
    self.get_remote_checksum()
    if self.STATUS:
      self.get_local_checksum()
      self.compare_check()
      self.check_exists()
      remove(self.RUTA_TEMP)

  
  # Obteniendo la lista local de svg y su checksum
  def get_local_checksum(self):
    for FILE in listdir(self.PATH_SVG):
      hash_md5 = md5()
      full_path_svg = join(self.PATH_SVG, FILE)
      with open(full_path_svg, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
          hash_md5.update(chunk)
      self.LOCAL_CHECK[FILE] = hash_md5.hexdigest()

  # Obteniendo la lista remota de svg y su checksum
  def get_remote_checksum(self):
    SVG_REMOTE = get(self.URL_REMOTE_SUMS)
    
    status_code = SVG_REMOTE.status_code
    if status_code == 200:
      open(self.RUTA_TEMP, 'w').write(SVG_REMOTE.text)
      with open(self.RUTA_TEMP, 'r') as f:
        for line in f:
          line = line.replace('\n','')
          (check, space, name) = line.split(' ')
          self.REMOTE_CHECK[name] = check
          self.LIST_SVG_REMOTE.append(name)
    else: self.STATUS = False
      
  # Comparando los checksum y descarga el archivo distinto
  # Borra aquel que este en local y no en el repo
  def compare_check(self):
    for svg_name in self.LOCAL_CHECK:
      if svg_name not in self.LIST_SVG_REMOTE:
        remove(join(self.PATH_SVG, svg_name))
      elif self.LOCAL_CHECK[svg_name] != self.REMOTE_CHECK[svg_name]:
        self.download_svg(svg_name)

  # Verifica si es que existe, so descarga el archivo
  def check_exists(self):
    for nombre in self.REMOTE_CHECK:
      if nombre not in self.LOCAL_CHECK:
        self.download_svg(nombre)

  # Descarga el archivo desde el repo
  def download_svg(self, name):
    url = join(self.URL_REPO_SVG, name)
    descargado = get(url)
    open(join(self.PATH_SVG, name), 'wb').write(descargado.content)