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
from PyQt5.QtGui import QPixmap, QFont, QColor, QCursor, QPainter

from typing import List

from deepinesStore.core import set_blur
# Para obtener applicacion random
from random import choice
# GUI o modulos locales
from deepinesStore.app_info import AppInfo, AppType, AppState
from deepinesStore.maing import Ui_MainWindow
from deepinesStore.cardg import Ui_Frame
from deepinesStore.dialog_install import Ui_DialogInstall
from deepinesStore.about import AboutDialog
from deepinesStore.core import get_res, get_app_icon
from deepinesStore.flatpak.get_apps_flatpak import fetch_list_app_flatpak, apps_flatpak_in_categories
from deepinesStore.deb.get_apps_deb import fetch_list_app_deb
from deepinesStore.widgets import LinkLabel
import deepinesStore.demoted_actions as demoted

# Global variables
global lista_inicio, lista_global, lista_selected, lista_temp
global selected_apps, instaladas, columnas, tamanio


class StoreMWindow(QMainWindow):
	def __init__(self):
		super(StoreMWindow, self).__init__()
		# Inicializamos la gui
		global ui
		ui = Ui_MainWindow(width, height)
		ui.setupUi(self)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)

		global selected_apps, instaladas,\
			lista_inicio, lista_global, lista_selected, \
			selected_type_app
		repo_file = "/etc/apt/sources.list.d/deepines.list"
		if os.path.exists(repo_file):
			self.lista_excluir = self.Get_App_Exclude()
			self.lista_deepines = self.Get_App_Deepines()
			# Variables globales
			selected_apps = list()
			lista_selected = list()
			# Almacenamos la lista, para cargarla solo al inicio
			self.lista_app_deb = fetch_list_app_deb(self.lista_excluir)
			self.total_apps_deb = len(self.lista_app_deb)
			self.lista_app_flatpak = apps_flatpak_in_categories()
			self.total_apps_flatpak = len(self.lista_app_flatpak)
			instaladas = self.get_installed_apps()

			selected_type_app = 0 # 0 by debs

			if self.lista_app_deb and self.lista_app_flatpak:
				# Obtenemos aplicaciones para la lista de apps
				self.inicio_apps_deb = self.Apps_inicio(self.lista_app_deb)
				self.inicio_apps_flatpak = self.Apps_inicio(self.lista_app_flatpak)
				lista_global = self.lista_app_deb
				lista_inicio = self.inicio_apps_deb
				self.primer_inicio = True
				
			else:
				self.error(ui.error_no_server_text)
		else:
			self.error(ui.error_no_deepines_repo_text)

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

	def error(self, text: str):
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

		self.label_error = LinkLabel(self)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(
			self.label_error.sizePolicy().hasHeightForWidth())
		self.label_error.setSizePolicy(sizePolicy)
		font = QFont()
		font.setPointSize(16)
		self.label_error.setFont(font)
		self.label_error.setScaledContents(True)
		self.label_error.setText(text)
		self.label_error.setEnabled(True)
		self.label_error.setAlignment(QtCore.AlignCenter)
		self.label_error.setObjectName("label_error")
		ui.gridLayout.addWidget(self.label_error, 2, 1, 1, 1)
		ui.listWidget.setEnabled(False)
		ui.frame_4.setEnabled(False)

	#			 /Control de errores			  #
	################################################

	def resizeEvent(self, event):
		if hasattr(self, 'primer_inicio') and self.primer_inicio:
			global lista_temp
			lista_temp = lista_inicio
			self.primer_inicio = False
		try:
			self.do_list_apps(lista_temp)
		except NameError:
			pass  # There are no apps, lista_temp is not defined...


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
			ui.listWidget.item(1).setHidden(True)
		else:
			# Seleccionamos deb
			selected_type_app = 0
			ui.btn_app_deb.setEnabled(False)
			ui.btn_app_deb.setStyleSheet(style_selected)
			ui.btn_app_flatpak.setEnabled(True)
			ui.btn_app_flatpak.setStyleSheet(style_unselected)
			lista_global = self.lista_app_deb
			lista_inicio = self.inicio_apps_deb
			ui.listWidget.item(1).setHidden(False)
		
		self.do_list_apps(lista_inicio)
		item = ui.listWidget.item(0)
		item.setSelected(True)

	#			  /Cambiar tipo de app			#
	################################################

	################################################
	#			  Busqueda de apps				#

	def search_app(self):
		text = ui.lineEdit.text().lower()

		lista_search = list()
		global lista_global, lista_temp
		if len(text) != 0 and len(text) > 2:
			ui.listWidget.clearSelection()
			for app_item in lista_global:
				if text in str(app_item.name).lower() or text in str(app_item.description).lower():
					indice = lista_global.index(app_item)
					item = lista_global[indice]
					lista_search.append(item)
			else:
				lista_temp = lista_search
		else:
			lista_temp = lista_inicio
		self.do_list_apps(lista_temp)

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
		if item == ui.listWidget.item(11):
			filtro.append("installed")			

		if "inicio" not in filtro and "installed" not in filtro:
			# TODO: Cambiar funcionamiento por una separacion de las app
			# TODO: en listas en diccionarios fijos, al cargar la tienda.
			global lista_temp
			lista_temp = self.Get_App_Filter(lista_global, filtro)
		elif "installed" in filtro:
			lista_temp = instaladas
		else:
			lista_temp = lista_inicio

		self.do_list_apps(lista_temp)
		self.clear_search_txt()

	#			   /Filtro de apps				#
	################################################

	################################################
	#				Lista de apps				 #

	#		   Filtrar aplicaciones			 #
	def Get_App_Filter(self, lista_app, filtro):
		lista_filtrada = list()
		filtros = ['web', 'net', 'mail', 'sound', 'audio', 'video', 'audiovideo'
					'graphics', 'office','media', 'games', 'game', 'editors', 'devel', 'shell',
					'admin', 'python', 'development','network', 'networking',
					'productivity', 'system', 'utility']
		if 'deepines' in filtro:
			for app in self.lista_deepines:
				for elemento in lista_app:
					if elemento.name == app:
						lista_filtrada.append(elemento)
		else:
			if "otros" not in filtro:
				for elemento in lista_app:
					categoria_app = elemento.category.lower().split("/")
					for filtro_uno in categoria_app:
						if filtro_uno in filtro:
							lista_filtrada.append(elemento)
			else:
				for elemento in lista_app:
					if elemento.category.lower() not in filtros:
						lista_filtrada.append(elemento)

		return lista_filtrada

	#		   Aplicaciones Inicio			  #
	def Apps_inicio(self, lista_app: List[AppInfo]):
		lista_key = []
		contador = True
		while contador:
			if len(lista_key) == 8:
				contador = False
			else:
				key = choice(lista_app)
				if key not in lista_key:
					lista_key.append(key)

		return lista_key

	#		   Listar aplicaciones			  #
	def do_list_apps(self, lista):
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
			carta = Card(item, self)
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

	def get_installed_apps(self):
		self.list_installed = list()

		dpkg_cmd = os.popen("dpkg --get-selections")
		installed_debs = [line.split()[0] for line in dpkg_cmd.read().splitlines() if line.split()[1] == "install"]
		dpkg_cmd.close()

		for installed_deb in installed_debs:
			for app_item in self.lista_app_deb:
				if installed_deb == app_item.id:
					self.list_installed.append(app_item)

		flatpak_cmd = demoted.run_cmd(demoted.DEF, cmd=['flatpak', '--user', 'list', '--columns=application'])
		installed_ids = [line.rstrip("\n") for line in flatpak_cmd.stdout.readlines()]

		for installed_id in installed_ids:
			for app_item in self.lista_app_flatpak:
				if installed_id == app_item.id:
					self.list_installed.append(app_item)

		return(self.list_installed)

	#			   /Apps Instaladas				#
	################################################

	################################################
	#			Apps nuevas Instaladas			#

	def installation_completed(self):
		global selected_apps, instaladas
		lista_complete = list()
		for app in selected_apps:
			lista_complete.append(app)
			instaladas.append(app) # FIXME: Check if it is really installed
			
		selected_apps = list()
		self.do_list_apps(lista_complete)
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
		self.do_list_apps(lista_selected)
		ui.listWidget.clearSelection()

################################################
#		   Card para la aplicacion			#


class Card(QFrame):
	def __init__(self, application: list, parent):
		super(Card, self).__init__()
		self.parentWindow = parent
		self.cd = Ui_Frame()
		self.cd.setupUi(self)
		# Establecemos los atributos de la app
		# self.cd.btn_select_app.setToolTip(version)
		self.application = application
		self.titulo = self.application.name
		self.descripcion = self.application.description
		self.cd.lbl_name_app.setText(self.titulo)
		self.cd.image_app.setToolTip(
			"<p wrap='hard'>{}</p>".format(self.descripcion))
		self.cd.image_app.setWordWrap(True)
		self.setMinimumSize(QSize(tamanio+30, int((tamanio+115)*0.72222)))
		self.setMaximumSize(QSize(tamanio+30, int((tamanio+115)*0.72222)))
		self.cd.image_app.setMinimumSize(QSize(tamanio, int(tamanio*0.72222)))

		self.texto_version()

		global instaladas
		if self.application not in instaladas:
			state = AppState.DEFAULT
			if self.application in selected_apps:
				state = AppState.SELECTED
		else:
			state = AppState.INSTALLED

		if self.application not in selected_apps and self.application not in instaladas:
			self.installEventFilter(self)

		self.change_color_buton(state)

		# Establecemos la imagen
		if (self.application.type == AppType.DEB_PACKAGE):
			app_banner = QPixmap(self.get_banner_path(self.application.id))
			self.cd.image_app.setPixmap(app_banner)
		if (self.application.type == AppType.FLATPAK_APP):
			# use app id, if not found, then use the alternative app name
			alt_app_name = str(self.application.name).lower().replace(" ", "-") # TODO: Check if replacing it by nothing fetches something...
			app_banner = QPixmap(self.get_banner_path(self.application.id, alt_app_name))
			app_overlay = QPixmap(get_res('flatpak'))
			app_pixmap = QPixmap(app_banner)
			painter = QPainter(app_pixmap)
			painter.drawPixmap(0, 0, app_overlay)
			painter.end()
			self.cd.image_app.setPixmap(app_pixmap)

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

	def get_banner_path(self, app_name: str, alt_app_name: str = ""):
		path = get_res(app_name, 'resources/apps')

		if alt_app_name and not os.path.exists(path):
			return self.get_banner_path(alt_app_name)

		if not os.path.exists(path):
			path = get_res('no-img', 'resources/apps')

		return path

	def texto_version(self):
		if self.application in selected_apps:
			self.cd.btn_select_app.setText(ui.selected_to_install_app_text)
			color = "color: rgb(0, 255, 255);"
		elif self.titulo in instaladas:
			self.cd.btn_select_app.setText(ui.selected_installed_app_text)
			color = "color: rgb(0, 212, 0);"
		else:
			self.cd.btn_select_app.setText("v: {}".format(self.application.version))
			color = "color: rgb(107,107,107);"

		self.cd.btn_select_app.setStyleSheet("border: transparent;\n"
											 "background-color: transparent;"
											 + color +
											 "border-bottom-right-radius:5px; border-bottom-left-radius:5px;"
											 "margin-bottom: 5px;")

	def select_app(self, titulo): # FIXME: Not needed parameter?
		global lista_global, selected_apps, instaladas, lista_selected

		# Si la app no esta instalada
		if self.application not in instaladas:
			lista_global_temp = lista_global
			if (self.application.type == AppType.DEB_PACKAGE):
				lista_global = self.parentWindow.lista_app_deb
			if (self.application.type == AppType.FLATPAK_APP):
				lista_global = self.parentWindow.lista_app_flatpak
			indice = lista_global.index(self.application)
			# Si la app no esta seleccionada
			if self.application not in selected_apps:
				selected_apps.append(self.application)
				lista_selected.append(self.application)
				new_state = AppState.SELECTED
				self.removeEventFilter(self)
			else:
				selected_apps.remove(self.application)
				lista_selected.remove(self.application)
				new_state = AppState.DEFAULT
				self.installEventFilter(self)
				

			lista_global[indice].state = new_state
			lista_global = lista_global_temp
			self.change_color_buton(new_state)
		else:
			self.change_color_buton(AppState.INSTALLED)

		self.texto_version()
		self.parentWindow.contar_apps()

	def change_color_buton(self, state: AppState):
		#if state == AppState.DEFAULT:
		r, g, b = 45, 45, 45
		radio = 0
		border_color = "border-color: transparent;"

		if state == AppState.SELECTED:
			r, g, b = 0, 255, 255
			radio = 20
			border_color = "border-color: #00bbc8;"
		if state == AppState.INSTALLED:
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
