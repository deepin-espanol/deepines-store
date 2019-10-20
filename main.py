import sys
import os
# Modulos de pyqt5
from PyQt5 import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QSystemTrayIcon,
                            QAction, QMenu, QGraphicsBlurEffect, QApplication)
from PyQt5.QtGui import QPixmap, QIcon
# Modulos para el scraping
from bs4 import BeautifulSoup
import urllib.request
import requests
# Para obtener applicacion random
import random
# Guis o modulos locales
from maing import Ui_MainWindow
from cardg import Ui_Frame
from dialog_install import Ui_Form as DInstall
# QThread para instalar en segundo plano
from install_thread import External
# Variables globales
global lista_app, total_apps, lista_inicio
global selected_apps

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        # Inicializamos la gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center()
        self.setAttribute(Qt.Qt.WA_TranslucentBackground, True )
        # Variables globales
        global lista_app
        global selected_apps
        selected_apps = list()
        # Almacenamos la lista, para cargarla solo al inicio
        lista_app = self.Get_App()
        # Obtenemos aplicaciones para la lista de apps
        inicio = self.Apps_inicio(lista_app)
        # Listamos las apps
        self.Listar_Apps(inicio)

        self.ui.lbl_list_apps.setText("Seleccione las aplicaciones a instalar")
        self.ui.btn_install.clicked.connect(self.ventana_install)
        self.ui.listWidget.itemClicked.connect(self.listwidgetclicked)
        self.ui.lineEdit.textChanged.connect(self.search_app)


    ################################################
    #              Busqueda de apps                #

    def search_app(self):
        text = self.ui.lineEdit.text()
        lista_search = {}
        contador = 0
        if len(text) != 0 and len(text) > 2:
            for elemento in lista_app:
                if elemento[0].startswith(text):
                    indice = lista_app.index(elemento)
                    item = lista_app[indice]
                    lista_search[contador] = item
                    contador += 1
            else:
                self.Listar_Apps(lista_search)
        else:
            self.Listar_Apps(lista_inicio)
    
    #              /Busqueda de apps               #
    ################################################

    ################################################
    #                Filtro de apps                #

    def listwidgetclicked(self, item):
        filtro = list() # Limpiamos la lista

        if item.text() == "Inicio":
            self.Listar_Apps(lista_inicio)
            filtro.append("inicio")
        elif item.text() == "Internet":
            filtro.append("web")
        elif item.text() == "Mensajeria":
            filtro.append("net")
            filtro.append("mail")
        elif item.text() == "Música":
            filtro.append("sound")
            filtro.append("audio")
        elif item.text() == "Gráficos":
            filtro.append("graphics")
            filtro.append("Media")
        elif item.text() == "Video":
            filtro.append("video")
        elif item.text() == "Juegos":
            filtro.append("games")
        elif item.text() == "Ofimática":
            filtro.append("editors")
        #elif item.text() == "Lectura":
        #   filtro = "editors"
        elif item.text() == "Desarrollo":
            filtro.append("devel")
            filtro.append("shells")
        elif item.text() == "Sistema":
            filtro.append("admin")
            filtro.append("python")
        elif item.text() == "Otros":
            filtro.append("base")
            filtro.append("default")
            filtro.append("fonts")
            filtro.append("gnome")
            filtro.append("interpreters")
            filtro.append("libs")
            filtro.append("misc")
            filtro.append("non-free")
            filtro.append("other")
            filtro.append("science")
            filtro.append("Tools")
            filtro.append("utils")
            filtro.append("universe")
            filtro.append("x11")

        if "inicio" not in filtro:
            lista = self.Get_App_Filter(lista_app, filtro)
            self.Listar_Apps(lista)

    #               /Filtro de apps                #
    ################################################

    ################################################
    #                Lista de apps                 #

    #           Obtener lista de apps              #
    def Get_App(self):
        lista_excluir = ['libobasis6.2-base','libobasis6.2-calc','libobasis6.2-core',
        'libobasis6.2-draw','libobasis6.2-en-us','libobasis6.2-extension-beanshell-script-provider',
        'libobasis6.2-extension-javascript-script-provider','libobasis6.2-extension-mediawiki-publisher',
        'libobasis6.2-extension-nlpsolver','libobasis6.2-extension-pdf-import','libobasis6.2-extension-report-builder',
        'libobasis6.2-firebird','libobasis6.2-gnome-integration','libobasis6.2-graphicfilter',
        'libobasis6.2-images','libobasis6.2-impress','libobasis6.2-kde-integration',
        'libobasis6.2-librelogo','libobasis6.2-libreofficekit-data','libobasis6.2-math','libobasis6.2-ogltrans',
        'libobasis6.2-onlineupdate','libobasis6.2-ooofonts','libobasis6.2-ooolinguistic','libobasis6.2-postgresql-sdbc',
        'libobasis6.2-python-script-provider','libobasis6.2-pyuno','libobasis6.2-writer','libobasis6.2-xsltfilter',
        'libreoffice6.2','libreoffice6.2-base','libreoffice6.2-debian-menus','libreoffice6.2-dict-en',
        'libreoffice6.2-dict-es','libreoffice6.2-dict-fr','libreoffice6.2-draw','libreoffice6.2-en-us',
        'libreoffice6.2-impress','libreoffice6.2-math','libreoffice6.2-ure','libreoffice6.2-writer',
        'libreoffice6.2-calc','radeon-profile-daemon','gtkdialog','libssl1.0.0','libsystemback',
        'systemback-cli','systemback-efiboot-amd64','systemback-locales','systemback-scheduler']
        # Asignamos la url
        #URL = "http://deepin.mooo.com:8082/deepines/paquetes.html"
        URL = "http://vps.deepines.com:8080/deepines/paquetes.html"

        # Realizamos la petición a la web
        req = requests.get(URL)

        # Comprobamos que la petición nos devuelve un Status Code = 200
        status_code = req.status_code
        if status_code == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")

            # Obtenemos todos los divs donde están las entradas
            entradas = html.find_all('tr')
            
            lista = list()
            global total_apps
            total_apps = 0
            # Recorremos todas las entradas para extraer el título, autor y fecha
            for i, entrada in enumerate(entradas):
                # Con el método "getText()" no nos devuelve el HTML
                titulo = entrada.find('td', {'class': 'package'}).getText()
                descripcion = entrada.find('td', {'class': 'description'}).getText()
                version = entrada.find('td', {'class': 'version'}).getText()
                categoria = entrada.find('td', {'class': 'section'}).getText()
                estado = 1
                if titulo not in lista_excluir:
                    lista_origen = [titulo, descripcion, version, categoria, estado]
                    lista.append(lista_origen)
                
                    total_apps += 1
            return lista
        else:
            print("Status Code %d" % status_code)

    #           Filtrar aplicaciones             #
    def Get_App_Filter(self, lista_app, filtro):
        lista_filtrada = {}
        contador = 0
        for elemento in lista_app:
            if elemento[3] in filtro:
                lista_filtrada[contador] = elemento

            contador += 1

        return lista_filtrada
        
    #           Aplicaciones Inicio              #
    def Apps_inicio(self, lista_app):
        global total_apps, lista_inicio
        lista_inicio = {}
        lista_key = []
        contador = True
        while contador:
            if len(lista_key) == 12:
                contador = False
            else:
                key = random.randint(0, (total_apps-1))
                if key not in lista_key:
                    lista_key.append(key)

        contador = 0
        for key in lista_key:
            lista_inicio[contador] = lista_app[key]
            contador += 1

        return lista_inicio   

    #           Listar aplicaciones              #
    def Listar_Apps(self, lista):
        for i in range(self.ui.gridLayout.count()):
            # Eliminamos los items de la grilla
            self.ui.gridLayout.itemAt(i).widget().deleteLater()

        y = 0 # Creamos la coordenada y
        x = 0 # Creamos la coordenada x 
        # Estas para establecer la ubicacion de la tarjetas en la grilla
        for key in lista: # Recorremos la lista con los elementos
            # Consultamos si ya tenemos tres tarjetas en y
            if y % 3 == 0 and y != 0:
                y = 0 # Reiniciamos y
                x += 1 # Agregamos otra columna
            y += 1 # agregamos 1 a la coordenada y
            # Creamos una instancia de la clase card
            carta = Card(lista[key][0], lista[key][1], lista[key][2], lista[key][4], self)
            # Agregamos dicha instancia a la grilla
            self.ui.gridLayout.addWidget(carta, x, y, 1, 1)

    #                /Lista de apps                #
    ################################################

    def contar_apps(self):
        global selected_apps
        cuenta = len(selected_apps)
        if cuenta == 0:
            texto = "Seleccione las aplicaciones a instalar"
            self.ui.btn_install.setEnabled(False)
        else:
            self.ui.btn_install.setEnabled(True)
            if cuenta != 1:
                articulo = "aplicaciones"
            else:
                articulo = "aplicacion"
            texto = "Seleccionada {} {} para instalar".format(cuenta, articulo)
        self.ui.lbl_list_apps.setText(texto)

    ################################################
    #                  Instalacion                 #

    def ventana_install(self):
        global selected_apps
        self.modal = DInstall(self, selected_apps)
        self.modal.show()

    #                 /Instalacion                 #
    ################################################

    ################################################
    #                   Centrar                    #
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    #                  /Centrar                    #
    ################################################

################################################
#           Card para la aplicacion            #

class Card(QFrame):
    def __init__(self, titulo: str, descripcion: str, version: str, estado: int, parent):
        super(Card, self).__init__()
        self.parentWindow = parent
        self.cd = Ui_Frame()
        self.cd.setupUi(self)
        # Establecemos los atributos de la app
        self.cd.btn_select_app.setText("Seleccionar")
        print(version)
        self.cd.btn_select_app.setToolTip(version)
        self.cd.lbl_name_app.setText(titulo)
        self.cd.image_app.setToolTip(descripcion)
        self.change_color_buton(estado)
        # Consultamos si existe el grafico de la app
        if not os.path.exists('./resources/apps/' + titulo  + '.svg'):
            url = './resources/apps/no-img.svg'
        else:
            url = './resources/apps/' + titulo  + '.svg'
        # Establecemos la imagen
        pixmap = QPixmap(url)
        self.cd.image_app.setPixmap(pixmap)

        # Conectamos a la funcion para instalar
        self.cd.btn_select_app.clicked.connect(lambda: self.select_app(titulo))

    def select_app(self, titulo):
        global selected_apps, lista_app
        
        for elemento in lista_app:
            if titulo in elemento: 
                indice = lista_app.index(elemento)
        
        if titulo not in selected_apps:
            selected_apps.append(titulo)
            self.change_color_buton(0)
            lista_app[indice][4] = 0

        else:
            selected_apps.remove(titulo)
            self.change_color_buton(1)
            lista_app[indice][4] = 1

        self.parentWindow.contar_apps()

    def change_color_buton(self, estado: int):
        if estado == 0: # App seleccionada
            self.cd.btn_select_app.setText("Deselecionar")
            self.cd.btn_select_app.setStyleSheet(""
                "background-color: rgb(234, 102, 70);"
                "padding: 7px;"
                "color: #000;"
                "border-radius: 5px;"
                "border: 2px solid rgb(142, 231, 255);"
                "}"
                "#btn_select_app:hover{"
                "padding: 7px;"
                "color:white;"
                "background-color: rgb(65, 159, 217);"
                "border-radius: 5px;"
                "}"
                "")
            
        else: # App no seleccionada
            self.cd.btn_select_app.setText("Selecionar")
            self.cd.btn_select_app.setStyleSheet("#btn_select_app{\n"
                "padding: 7px;\n"
                "color: white;\n"
                "border-radius: 5px;\n"
                "    background-color: rgb(45, 45, 45);\n"
                "}\n"
                "#btn_select_app:hover{\n"
                "border: 1px solid rgb(142, 231, 255);\n"
                "padding: 7px;\n"
                "color:white;\n"
                "background-color: rgb(65, 159, 217);\n"
                "border-radius: 5px;\n"
                "}")
            
#           /Card para la aplicacion           #
################################################

if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = Ventana()
  win.show()
  sys.exit(app.exec_())