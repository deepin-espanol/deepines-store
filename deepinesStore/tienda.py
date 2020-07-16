#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
# Modulos de pyqt5
from PyQt5.Qt import Qt
from PyQt5.QtCore import QSize, QPointF, QPoint, QEvent, Qt as QtCore,\
                         pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QLabel,
        QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem,
        QDesktopWidget, QWidget, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QCursor
# Modulos para el scraping
from bs4 import BeautifulSoup
from requests import get
# Para obtener applicacion random
from random import randint
# Obtener ruta variable de las imgs
from os.path import join, abspath, dirname
# Guis o modulos locales
from deepinesStore.maing import Ui_MainWindow
from deepinesStore.cardg import Ui_Frame
from deepinesStore.dialog_install import Ui_Form as DInstall
from deepinesStore.about import Dialog as DAbout

# Variables globales
global lista_app, total_apps, lista_inicio, lista_global, lista_selected
global selected_apps, instaladas, columnas, tamanio, repo, contador_selected

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        # Inicializamos la gui
        self.ui = Ui_MainWindow(width, height)
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True )
        self.lista_deepines = ['conkys-widgets','deepin-blu-red','deepin-osx',
            'dexter-icon-theme','firefox-latest','halo-icon-theme',
            'marea-icon-theme','marwaita-osx','mcos--hs-collection',
            'mcos--mjv-collection','milky','osx-arc-collection','plastik-colletion',
            'sierra','zukitwo']
        self.lista_excluir = ['brave-keyring','deepines-repository',
            'docker-ce-cli','gtkdialog','fish-common', 'libgutenprint2',
            'libobasis6.3-base','libobasis6.3-calc','libobasis6.3-core',
            'libobasis6.3-draw','libobasis6.3-en-us','libobasis6.3-es',
            'libobasis6.3-es-help','libobasis6.3-extension-beanshell-script-provider',
            'libobasis6.3-extension-javascript-script-provider',
            'libobasis6.3-extension-mediawiki-publisher',
            'libobasis6.3-extension-nlpsolver','libobasis6.3-extension-pdf-import',
            'libobasis6.3-extension-report-builder','libobasis6.3-firebird',
            'libobasis6.3-gnome-integration','libobasis6.3-graphicfilter',
            'libobasis6.3-images','libobasis6.3-impress','libobasis6.3-kde-integration',
            'libobasis6.3-librelogo','libobasis6.3-libreofficekit-data',
            'libobasis6.3-math','libobasis6.3-ogltrans','libobasis6.3-onlineupdate',
            'libobasis6.3-ooofonts','libobasis6.3-ooolinguistic',
            'libobasis6.3-postgresql-sdbc','libobasis6.3-python-script-provider',
            'libobasis6.3-pyuno','libobasis6.3-writer','libobasis6.3-xsltfilter',
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

        
        global lista_app, selected_apps, instaladas,\
         lista_global, repo, lista_selected, contador_selected
        repo = self.repo_is_exist()
        if repo:
            # Variables globales
            selected_apps = list()
            lista_selected = {}
            contador_selected = 0
            instaladas = self.apps_instaladas()
            # Almacenamos la lista, para cargarla solo al inicio
            lista_app = self.Get_App()
            if lista_app:
                # Obtenemos aplicaciones para la lista de apps
                self.Apps_inicio(lista_app)
                
            else:
                self.error("No ha podido establecer conexión con el servidor, <br>"
                    "por favor verifique su conexión de internet.<br>"
                    "Si el problema persiste, contáctenos vía Telegram <br>"
                    "en @deepinenespanol.<br><br>"
                    "<a href='#'>deepinenespañol.org | Copiar enlace</a><br>"
                    "Visite Deepin en Español para más información.",
                    "https://deepinenespañol.org")
        else:
            self.error("El repositorio Deepines no está instalado en su sistema,<br>"
                "Tienda Deepines necesita este repositorio para funcionar.<br>"
                "En el siguiente enlace encontrará las instrucciones para instalarlo.<br><br>"
                "<a href='#'>deepinenespañol.org/repositorio/ | Copiar enlace<a/><br>",
                "https://deepinenespañol.org/repositorio")

        self.ui.btn_install.setEnabled(False)
        self.ui.btn_install.clicked.connect(self.ventana_install)
        self.ui.lbl_list_apps.setText("Seleccione las aplicaciones a instalar")
        self.ui.lbl_list_apps.setEnabled(False)
        self.ui.lbl_list_apps.clicked.connect(lambda: self.Listar_Apps(lista_selected))
        self.ui.listWidget.itemClicked.connect(self.listwidgetclicked)
        self.ui.lineEdit.textChanged.connect(self.search_app)
        self.ui.label_2.clicked.connect(self.acerca_de)
        self.ui.btn_cerrar.clicked.connect(self.close)
        self.ui.btn_maximizar.clicked.connect(self.maximize)
        self.ui.btn_minimizar.clicked.connect(self.minimize)
        self.ui.widget_1.installEventFilter(self)
        self.ui.label.clicked.connect(self.acerca_de)
        shadow = QGraphicsDropShadowEffect(self,
          blurRadius=10,
          color=QColor(255,255,255),
          offset=QPointF(0, 0)
        )
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.ui.btn_install.setGraphicsEffect(shadow)
        
        self.center()


    
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

    def error(self, text: str, enlace: str):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 40, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.raccoon = QLabel(self)
        self.raccoon.setText("")
        self.raccoon.setMinimumSize(300, 300)
        self.raccoon.setMaximumSize(300, 300)
        self.raccoon.setObjectName("raccoon")
        self.raccoon.setStyleSheet("#raccoon{"
            "background-color: transparent;}")

        ruta = abspath(join(dirname(__file__), 'resources', 'raccoon.svg'))
        pixmap = QPixmap(ruta)
        self.raccoon.setPixmap(pixmap)
        self.horizontalLayout.addWidget(self.raccoon)
        self.ui.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        

        self.label_error = QLabelClickable(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_error.sizePolicy().hasHeightForWidth())
        self.label_error.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(16)
        self.text = ("""<html> <style type=text/css>
        a:link, a:visited, a:active {
            text-decoration:none;
            color: rgba(0, 192, 255, 255);
        }
        </style>
            <head/><body><p>"""
            + text +
            """</p></body></html>""")
        self.label_error.setFont(font)
        self.label_error.setScaledContents(True)
        self.label_error.setText(self.text)
        self.label_error.setStyleSheet("background-color: transparent;\n"
        "color: white;")
        self.label_error.setEnabled(True)
        self.label_error.setAlignment(QtCore.AlignCenter)
        self.label_error.setObjectName("label_error")
        self.label_error.clicked.connect(lambda:
            QApplication.clipboard().setText(enlace))
        self.ui.gridLayout.addWidget(self.label_error, 2, 1, 1, 1)
        self.ui.listWidget.setEnabled(False)
        self.ui.frame_4.setEnabled(False)
    
    #             /Control de errores              #
    ################################################

    def resizeEvent(self, event):

        if repo and lista_app:
            self.Listar_Apps(lista_global)

    ################################################
    #              Busqueda de apps                #

    def search_app(self):
        text = self.ui.lineEdit.text()

        lista_search = {}
        contador = 0
        global lista_global
        if len(text) != 0 and len(text) > 2:
            self.ui.listWidget.clearSelection()
            for elemento in lista_app:
                if elemento[0] not in self.lista_excluir and elemento[0].startswith(text) or text in elemento[1]:
                    indice = lista_app.index(elemento)
                    item = lista_app[indice]
                    lista_search[contador] = item
                    contador += 1
            else:
                lista_global = lista_search
        else:
            lista_global = lista_inicio
        self.Listar_Apps(lista_global)
   
    def clear_search_txt(self):
        self.ui.lineEdit.setText("")

    #              /Busqueda de apps               #
    ################################################

    ################################################
    #                Filtro de apps                #

    def listwidgetclicked(self, item):
        filtro = list() # Limpiamos la lista
        global lista_global

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
            global lista_global
            lista_global = self.Get_App_Filter(lista_app, filtro)
            self.Listar_Apps(lista_global)
        else:
            lista_global = lista_inicio

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
                    categoria_app = elemento[3].lower().split("/")
                    for filtro_uno in categoria_app:
                        if filtro_uno in filtro:
                            lista_filtrada[contador] = elemento
                            contador += 1
            else:
                for elemento in lista_app:
                    if elemento[3].lower() not in filtros:
                        lista_filtrada[contador] = elemento
                        contador += 1

        return lista_filtrada
        
    #           Aplicaciones Inicio              #
    def Apps_inicio(self, lista_app):
        global total_apps, lista_inicio, lista_global
        lista_inicio = {}
        lista_key = []
        contador = True
        while contador:
            if len(lista_key) == 8:
                contador = False
            else:
                key = randint(0, (total_apps-1))
                if key not in lista_key:
                    lista_key.append(key)

        contador = 0
        for key in lista_key:
            lista_inicio[contador] = lista_app[key]
            contador += 1

        lista_global = lista_inicio

    #           Listar aplicaciones              #
    def Listar_Apps(self, lista):
        equal = lista_inicio == lista_global
        if equal: 
            item = self.ui.listWidget.item(0)
            item.setSelected(True)

        while self.ui.gridLayout.count():
            item = self.ui.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        y = 0 # Creamos la coordenada y
        x = 0 # Creamos la coordenada x 
        # Estas para establecer la ubicacion de la tarjetas en la grilla
        i = 0
        self.calcular_columnas()
        for key in lista: # Recorremos la lista con los elementos
            i += 1 # Contador para agregar el espaciador horizontal
            # Consultamos si ya tenemos tres tarjetas en y
            if y % columnas == 0 and y != 0:
                y = 0 # Reiniciamos y
                x += 1 # Agregamos otra columna
            y += 1 # agregamos 1 a la coordenada y

            # Creamos una instancia de la clase card
            carta = Card(lista[key][0], lista[key][1], lista[key][2], lista[key][4], self)
            # Agregamos dicha instancia a la grilla
            self.ui.gridLayout.addWidget(carta, x, y, 1, 1)
        self.ui.frame.verticalScrollBar().setSliderPosition(0)

        # Espaciador vertical
        spacerItem9 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.ui.gridLayout.addItem(spacerItem9, (x+1), 1, 1, 1)

        # Si tenemos menos apps que las columnas, agregamos el espaciador
        if i < columnas:
            # Espaciador horizontal
            spacerItem8 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.ui.gridLayout.addItem(spacerItem8, x, columnas, 1, 10)

    #                /Lista de apps                #

    #              Calcular columnas               #
    def calcular_columnas(self):
      if width < 1360:
          base = 180
      elif width >= 1360 and width < 2500:
          base = 210
      elif width > 2500:
          base = 420

      ancho = self.ui.frame.frameGeometry().width()
      global columnas, tamanio
      
      if ancho < 700: ancho = ancho_inicio
      
      columnas = ancho // (base + 40)
      restante = ancho % (base + 40)
      tamanio = base + (restante // columnas)

    def calcular_anchos(self):
      width_screen = int(width * 0.7)
      if width_screen < 945: width_screen = 945

      size_frame = int(width * 0.14)
      if size_frame < 200: size_frame = 200
      if size_frame > 300: size_frame = 300
      global ancho_inicio
      ancho_inicio = width_screen - size_frame


    #              /Calcular columnas              #
    ################################################

    def contar_apps(self):
        global selected_apps
        cuenta = len(selected_apps)
        if cuenta == 0:
            texto = "Seleccione las aplicaciones a instalar"
            borde = "border: 2px solid rgb(45, 45, 45);"
            r, g, b = 255, 255, 255
            cursor = QtCore.ArrowCursor
            enabled = False
        else:
            borde = "border: 2px solid #419fd9;"
            r, g, b = 0, 255, 255
            cursor = QtCore.PointingHandCursor
            enabled = True

            if cuenta != 1:
                acentuacion, articulo, plural = "o", "es", "s"
            else:
                acentuacion, articulo, plural = "ó", "", ""
            texto = "{} aplicaci{}n{} seleccionada{} para instalar, clic aquí para verla{}".format(
                cuenta, acentuacion, articulo, plural, plural)
            
        self.ui.btn_install.setEnabled(enabled)
        self.ui.lbl_list_apps.setEnabled(enabled)
        self.ui.lbl_list_apps.setCursor(QCursor(cursor))

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

        shadow = QGraphicsDropShadowEffect(self,
          blurRadius=10,
          color=QColor(r,g,b),
          offset=QPointF(0, 0)
        )
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.ui.btn_install.setGraphicsEffect(shadow)


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
    #                   Acerca de                  #

    def acerca_de(self):
        self.modal = DAbout(self)
        self.modal.show()

    #                   /cerca de                  #
    ################################################

    ################################################
    #                   Centrar                    #
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        #mover = QPoint(self.x(), 100)
        self.move(qr.topLeft())
        #self.move(self.x(), self.y() - mover.y())

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


    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            self.oldPos = event.globalPos()
        elif event.type() == QEvent.MouseMove:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            
        return True


    def maximize(self):
        global maximized
        if maximized: # Restauramos al tamaño original
          self.setWindowState(Qt.WindowNoState)
          maximized = False
          icono = abspath(join(dirname(__file__), 'resources', 'maximizar.svg'))
          self.ui.widget_1.installEventFilter(self)
        else: # Agrandamos la ventana
          self.setWindowState(Qt.WindowMaximized)
          maximized = True
          icono = abspath(join(dirname(__file__), 'resources', 'restaurar.svg'))
          self.ui.widget_1.removeEventFilter(self)

        # Cambio de icono al maximizar
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(icono), QIcon.Normal, QIcon.Off)
        self.ui.btn_maximizar.setIcon(icon1)


    def minimize(self):
        global maximized
        # No se ve la app, agrandamos
        self.setWindowState(Qt.WindowMinimized)
        if maximized: # Si estaba maximizada, agrandamos
            self.setWindowState(Qt.WindowMaximized)

class QLabelClickable(QLabel):

    clicked = pyqtSignal()
    
    def __init__(self, *args):
        QLabel.__init__(self, *args)
   
    def mouseReleaseEvent(self, ev):
        self.clicked.emit()

################################################
#           Card para la aplicacion            #

class Card(QFrame):
    def __init__(self, titulo: str, descripcion: str, version: str, estado: int, parent):
        super(Card, self).__init__()
        self.parentWindow = parent
        self.cd = Ui_Frame()
        self.cd.setupUi(self)
        # Establecemos los atributos de la app
        #self.cd.btn_select_app.setToolTip(version)
        self.titulo = titulo
        self.version = version
        self.cd.lbl_name_app.setText(self.titulo)
        self.cd.image_app.setToolTip("<p wrap='hard'>{}</p>".format(descripcion))
        self.cd.image_app.setWordWrap(True)
        self.setMinimumSize(QSize(tamanio+30, int((tamanio+115)*0.72222)))
        self.setMaximumSize(QSize(tamanio+30, int((tamanio+115)*0.72222)))
        self.cd.image_app.setMinimumSize(QSize(tamanio, int(tamanio*0.72222)))

        self.texto_version()

        global instaladas
        if self.titulo not in instaladas:
            estado = 1
            if self.titulo in selected_apps:
                estado = 0
        else:
            estado = 2
        
        if self.titulo not in selected_apps and self.titulo not in instaladas:
            self.installEventFilter(self)

        self.change_color_buton(estado)
        # Consultamos si existe el grafico de la app
        ruta = abspath(join(dirname(__file__), 'resources/apps', self.titulo + '.svg'))
        if not os.path.exists(ruta):
            url = abspath(join(dirname(__file__), 'resources/apps', 'no-img.svg'))
        else:
            url = ruta
        # Establecemos la imagen
        pixmap = QPixmap(url)
        self.cd.image_app.setPixmap(pixmap)
        self.cd.btn_select_app.clicked.connect(lambda: self.select_app(self.titulo))
        self.cd.image_app.clicked.connect(lambda: self.select_app(self.titulo))
        self.cd.lbl_name_app.clicked.connect(lambda: self.select_app(self.titulo))

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            radius = 20
        elif event.type() == QEvent.Leave:
            radius = 0
        else:
            return False

        shadow = QGraphicsDropShadowEffect(self,
              blurRadius=radius,
              color=QColor(255,255,255),
              offset=QPointF(0, 0))
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)
        return True
    
    def texto_version(self):
        if self.titulo in selected_apps:
            self.cd.btn_select_app.setText("Seleccionada")
            color = "color: rgb(0, 255, 255);"
        elif self.titulo in instaladas:
            self.cd.btn_select_app.setText("Instalada")
            color = "color: rgb(0, 212, 0);"
        else:
            self.cd.btn_select_app.setText("v: {}".format(self.version))
            color = "color: rgb(107,107,107);"

        self.cd.btn_select_app.setStyleSheet("border: transparent;\n"
        "background-color: transparent;"
        + color + 
        "border-bottom-right-radius:5px; border-bottom-left-radius:5px;"
        "margin-bottom: 5px;")

    def select_app(self, titulo):
        global selected_apps, lista_app, instaladas, lista_selected, contador_selected
        
        for elemento in lista_app:
            if titulo in elemento: 
                indice = lista_app.index(elemento)

        # Si la app no esta instalada
        if titulo not in instaladas:
            # Si la app no esta seleccionada
            if titulo not in selected_apps:
                selected_apps.append(titulo)
                
                
                for elemento in lista_app:
                    if elemento[0] == titulo:    
                        indice = lista_app.index(elemento)
                        item = lista_app[indice]
                        lista_selected[contador_selected] = item
                        contador_selected += 1

                lista_app[indice][4] = 0
                self.change_color_buton(0)
                self.removeEventFilter(self)
            else:
                selected_apps.remove(titulo)
                

                count = 0
                for elemento in lista_selected:
                    titulo_elemento = lista_selected[elemento]

                    if titulo_elemento[0] == titulo:    
                        eliminar = elemento
                    count += 1
                
                lista_selected.pop(eliminar)
                

                lista_app[indice][4] = 1
                self.change_color_buton(1)
                self.installEventFilter(self)
        else:
            self.change_color_buton(2)

        self.texto_version()
        self.parentWindow.contar_apps()

    def change_color_buton(self, estado: int):
        if estado == 0: # App seleccionada RGB(0,255,255)
            r, g, b=0, 255, 255
            radio = 20
            border_color = "border-color: #00bbc8;"
        elif estado == 1: # App no seleccionada RGB(45,45,45)
            r, g, b=45, 45, 45
            radio = 0
            border_color = "border-color: transparent;"
        else: # app instalada RGB(0,212,0)
            r, g, b=0, 212, 0
            radio = 20
            border_color = "border-color: #009800;"
            self.cd.btn_select_app.setEnabled(False)

        self.setStyleSheet("#Frame{"
            "background-color: #2d2d2d;"
            "border-radius: 10px;"
            "margin: 10px;"
            + border_color +
            "border-width: 1px;"
            "border-style: solid;"
            "}"
            "QToolTip {"
            "border: 2px solid #419fd9;"
            "border-radius: 4px;"
            "padding: 2px;"
            "font-size: 12px;"
            "background-color: transparent;"
            "})")

        shadow = QGraphicsDropShadowEffect(self,
          blurRadius=radio,
          color=QColor(r, g, b),
          offset=QPointF(0, 0)
        )
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)


            
            
#           /Card para la aplicacion           #
################################################

def ejecutar():
  app = QApplication(sys.argv)
  global width, height, maximized
  maximized = False
  screen_rect = app.desktop().screenGeometry()
  width, height = screen_rect.width(), screen_rect.height()
  win = Ventana()
  win.calcular_anchos()
  os.system('xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {}'.format(int(win.winId())))
  win.show()
  sys.exit(app.exec_())