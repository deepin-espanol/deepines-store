import sys
import os
# Modulos de pyqt5
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QSystemTrayIcon,
                            QAction, QMenu, QGraphicsBlurEffect)
from PyQt5.QtGui import QPixmap, QIcon
# Modulos para el scraping
from bs4 import BeautifulSoup
import urllib.request
import requests
# Guis o modulos locales
from maing import Ui_MainWindow
from cardg import Ui_Frame
# QThread para instalar en segundo plano
from install_thread import External
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

    def start_message(self, application: str):
        self.trayIcon.showMessage("Comenzando la instalación",
                        "Se ha comenzado la instalación de {}, en un "
                        "momento estara lista.".format(application), 1, 10000)

    def finish_message(self, application: str):
        self.trayIcon.showMessage("Instalación completada",
                        "Se ha instalado {} correctamente, "
                        "esperamos que disfrute la aplicación.".format(application), 1, 10000)

    def error_message(self, application: str):
        self.trayIcon.showMessage("Ha ocurrido un error",
                    "No se ha podido instalar {} correctamente, "
                    "vuelva a intentarlo.".format(application), 1, 10000)


    #				END SYSTRAY					   #
    ################################################

    ################################################
    #                Lista de apps                 #

    #           Obtener lista de apps              #
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

    #           Listar aplicaciones              #
    def Listar_Apps(self, lista):

        y = 0
        x = 0
        for key in lista:
            if y % 3 == 0 and y != 0:
                y = 0
                x += 1
            y += 1
            carta = Card(lista[key][0], lista[key][1], lista[key][2])
            self.ui.gridLayout.addWidget(carta, x, y, 1, 1)

    #                /Lista de apps                #
    ################################################

    def install_thread(self, app:str):
        self.obj = External(app)
        self.thread = QThread()
        self.obj.start.connect(self.start_message)
        self.obj.finish.connect(self.finish_message)
        self.obj.error.connect(self.error_message)
        self.obj.moveToThread(self.thread)
        self.thread.started.connect(self.obj.run)
        #self.thread.finished.connect(self.thread.quit)
        self.thread.start()



################################################
#           Card para la aplicacion            #

class Card(QFrame):
    def __init__(self, titulo: str, descripcion: str, version: str):
        super(Card, self).__init__()
        self.cd = Ui_Frame()
        self.cd.setupUi(self)
        self.app = titulo
        # Establecemos los atributos de la app
        self.cd.boton_ver_card.setToolTip(version)
        self.cd.label_titulo_card.setText(titulo)
        self.cd.image_card.setToolTip(descripcion)
        # Consultamos si existe el grafico de la app
        if not os.path.exists('./resources/apps/' + titulo  + '.svg'):
            url = './resources/apps/no-img.svg'
        else:
            url = './resources/apps/' + titulo  + '.svg'
        # Establecemos la imagen
        pixmap = QPixmap(url)
        self.cd.image_card.setPixmap(pixmap)
        # Conectamos a la funcion para instalar
        self.cd.boton_ver_card.clicked.connect(Ventana.install_thread(Ventana(), titulo))
        #self.cd.boton_ver_card.clicked.connect(lambda: Ventana.error_message(Ventana(), titulo))

#           /Card para la aplicacion           #
################################################


if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = Ventana()
  win.show()
  sys.exit(app.exec_())
