#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Creador en Agosto 2019
@Autor: Sebastian Trujillo
@Contacto: t.me/sebtrujillo
@Descripcion: App store para el repositorio de deepines 
'''

import sys, os #, subprocess
from PyQt5.QtCore import QThread
# Para obtener applicacion random
import random
# Graficos de PyQt
from PyQt5 import Qt
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QSystemTrayIcon,
                            QAction, QMenu, QGraphicsBlurEffect)
from PyQt5.QtGui import QPixmap, QIcon

# Modulos para el scraping
from bs4 import BeautifulSoup
import urllib.request
import requests

# Guis
from maing import Ui_MainWindow
from cardg import Ui_Frame
# Para la Instalacion
import install


global lista_app, total_apps, lista_inicio

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Icono de sistema
        self.createActions()
        self.createTrayIcon()
        self.trayIcon.show()
        self.trayIcon.showMessage("Inicio", "Bienvenido a Store", 1, 10000)
        # Variable global
        global lista_app
        lista_app = self.Get_App()
        inicio = self.Apps_inicio(lista_app)
        self.Listar_Apps(inicio)
        self.setAttribute(Qt.Qt.WA_TranslucentBackground, True )
        self.setAttribute(Qt.Qt.WA_NoSystemBackground, False)
        #self.setStyleSheet("background-color: rgba(16, 16, 16, 100);") 
        
        #self.ui.frame.setGraphicsEffect(QGraphicsBlurEffect())
        #self.shadow = QGraphicsBlurEffect(self) #Efecto blur
        #self.shadow.setBlurRadius(25)
        #self.shadow.BlurHint(QGraphicsBlurEffect.PerformanceHint)
        #self.setGraphicsEffect(self.shadow)

        self.ui.listWidget.itemClicked.connect(self.listwidgetclicked)
        

    def listwidgetclicked(self, item):
        for i in range(self.ui.gridLayout.count()):
            self.ui.gridLayout.itemAt(i).widget().deleteLater()

        if item.text() == "Inicio":
            self.Listar_Apps(lista_inicio)
            filtro = "inicio"
        elif item.text() == "Internet":
            filtro = "web"
        elif item.text() == "Mensajeria":
            filtro = "net"
        elif item.text() == "Música":
            filtro = "sound"
        elif item.text() == "Gráficos":
            filtro = "graphics"
        elif item.text() == "Video":
            filtro = "video"
        elif item.text() == "Juegos":
            filtro = "games"
        elif item.text() == "Ofimática":
            filtro = "editors"
        #elif item.text() == "Lectura":
        #   filtro = "editors"
        elif item.text() == "Desarrollo":
            filtro = "devel"
        elif item.text() == "Sistema":
            filtro = "admin"
        elif item.text() == "Otros":
            filtro = "other"
        else:
            filtro = "0"
        
        if filtro != "inicio":
            lista = self.Get_App_Filter(lista_app, filtro)
            self.Listar_Apps(lista)

    def Get_App(self):

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

    def Get_App_Filter(self, lista_app, filtro):
        lista_filtrada = {}
        contador = 0
        for key in lista_app:
            if filtro == lista_app[key][3]:
                lista_filtrada[contador] = lista_app[key]
            elif lista_app[key][3] == "misc" and filtro == "other":
                lista_filtrada[contador] = lista_app[key]
            elif lista_app[key][3] == "utils" and filtro == "other":
                lista_filtrada[contador] = lista_app[key]
            contador += 1

        return lista_filtrada
        

    def Apps_inicio(self, lista_app):
        global total_apps, lista_inicio
        lista_inicio = {}
        for z in range(12):
            key = random.randint(0, (total_apps-1))
            lista_inicio[z] = lista_app[key]
        return lista_inicio            

    def Listar_Apps(self, lista):

        y = 0
        x = 0
        for key in lista:
            if y % 3 == 0 and y != 0:
                y = 0
                x += 1
            y += 1
            # Estas lineas las use para cuando tenia la funcion install_thread
            # Dentro de la clase Ventana
            #self.card = Card(lista[key][0], lista[key][1], lista[key][2])
            #self.card.cd.boton_ver_card.clicked.connect(lambda: self.install_thread(lista[key][0]))
            self.ui.gridLayout.addWidget(Card(lista[key][0], lista[key][1], lista[key][2]), x, y, 1, 1)

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

    def showMessage(self, estado: int, app: str):
        if estado == 1:
            titulo = "Comenzando instalacion"
            texto = "Instalando {}".format(app)
        elif estado == 2:
            titulo = "Instalacion Completada"
            texto = "Se ha instalado correctamente {}".format(app)
        else:
            titulo = "Algo a fallado"
            texto = "No se a podido instalar {}".format(app)
        # Message(Titulo, Texto, Icono, Duracion[ms])
        # Icon{0:'NoIcon', 1:'Information', 2:'Warning', 3:'Critical'}
        self.trayIcon.showMessage(titulo,texto,1,10000)

def install_thread(estado: int, aplicacion:str):
    # Si esta funcion esta dentro de la clase Ventana
    # No me toma el nombre de la app que deberia
    # Pero si manda el mensaje de notificacion
    obj = install.External(aplicacion)
    thread = QThread()
    obj.intReady.connect(Ventana.showMessage(estado, aplicacion))
    obj.moveToThread(thread)
    obj.finished.connect(thread.quit)
    thread.started.connect(obj.run)
    #self.thread.finished.connect(self.thread.quit())
    thread.start()

class Card(QFrame):
    def __init__(self, titulo: str, descripcion: str, version: str):
        super(Card, self).__init__()
        self.cd = Ui_Frame()
        self.cd.setupUi(self)
        self.cd.boton_ver_card.setToolTip(version)
        self.cd.label_titulo_card.setText(titulo)
        self.cd.image_card.setToolTip(descripcion)
        
        if not os.path.exists('./resources/apps/' + titulo  + '.svg'):
            url = './resources/apps/no-img.svg'
        else:
            url = './resources/apps/' + titulo  + '.svg'

        pixmap = QPixmap(url)
        self.cd.image_card.setPixmap(pixmap)

        self.cd.boton_ver_card.clicked.connect(lambda: install_thread(1, titulo))

        
if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = Ventana()
  win.show()
  sys.exit(app.exec_())
