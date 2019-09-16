import sys
import os
# Modulos de pyqt5
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QSystemTrayIcon,
                            QAction, QMenu, QGraphicsBlurEffect)
from PyQt5.QtGui import QPixmap, QIcon
# Modulos para el scraping
from bs4 import BeautifulSoup
import urllib.request
import requests
# Guis o modulos locales
from maing import Ui_MainWindow
from cardg import Ui_Frame as Card
# Variables globales
global lista_app, total_apps, lista_inicio

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        # Inicializamos la gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Creamos el icono de sistema
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()
        # Variables globales
        global lista_app
        # Almacenamos la lista, para cargarla solo al inicio
        lista_app = self.Get_App()
        self.Listar_Apps(lista_app)
        # Probamos el mensaje
        #self.messages("Bienvenido", "Cargando las aplicaciones", 1)
        #self.trayIcon.showMessage("Bienvenido", "Cargando las aplicaciones", 1, 10000)

    ################################################
    #				SYSTRAY 					   #
    def createActions(self):
            self.minimizeAction = QAction("Minimizar", self, triggered=self.hide)
            self.maximizeAction = QAction("Maximizar", self,
                    triggered=self.showMaximized)
            self.restoreAction = QAction("Restaurar", self,
                    triggered=self.showNormal)
            self.quitAction = QAction("Salir", self,
                    triggered=QApplication.instance().quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.maximizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setToolTip("DeepineStore")
        self.trayIcon.setIcon(QIcon('./resources/deepines_logo_beta.svg'))
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def messages(self, titulo: str, texto: str, estado: int):
        self.trayIcon.showMessage(titulo, texto, estado, 10000)

    #				END SYSTRAY					   #
    ################################################

    ################################################
    #          Obtener lista de apps               #

    def Get_App(self):
        # Asignamos la url
        URL = "http://deepin.mooo.com:8082/deepines/paquetes.html"

        # Realizamos la petición a la web
        req = requests.get(URL)

        # Comprobamos que la petición nos devuelve un Status Code = 200
        status_code = req.status_code
        if status_code == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos todos los divs donde están las entradas
            entradas = html.find_all('tr')
            
            lista = {}
            global total_apps
            total_apps = 0
            # Recorremos todas las entradas para extraer el título, autor y fecha
            for i, entrada in enumerate(entradas):
                # Con el método "getText()" no nos devuelve el HTML
                titulo = entrada.find('td', {'class': 'package'}).getText()
                descripcion = entrada.find('td', {'class': 'description'}).getText()
                version = entrada.find('td', {'class': 'version'}).getText()
                categoria = entrada.find('td', {'class': 'section'}).getText()
                lista[i] = (titulo, descripcion, version, categoria)
                
                total_apps += 1

            return lista
        else:
            print("Status Code %d" % status_code)

    def Listar_Apps(self, lista):

        y = 0
        x = 0
        for key in lista:
            if y % 3 == 0 and y != 0:
                y = 0
                x += 1
            y += 1
            carta = Card(lista[key][0], lista[key][1], lista[key][2])
            print(carta)
            self.ui.gridLayout.addWidget(carta, x, y, 1, 1)



if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = Ventana()
  win.show()
  sys.exit(app.exec_())
