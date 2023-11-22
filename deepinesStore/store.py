#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
# PyQt5 modules
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTranslator, QLocale, QSize, QPointF, QPoint, QEvent, Qt as QtCore, pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QLabel,
							 QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem,
							 QDesktopWidget, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QFont, QColor, QCursor
# Modulos para el scraping
from bs4 import BeautifulSoup
from deepinesStore.core import get_dl, set_blur, get_deepines_uri
# Para obtener applicacion random
from random import choice
# GUI o modulos locales
from deepinesStore.maing import Ui_MainWindow
from deepinesStore.cardg import Ui_Frame
from deepinesStore.dialog_install import Ui_DialogInstall
from deepinesStore.about import AboutDialog
from deepinesStore.core import get_res, get_app_icon
from deepinesStore.flatpak.get_apps_flatpak import fetch_list_app_flatpak, apps_flatpak_in_categories
from deepinesStore.deb.get_apps_deb import fetch_list_app_deb

if os.name == 'nt':
	try:
		from ctypes import windll
		windll.shell32.SetCurrentProcessExplicitAppUserModelID('Deepines Store')
	except AttributeError:
        # Not available?
		pass

# Global variables
global lista_inicio, lista_global, lista_selected, lista_temp
global selected_apps, instaladas, columnas, tamanio,\
	  contador_selected


class StoreMWindow(QMainWindow):
	def __init__(self):
		super(StoreMWindow, self).__init__()
		# Inicializamos la gui
		global ui
		ui = Ui_MainWindow(width, height)
		ui.setupUi(self)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.lista_excluir = self.Get_App_Exclude()
		self.lista_deepines = self.Get_App_Deepines()

		global selected_apps, instaladas,\
			lista_inicio, lista_global, lista_selected, \
			contador_selected, selected_type_app
		repo_file = "/etc/apt/sources.list.d/deepines.list"
		if os.path.exists(repo_file):
			# Variables globales
			selected_apps = list()
			lista_selected = {}
			contador_selected = 0
			instaladas = self.apps_instaladas()
			# Almacenamos la lista, para cargarla solo al inicio
			self.lista_app_deb = fetch_list_app_deb(self.lista_excluir)
			self.total_apps_deb = len(self.lista_app_deb)
			self.lista_app_flatpak = apps_flatpak_in_categories()
			self.total_apps_flatpak = len(self.lista_app_flatpak)

			selected_type_app = 0 # 0 by debs

			if self.lista_app_deb and self.lista_app_flatpak:
				# Obtenemos aplicaciones para la lista de apps
				self.inicio_apps_deb = self.Apps_inicio(self.lista_app_deb)
				self.inicio_apps_flatpak = self.Apps_inicio(self.lista_app_flatpak)
				lista_global = self.lista_app_deb
				lista_inicio = self.inicio_apps_deb
				self.primer_inicio = True
				
			else:
				self.error(ui.error_no_server_text, "https://deepinenespañol.org")
		else:
			self.error(ui.error_no_deepines_repo_text, "https://deepinenespañol.org/repositorio")

		ui.btn_install.setEnabled(False)
		ui.btn_install.clicked.connect(self.window_install)
		ui.lbl_list_apps.setText(ui.list_apps_text)
		ui.lbl_list_apps.setEnabled(False)
		ui.icon_car.clicked.connect(self.apps_seleccionadas)
		ui.lbl_list_apps.clicked.connect(self.apps_seleccionadas)
		ui.listWidget.itemClicked.connect(self.listwidgetclicked)
		ui.lineEdit.textChanged.connect(self.search_app)
		self.about_dialog = AboutDialog(self) #  Intentional preloading.
		ui.label_2.clicked.connect(self.show_about_dialog)
		ui.btn_close.clicked.connect(self.close)
		ui.btn_zoom.clicked.connect(self.maximize)
		ui.btn_minimize.clicked.connect(self.minimize)
		ui.widget_1.installEventFilter(self)
		ui.label.clicked.connect(self.show_about_dialog)
		ui.btn_app_deb.clicked.connect(self.change_type_app_selected)
		ui.btn_app_flatpak.clicked.connect(self.change_type_app_selected)
		shadow = QGraphicsDropShadowEffect(self,
										   blurRadius=10,
										   color=QColor(255, 255, 255),
										   offset=QPointF(0, 0)
										   )
		shadow.setXOffset(0)
		shadow.setYOffset(0)
		ui.btn_install.setGraphicsEffect(shadow)

		self.center()

	################################################
	#			 Control de errores			   #

	def error(self, text: str, link: str):
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

		ruta = get_res('raccoon')
		pixmap = QPixmap(ruta)
		self.raccoon.setPixmap(pixmap)
		self.horizontalLayout.addWidget(self.raccoon)
		ui.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

		self.label_error = QLabelClickable(self)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.label_error.sizePolicy().hasHeightForWidth())
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
		self.label_error.clicked.connect(lambda: QApplication.clipboard().setText(link))
		ui.gridLayout.addWidget(self.label_error, 2, 1, 1, 1)
		ui.listWidget.setEnabled(False)
		ui.frame_4.setEnabled(False)

	#			 /Control de errores			  #
	################################################

	def resizeEvent(self, event):
		if self.primer_inicio:
			self.Listar_Apps(lista_inicio)
			self.primer_inicio = False
		else: 
			self.Listar_Apps(lista_temp)


	################################################
	#			  Cambiar tipo de app			#

	def change_type_app_selected(self):
		global selected_type_app, lista_inicio, lista_global
		style_selected = """
		background-color: rgb(203, 203, 203);
		"""
		style_unselected = ""
		if selected_type_app == 0:
			# Seleccionamos flatpak
			selected_type_app = 1
			ui.btn_app_deb.setEnabled(True)
			ui.btn_app_deb.setStyleSheet(style_unselected)
			ui.btn_app_flatpak.setEnabled(False)
			ui.btn_app_flatpak.setStyleSheet(style_selected)
			lista_global = self.lista_app_flatpak
			lista_inicio = self.inicio_apps_flatpak
		else:
			# Seleccionamos deb
			selected_type_app = 0
			ui.btn_app_deb.setEnabled(False)
			ui.btn_app_deb.setStyleSheet(style_selected)
			ui.btn_app_flatpak.setEnabled(True)
			ui.btn_app_flatpak.setStyleSheet(style_unselected)
			lista_global = self.lista_app_deb
			lista_inicio = self.inicio_apps_deb
		
		self.Listar_Apps(lista_inicio)
		item = ui.listWidget.item(0)
		item.setSelected(True)

	#			  /Cambiar tipo de app			#
	################################################

	################################################
	#			  Busqueda de apps				#

	def search_app(self):
		text = ui.lineEdit.text()

		lista_search = {}
		contador = 0
		global lista_global
		if len(text) != 0 and len(text) > 2:
			ui.listWidget.clearSelection()
			for elemento in lista_app_deb:
				if elemento[0] not in self.lista_excluir and elemento[0].startswith(text) or text in elemento[1]:
					indice = lista_app_deb.index(elemento)
					item = lista_app_deb[indice]
					lista_search[contador] = item
					contador += 1
			else:
				lista_global = lista_search
		else:
			lista_global = lista_inicio
		self.Listar_Apps(lista_global)

	def clear_search_txt(self):
		ui.lineEdit.setText("")

	#			  /Busqueda de apps			   #
	################################################

	################################################
	#				Filtro de apps				#

	def listwidgetclicked(self, item):
		filtro = list()  # Limpiamos la lista
		global lista_global, lista_inicio

		# TODO: Maybe a switch statement would be nice here
		if item == ui.listWidget.item(0):  # Home
			filtro.append("inicio")
		if item == ui.listWidget.item(1):  # Deepines
			filtro.append("deepines")
		if item == ui.listWidget.item(2):  # Internet
			filtro.append("web")
			filtro.append("net")
			filtro.append("mail")
			filtro.append("networking")
			filtro.append("network")
		if item == ui.listWidget.item(3):  # Multimedia
			filtro.append("sound")
			filtro.append("audio")
			filtro.append("video")
			filtro.append("audiovideo")
		if item == ui.listWidget.item(4):  # Graphics
			filtro.append("graphics")
			filtro.append("media")
		if item == ui.listWidget.item(5):  # Games
			filtro.append("games")
			filtro.append("game")
		if item == ui.listWidget.item(6):  # Office automation
			filtro.append("editors")
			filtro.append("office")
			filtro.append("productivity")
		if item == ui.listWidget.item(7):  # Development
			filtro.append("devel")
			filtro.append("shells")
			filtro.append("development")
		if item == ui.listWidget.item(8):  # System
			filtro.append("admin")
			filtro.append("python")
			filtro.append("system")
			filtro.append("utility")
		if item == ui.listWidget.item(9):  # Other
			filtro.append("otros")
			filtro.append("education")
			filtro.append("science")

		if "inicio" not in filtro:
			# TODO: Cambiar funcionamiento por una separacion de las app
			# TODO: en listas en diccionarios fijos, al cargar la tienda.
			global lista_temp
			lista_temp = self.Get_App_Filter(lista_global, filtro)
		else:
			lista_temp = lista_inicio

		self.Listar_Apps(lista_temp)
		self.clear_search_txt()

	#			   /Filtro de apps				#
	################################################

	################################################
	#				Lista de apps				 #




	#		   Filtrar aplicaciones			 #
	def Get_App_Filter(self, lista_app, filtro):
		lista_filtrada = list()
		filtros = ['web', 'net', 'mail', 'sound', 'audio', 'video',
					'graphics', 'media', 'games', 'editors', 'devel', 'shell',
					'admin', 'python', 'network', 'networking']
		if 'deepines' in filtro:
			for app in self.lista_deepines:
				for elemento in lista_app:
					if elemento[0] == app:
						lista_filtrada.append(elemento)
		else:
			if "otros" not in filtro:
				for elemento in lista_app:
					categoria_app = elemento[3].lower().split("/")
					for filtro_uno in categoria_app:
						if filtro_uno in filtro:
							lista_filtrada.append(elemento)
			else:
				for elemento in lista_app:
					if elemento[3].lower() not in filtros:
						lista_filtrada.append(elemento)

		return lista_filtrada

	#		   Aplicaciones Inicio			  #
	def Apps_inicio(self, lista_app):
		lista_key = []
		contador = True
		i=0
		while contador:
			if len(lista_key) == 8:
				contador = False
			else:
				key = choice(lista_app)
				if key not in lista_key:
					lista_key.append(key)
					i+= 1

		return lista_key

	#		   Listar aplicaciones			  #
	def Listar_Apps(self, lista):
		global lista_inicio, lista_global
		equal = lista_inicio == lista_global
		if equal:
			item = ui.listWidget.item(0)
			item.setSelected(True)

		while ui.gridLayout.count():
			item = ui.gridLayout.takeAt(0)
			widget = item.widget()
			if widget:
				widget.deleteLater()

		y = 0  # Creamos la coordenada y
		x = 0  # Creamos la coordenada x
		# Estas para establecer la ubicacion de la tarjetas en la grilla
		i = 0
		self.calcular_columnas()
		for item in lista:  # Recorremos la lista con los elementos
			i += 1  # Contador para agregar el espaciador horizontal
			# Consultamos si ya tenemos tres tarjetas en y
			if y % columnas == 0 and y != 0:
				y = 0  # Reiniciamos y
				x += 1  # Agregamos otra columna
			y += 1  # agregamos 1 a la coordenada y

			# Creamos una instancia de la clase card
			carta = Card(item[0], item[1],
						 item[2], item[4], self)
			# Agregamos dicha instancia a la grilla
			ui.gridLayout.addWidget(carta, x, y, 1, 1)
		ui.frame.verticalScrollBar().setSliderPosition(0)

		# Espaciador vertical
		spacerItem9 = QSpacerItem(
			0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		ui.gridLayout.addItem(spacerItem9, (x+1), 1, 1, 1)

		# Si tenemos menos apps que las columnas, agregamos el espaciador
		if i < columnas:
			# Espaciador horizontal
			spacerItem8 = QSpacerItem(
				0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
			ui.gridLayout.addItem(spacerItem8, x, columnas, 1, 10)

	#		Lista aplicaciones excluidas		  #
	def Get_App_Exclude(self):
		lista = list()
		ruta_excluidos = get_res('excluidos', ext='.txt', dir='config')
		excluidos = open(ruta_excluidos, 'r')

		for line in excluidos:
			line = line.replace('\n', '')
			lista.append(line)

		return lista

	#		Lista aplicaciones excluidas		  #
	def Get_App_Deepines(self):
		lista = list()
		ruta_deepines = get_res('deepines', ext='.txt', dir='config')
		deepines = open(ruta_deepines, 'r')

		for line in deepines:
			line = line.replace('\n', '')
			lista.append(line)

		return lista

	#				/Lista de apps				#
	################################################

	################################################
	#			  Calcular columnas			   #
	def calcular_columnas(self):
		if width < 1360:
			base = 180
		elif width >= 1360 and width < 2500:
			base = 210
		elif width > 2500:
			base = 420

		ancho = ui.frame.frameGeometry().width()
		global columnas, tamanio

		if ancho < 700:
			ancho = ancho_inicio

		columnas = ancho // (base + 40)
		restante = ancho % (base + 40)
		tamanio = base + (restante // columnas)

	def calcular_anchos(self):
		width_screen = int(width * 0.7)
		if width_screen < 945:
			width_screen = 945

		size_frame = int(width * 0.14)
		if size_frame < 200:
			size_frame = 200
		if size_frame > 300:
			size_frame = 300
		global ancho_inicio
		ancho_inicio = width_screen - size_frame

	#			  /Calcular columnas			  #
	################################################

	def contar_apps(self):
		global selected_apps
		cuenta = len(selected_apps)
		if cuenta == 0:
			texto = ui.list_apps_text
			borde = "border: 2px solid rgb(45, 45, 45);"
			r, g, b = 255, 255, 255
			cursor = QtCore.ArrowCursor
			enabled = False
			pix_car = "carDisable"
		else:
			borde = "border: 2px solid #419fd9;"
			r, g, b = 0, 255, 255
			cursor = QtCore.PointingHandCursor
			enabled = True
			pix_car = "carEnable"

			if cuenta != 1:
				preview_to_install = ui.multi_apps_text
			else:
				preview_to_install = ui.single_app_text
			texto = preview_to_install.format(app_count=cuenta)

		ui.btn_install.setEnabled(enabled)
		ui.lbl_list_apps.setEnabled(enabled)
		ui.lbl_list_apps.setCursor(QCursor(cursor))

		pix_car = QPixmap(get_res(pix_car))
		ui.icon_car.setPixmap(pix_car)

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
		ui.btn_install.setStyleSheet(estilo)

		shadow = QGraphicsDropShadowEffect(self,
										   blurRadius=10,
										   color=QColor(r, g, b),
										   offset=QPointF(0, 0)
										   )
		shadow.setXOffset(0)
		shadow.setYOffset(0)
		ui.btn_install.setGraphicsEffect(shadow)

		ui.lbl_list_apps.setText(texto)

	################################################
	#				  Instalacion				 #

	def window_install(self):
		global selected_apps
		self.modal = Ui_DialogInstall(self, selected_apps)
		self.modal.show()

	#				 /Instalacion				 #
	################################################

	################################################
	#				     About   				  #

	def show_about_dialog(self):
		if not self.about_dialog.isVisible():
			self.about_dialog.show()

	#				     /About   				  #
	################################################

	################################################
	#				   Centrar					#
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		#mover = QPoint(self.x(), 100)
		self.move(qr.topLeft())
		#self.move(self.x(), self.y() - mover.y())

	#				  /Centrar					#
	################################################

	################################################
	#			   Apps Instaladas				#

	def apps_instaladas(self):
		comando = "dpkg --get-selections | grep -w install"
		lista = os.popen(comando)
		instaladas = list()
		for linea in lista.readlines():
			linea = ''.join(linea.split())
			linea = linea.replace("install", "")
			instaladas.append(linea)

		return(instaladas)

	#			   /Apps Instaladas				#
	################################################

	################################################
	#			Apps nuevas Instaladas			#

	def instalacion_completada(self):
		global selected_apps, instaladas
		lista_complete = {}
		contador = 0
		for app in selected_apps:
			for elemento in self.lista_app_deb:
				if elemento[0] == app:
					indice = self.lista_app_deb.index(elemento)
					item = self.lista_app_deb[indice]
					lista_complete[contador] = item
					contador += 1

			instaladas.append(app)
		selected_apps = list()
		self.Listar_Apps(lista_complete)
		self.contar_apps()

	#		   /Apps nuevas Instaladas			#
	################################################

	def eventFilter(self, obj, event):
		if event.type() == QEvent.MouseButtonPress:
			self.oldPos = event.globalPos()
		elif event.type() == QEvent.MouseMove:
			if hasattr(self, 'oldPos'):
				delta = QPoint(event.globalPos() - self.oldPos)
				self.move(self.x() + delta.x(), self.y() + delta.y())
				self.oldPos = event.globalPos()

		return True

	def maximize(self):
		global maximized
		if maximized:  # Restauramos al tamaño original
			self.setWindowState(Qt.WindowNoState)
			maximized = False
			ui.widget_1.installEventFilter(self)
		else:  # Agrandamos la ventana
			self.setWindowState(Qt.WindowMaximized)
			maximized = True
			ui.widget_1.removeEventFilter(self)

	def minimize(self):
		global maximized
		# No se ve la app, agrandamos
		self.setWindowState(Qt.WindowMinimized)
		if maximized:  # Si estaba maximizada, agrandamos
			self.setWindowState(Qt.WindowMaximized)

	def apps_seleccionadas(self):
		self.Listar_Apps(lista_selected)
		ui.listWidget.clearSelection()


class QLabelClickable(QLabel):

	clicked = pyqtSignal()

	def __init__(self, *args):
		QLabel.__init__(self, *args)

	def mouseReleaseEvent(self, ev):
		self.clicked.emit()

################################################
#		   Card para la aplicacion			#


class Card(QFrame):
	def __init__(self, titulo: str, descripcion: str, version: str, estado: int, parent):
		super(Card, self).__init__()
		self.parentWindow = parent
		self.cd = Ui_Frame()
		self.cd.setupUi(self)
		# Establecemos los atributos de la app
		# self.cd.btn_select_app.setToolTip(version)
		self.titulo = titulo
		self.version = version
		self.cd.lbl_name_app.setText(self.titulo)
		self.cd.image_app.setToolTip(
			"<p wrap='hard'>{}</p>".format(descripcion))
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
		ruta = get_res(self.titulo, 'resources/apps')
		if not os.path.exists(ruta):
			url = get_res('no-img', 'resources/apps')
		else:
			url = ruta
		# Establecemos la imagen
		pixmap = QPixmap(url)
		self.cd.image_app.setPixmap(pixmap)
		self.cd.btn_select_app.clicked.connect(
			lambda: self.select_app(self.titulo))
		self.cd.image_app.clicked.connect(lambda: self.select_app(self.titulo))
		self.cd.lbl_name_app.clicked.connect(
			lambda: self.select_app(self.titulo))

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			radius = 20
		elif event.type() == QEvent.Leave:
			radius = 0
		else:
			return False

		shadow = QGraphicsDropShadowEffect(self,
										   blurRadius=radius,
										   color=QColor(255, 255, 255),
										   offset=QPointF(0, 0))
		shadow.setXOffset(0)
		shadow.setYOffset(0)
		self.setGraphicsEffect(shadow)
		return True

	def texto_version(self):
		if self.titulo in selected_apps:
			self.cd.btn_select_app.setText(ui.selected_to_install_app_text)
			color = "color: rgb(0, 255, 255);"
		elif self.titulo in instaladas:
			self.cd.btn_select_app.setText(ui.selected_installed_app_text)
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
		global selected_apps, instaladas, lista_selected, contador_selected

		for elemento in self.parentWindow.lista_app_deb:
			if titulo in elemento:
				indice = self.parentWindow.lista_app_deb.index(elemento)

		# Si la app no esta instalada
		if titulo not in instaladas:
			# Si la app no esta seleccionada
			if titulo not in selected_apps:
				selected_apps.append(titulo)

				for elemento in self.parentWindow.lista_app_deb:
					if elemento[0] == titulo:
						indice = self.parentWindow.lista_app_deb.index(elemento)
						item = self.parentWindow.lista_app_deb[indice]
						lista_selected[contador_selected] = item
						contador_selected += 1

				self.parentWindow.lista_app_deb[indice][4] = 0
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

				self.parentWindow.lista_app_deb[indice][4] = 1
				self.change_color_buton(1)
				self.installEventFilter(self)
		else:
			self.change_color_buton(2)

		self.texto_version()
		self.parentWindow.contar_apps()

	def change_color_buton(self, estado: int):
		if estado == 0:  # App seleccionada RGB(0,255,255)
			r, g, b = 0, 255, 255
			radio = 20
			border_color = "border-color: #00bbc8;"
		elif estado == 1:  # App no seleccionada RGB(45,45,45)
			r, g, b = 45, 45, 45
			radio = 0
			border_color = "border-color: transparent;"
		else:  # app instalada RGB(0,212,0)
			r, g, b = 0, 212, 0
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
						   "}")

		shadow = QGraphicsDropShadowEffect(self,
										   blurRadius=radio,
										   color=QColor(r, g, b),
										   offset=QPointF(0, 0)
										   )
		shadow.setXOffset(0)
		shadow.setYOffset(0)
		self.setGraphicsEffect(shadow)


#		   /Card para la aplicacion		   #
################################################

def run_gui():
	app = QApplication(sys.argv)
	app.setWindowIcon(get_app_icon())
	translator = QTranslator()
	translator.load(QLocale(), "", "", get_res('', 'translations', ''), ".qm")
	app.installTranslator(translator)
	global width, height, maximized
	maximized = False
	screen_rect = app.desktop().screenGeometry()
	width, height = screen_rect.width(), screen_rect.height()
	store_win = StoreMWindow()
	store_win.calcular_anchos()
	set_blur(store_win)
	store_win.show()
	sys.exit(app.exec_())
