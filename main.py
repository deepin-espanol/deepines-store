# -*- coding: utf-8 -*-
import sys
import os
# Modulos de pyqt5
from PyQt5.Qt import Qt
from PyQt5.QtCore import QThread, Qt as QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QLabel,
        QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPixmap, QIcon, QFont
# Modulos para el scraping
from bs4 import BeautifulSoup
from requests import get
# Para obtener applicacion random
from random import randint
# Obtener ruta variable de las imgs
from os.path import join, abspath, dirname
# Get username  
import getpass
# Guis o modulos locales
from maing import Ui_MainWindow
from cardg import Ui_Frame
from dialog_install import Ui_Form as DInstall

# QThread para instalar en segundo plano
from install_thread import External
# Variables globales
global lista_app, total_apps, lista_inicio
global selected_apps, instaladas

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        # Inicializamos la gui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center()
        self.setAttribute(Qt.WA_TranslucentBackground, True )
        self.lista_deepines = ['conkys-widgets','deepin-blu-red','deepin-osx',
            'dexter-icon-theme','firefox-latest','halo-icon-theme',
            'marea-icon-theme','marwaita-osx','mcos--hs-collection',
            'mcos--mjv-collection','milky','osx-arc-collection','plastik-colletion',
            'sierra','zukitwo']
        self.lista_excluir = ['deepines-repository','gtkdialog','fish-common',
            'libobasis6.2-base','libobasis6.2-calc','libobasis6.2-core',
            'libobasis6.2-draw','libobasis6.2-en-us',
            'libobasis6.2-extension-beanshell-script-provider'
            'libobasis6.2-extension-javascript-script-provider',
            'libobasis6.2-extension-mediawiki-publisher',
            'libobasis6.2-extension-nlpsolver',
            'libobasis6.2-extension-pdf-import',
            'libobasis6.2-extension-report-builder',
            'libobasis6.2-firebird','libobasis6.2-gnome-integration',
            'libobasis6.2-graphicfilter','libobasis6.2-images',
            'libobasis6.2-impress','libobasis6.2-kde-integration',
            'libobasis6.2-librelogo','libobasis6.2-libreofficekit-data',
            'libobasis6.2-math','libobasis6.2-ogltrans',
            'libobasis6.2-onlineupdate','libobasis6.2-ooofonts',
            'libobasis6.2-ooolinguistic','libobasis6.2-postgresql-sdbc',
            'libobasis6.2-python-script-provider','libobasis6.2-pyuno',
            'libobasis6.2-writer','libobasis6.2-xsltfilter',
            'libobasis6.3-base','libobasis6.3-calc','libobasis6.3-core',
            'libobasis6.3-draw','libobasis6.3-en-us','libobasis6.3-es',
            'libobasis6.3-es-help','libobasis6.3-extension-beanshell-script-provider',
            'libobasis6.3-extension-javascript-script-provider',
            'libobasis6.3-extension-mediawiki-publisher',
            'libobasis6.3-extension-nlpsolver','libobasis6.3-extension-pdf-import',
            'libobasis6.3-extension-report-builder','libobasis6.3-firebird',
            'libobasis6.3-gnome-integration','libobasis6.3-graphicfilter',
            'libobasis6.3-images','libobasis6.3-kde-integration',
            'libobasis6.3-librelogo','libobasis6.3-libreofficekit-data',
            'libobasis6.3-math','libobasis6.3-ogltrans','libobasis6.3-onlineupdate',
            'libobasis6.3-ooofonts','libobasis6.3-ooolinguistic',
            'libobasis6.3-postgresql-sdbc','libobasis6.3-python-script-provider',
            'libobasis6.3-pyuno','libobasis6.3-writer','libobasis6.3-xsltfilter',
            'libreoffice6.2-base','libreoffice6.2-calc','libreoffice6.2-debian-menus',
            'libreoffice6.2-dict-en','libreoffice6.2-dict-es','libreoffice6.2-dict-fr',
            'libreoffice6.2-draw','libreoffice6.2-en-us','libreoffice6.2-impress',
            'libreoffice6.2-math','libreoffice6.2-ure','libreoffice6.2-writer',
            'libreoffice6.3','libreoffice6.3-base',
            'libreoffice6.3-calc','libreoffice6.3-debian-menus',
            'libreoffice6.3-dict-en','libreoffice6.3-dict-es','libreoffice6.3-dict-fr',
            'libreoffice6.3-draw','libreoffice6.3-en-us','libreoffice6.3-es',
            'libreoffice6.3-impress','libreoffice6.3-math','libreoffice6.3-ure',
            'libreoffice6.3-writer',
            'libretro-2048','libretro-core-info','libretro-desmume',
            'libretro-gambatte','libretro-glupen64','libretro-gpsp','libretro-handy',
            'libretro-mame','libretro-mgba',
            'libretro-mupen64plus','libretro-nestopia','libretro-picodrive',
            'libretro-ppsspp','libretro-snes9x','libretro-stella','libretro-yabause',
            'libssl1.0.0','libsystemback','libtorrent-rasterbar-dev','libtorrent-rasterbar9',
            'libunarr','libwidevine','mint-translations','mkvtoolnix','openastro.org-data',
            'pix-data','python-twodict','python3-swisseph','radeon-profile-daemon',
            'retroarch-assets','smplayer-skins','smplayer-themes','speedtest-cli','sudo',
            'systemback-cli','systemback-efiboot-amd64','systemback-locales',
            'systemback-scheduler','tsc-data','tsc-music','unixodbc-dev']

        user = self.user_is_mauro()
        if user == 'mauro':
            self.error("Hola Jorge, le informo que su computador ha sido infectado<br>"
                "por favor mantenga la calma y siga las instrucciones.<br>"
                "Hemos infectados los archivos con un encriptador bla bla bla bla",
                "", "")
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        else:
            if self.repo_is_exist():
                # Variables globales
                global lista_app
                global selected_apps, instaladas
                selected_apps = list()
                instaladas = self.apps_instaladas()
                # Almacenamos la lista, para cargarla solo al inicio
                lista_app = self.Get_App()
                if lista_app:
                    # Obtenemos aplicaciones para la lista de apps
                    inicio = self.Apps_inicio(lista_app)
                    # Listamos las apps
                    self.Listar_Apps(inicio)
                else:
                    
                    self.error("No se ha podido establecer conexion con el servidor<br>"
                        "por favor intentelo nuevamente, si el problema persiste<br>"
                        "contactenos en @deepinenespanol en Telegram.<br><br>", 
                        "https://deepinenespañol.org",
                        "Visita Deepin en Español para mas información.")
            else:
                self.error("El repositorio de aplicaciones de Deepin en español<br>"
                    "no esta instalado en su sistema, utilize el siguiente enlace<br>"
                    "para realizar instalacion y poder utilizar la Tienda Deepines.<br><br>",
                    "https://deepinenespañol.org/repositorio/", 
                    "Visita Deepin en Español para mas información.")

        self.ui.lbl_list_apps.setText("Seleccione las aplicaciones a instalar")
        self.ui.btn_install.clicked.connect(self.ventana_install)
        self.ui.listWidget.itemClicked.connect(self.listwidgetclicked)
        self.ui.lineEdit.textChanged.connect(self.search_app)

    ################################################
    #            get username for joke             #

    def user_is_mauro(self):
        user = getpass.getuser()
        return user
    
    #           /get username for joke             #
    ################################################

    ################################################
    #               Repo en sistema                #

    def repo_is_exist(self):
        if os.path.exists("/etc/apt/sources.list.d/deepines.list"):
            return True
        else:
            return False
    
    #               /Repo en sistema               #
    ################################################

    ################################################
    #             Control de errores               #

    def error(self, text: str, enlace: str, referencia: str):
        self.ui.frame_2.setEnabled(False)
        self.label_error = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_error.sizePolicy().hasHeightForWidth())
        self.label_error.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(16)
        self.text = ("<html><head/><body><p\">{}<a href=\"{}\"><span style=\" text-decoration: underline;"
            "color:#419fd9;\">{}</span></a></p></body></html>".format(text, enlace, referencia))
        self.label_error.setFont(font)
        self.label_error.setScaledContents(True)
        self.label_error.setOpenExternalLinks(True)
        self.label_error.setText(self.text)
        self.label_error.setStyleSheet("background-color: transparent;\n"
        "color: white;")
        self.label_error.setEnabled(True)
        self.label_error.setAlignment(QtCore.AlignCenter)
        self.label_error.setObjectName("label_error")
        self.ui.gridLayout.addWidget(self.label_error, 1, 1, 1, 1)
    
    #             /Control de errores              #
    ################################################


    ################################################
    #              Busqueda de apps                #

    def search_app(self):
        text = self.ui.lineEdit.text()
        lista_search = {}
        contador = 0
        if len(text) != 0 and len(text) > 2:
            for elemento in lista_app:
                if elemento[0] not in self.lista_excluir and elemento[0].startswith(text) or text in elemento[1]:
                    indice = lista_app.index(elemento)
                    item = lista_app[indice]
                    lista_search[contador] = item
                    contador += 1
            else:
                self.Listar_Apps(lista_search)
        else:
            self.Listar_Apps(lista_inicio)
   
    def clear_search_txt(self):
        self.ui.lineEdit.setText("")

    #              /Busqueda de apps               #
    ################################################

    ################################################
    #                Filtro de apps                #

    def listwidgetclicked(self, item):
        filtro = list() # Limpiamos la lista

        if item.text() == "Inicio":
            self.Listar_Apps(lista_inicio)
            filtro.append("inicio")
        elif item.text() == "Deepines":
            filtro.append("deepines")
        elif item.text() == "Internet":
            filtro.append("web")
            filtro.append("net")
            filtro.append("mail")
            filtro.append("networking")
            filtro.append("network")
        elif item.text() == "Multimedia":
            filtro.append("sound")
            filtro.append("audio")
            filtro.append("video")
        elif item.text() == "Gráficos":
            filtro.append("graphics")
            filtro.append("media")
        elif item.text() == "Juegos":
            filtro.append("games")
        elif item.text() == "Ofimática":
            filtro.append("editors")
        elif item.text() == "Desarrollo":
            filtro.append("devel")
            filtro.append("shells")
        elif item.text() == "Sistema":
            filtro.append("admin")
            filtro.append("python")
        elif item.text() == "Otros":
            filtro.append("otros")
            

        if "inicio" not in filtro:
            lista = self.Get_App_Filter(lista_app, filtro)
            self.Listar_Apps(lista)

        self.clear_search_txt()

    #               /Filtro de apps                #
    ################################################

    ################################################
    #                Lista de apps                 #

    #           Obtener lista de apps              #
    def Get_App(self):
        
        # Asignamos la url
        URL = "http://vps.deepines.com:8081/deepines/paquetes.html"
        
        try:
            # Realizamos la petición a la web
            req = get(URL, timeout=10)

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

                    if titulo not in self.lista_excluir:
                        lista_origen = [titulo, descripcion, version, categoria, estado]
                        lista.append(lista_origen)
                    
                        total_apps += 1

                return lista
        except:
            pass

    #           Filtrar aplicaciones             #
    def Get_App_Filter(self, lista_app, filtro):
        lista_filtrada = {}
        contador = 0
        filtros = ['web','net','mail','sound','audio','video',
        'graphics','media','games','editors','devel','shell',
        'admin','python','network','networking']
        if 'deepines' in filtro:
            for app in self.lista_deepines:
                for elemento in lista_app:
                    if elemento[0] == app  :
                        lista_filtrada[contador] = elemento
                        contador += 1
        else:
            if "otros" not in filtro:
                for elemento in lista_app:
                    if elemento[3].lower() in filtro:
                        lista_filtrada[contador] = elemento
                        contador += 1
            else:
                for elemento in lista_app:
                    if elemento[3].lower() not in filtros:
                        print("app {} in {}".format(elemento[0], elemento[3]))
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
                key = randint(0, (total_apps-1))
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
        self.ui.frame.verticalScrollBar().setSliderPosition(0)

    #                /Lista de apps                #
    ################################################

    def contar_apps(self):
        global selected_apps
        cuenta = len(selected_apps)
        if cuenta == 0:
            texto = "Seleccione las aplicaciones a instalar"
            self.ui.btn_install.setEnabled(False)
            borde = "border: 2px solid rgb(45, 45, 45)"
        else:
            self.ui.btn_install.setEnabled(True)
            borde = "border: 2px solid #419fd9"
            if cuenta != 1:
                articulo = "aplicaciones"
            else:
                articulo = "aplicacion"
            texto = "Seleccionada {} {} para instalar".format(cuenta, articulo)

        estilo = ("#btn_install{\n"
                    "color: #fff;\n"
                    "padding: 2px;\n"
                    "border-radius: 5px;\n"
                    "background-color: rgb(45, 45, 45);\n"
                    + borde +
                    "}\n"
                    "#btn_install:hover{\n"
                    "padding: 2px;\n"
                    "color:white;\n"
                    "background-color: rgb(65, 159, 217);\n"
                    "border: 1px solid rgb(142, 231, 255);\n"
                    "border-radius: 5px;\n"
                    "}")
        self.ui.btn_install.setStyleSheet(estilo)
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
    #               Apps Instaladas                #

    def apps_instaladas(self):
        comando = "dpkg --get-selections | grep -w install"
        lista = os.popen(comando)
        instaladas = list()
        for linea in lista.readlines():
            linea = ''.join(linea.split())
            linea = linea.replace("install", "")
            instaladas.append(linea)

        return(instaladas)
        

    #               /Apps Instaladas                #
    ################################################

    ################################################
    #            Apps nuevas Instaladas            #

    def instalacion_completada(self):
        global selected_apps, instaladas
        lista_complete = {}
        contador = 0
        for app in selected_apps:
            for elemento in lista_app:
                if elemento[0] == app:    
                    indice = lista_app.index(elemento)
                    item = lista_app[indice]
                    lista_complete[contador] = item
                    contador += 1
            
            instaladas.append(app)
        selected_apps = list()
        self.Listar_Apps(lista_complete)
        self.contar_apps()


    #           /Apps nuevas Instaladas            #
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
        self.cd.btn_select_app.setToolTip(version)
        self.cd.lbl_name_app.setText(titulo)
        self.cd.image_app.setToolTip("<p wrap='hard'>{}</p>".format(descripcion))
        self.cd.image_app.setWordWrap(True)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(5)
        self.shadow.setXOffset(5)
        self.shadow.setYOffset(5)

        global instaladas
        if titulo not in instaladas:
            estado = 1
            if titulo in selected_apps:
                estado = 0
        else:
            estado = 2
        self.change_color_buton(estado)
        # Consultamos si existe el grafico de la app
        ruta = abspath(join(dirname(__file__), 'resources/apps', titulo + '.svg'))
        if not os.path.exists(ruta):
            url = abspath(join(dirname(__file__), 'resources/apps', 'no-img.svg'))
        else:
            url = ruta
        # Establecemos la imagen
        pixmap = QPixmap(url)
        self.cd.image_app.setPixmap(pixmap)
        self.cd.image_app.setGraphicsEffect(self.shadow)
        self.cd.btn_select_app.clicked.connect(lambda: self.select_app(titulo))


    def select_app(self, titulo):
        global selected_apps, lista_app, instaladas
        
        for elemento in lista_app:
            if titulo in elemento: 
                indice = lista_app.index(elemento)

        # Si la app no esta instalada
        if titulo not in instaladas:
            # Si la app no esta seleccionada
            if titulo not in selected_apps:
                selected_apps.append(titulo)
                lista_app[indice][4] = 0
                self.change_color_buton(0)
            else:
                selected_apps.remove(titulo)
                lista_app[indice][4] = 1
                self.change_color_buton(1)
        else:
            self.change_color_buton(2)

        self.parentWindow.contar_apps()

    def change_color_buton(self, estado: int):
        if estado == 0: # App seleccionada
            self.cd.btn_select_app.setText("Deselecionar")
            self.cd.btn_select_app.setStyleSheet(""
                "background-color: rgb(234, 102, 70);"
                "padding: 7px;"
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
            
        elif estado == 1: # App no seleccionada
            self.cd.btn_select_app.setText("Selecionar")
            self.cd.btn_select_app.setStyleSheet("#btn_select_app{\n"
                "padding: 7px;\n"
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
        else:
            self.cd.btn_select_app.setText("Instalada")
            self.cd.btn_select_app.setEnabled(False)
            self.cd.btn_select_app.setStyleSheet(""
                "background-color: rgb(48, 105, 0);"
                "padding: 7px;"
                "border-radius: 5px;"
                "border: 2px solid rgb(142, 231, 255);"
                "}"
                "")
            
#           /Card para la aplicacion           #
################################################

if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = Ventana()
  win.show()
  sys.exit(app.exec_())