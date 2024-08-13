#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from typing import Dict, List
# PyQt5 modules
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTranslator, QLocale, QSize, QPointF, QEvent, QTimer, Qt as QtCore, pyqtSignal, QThread, QCoreApplication
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFrame, QLabel,
							 QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem,
							 QDesktopWidget, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtGui import QPixmap, QFont, QColor, QCursor, QPainter, QMovie

from deepinesStore.core import set_blur
# Para obtener applicacion random
from random import choice
# GUI o modulos locales
from deepinesStore.app_info import AppInfo, AppType, AppState, ProcessType
from deepinesStore.maing import Ui_MainWindow
from deepinesStore.cardg import Ui_Frame
from deepinesStore.about import AboutDialog
from deepinesStore.core import get_res, get_app_icon, get_dl
from deepinesStore.flatpak.get_apps_flatpak import app_list_flatpak
from deepinesStore.deb.get_apps_deb import fetch_list_app_deb
from deepinesStore.install_progress import InstallThread
from deepinesStore import setup
from deepinesStore.widgets import LinkLabel

class EventsMixin:
	def __init__(self):
		self.drag_position = None

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.setProperty("previous_position", self.pos())
			self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
		event.accept()
	
	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton and self.drag_position is not None:
			self.setCursor(Qt.SizeAllCursor)
			if not self.isMaximized():
				self.move(event.globalPos() - self.drag_position)
			else:
				self.showNormal()
		event.accept()

	def mouseReleaseEvent(self, event):
		self.setCursor(Qt.ArrowCursor)
		self.drag_position = None

	def keyPressEvent(self, event):
		if self.drag_position is not None and event.key() == Qt.Key_Escape:
			previous_position = self.property("previous_position")
			self.setCursor(Qt.ArrowCursor)
			if previous_position is not None:
				self.move(previous_position)
				self.drag_position = None
			event.accept()
		else:
			event.ignore()

	def resizeEvent(self, event):
		self.drag_position = None
		event.accept()

# Global variables
global lista_inicio, lista_global, list_app_show_temp, uninstalled
global list_app_exclude, list_app_deepines, list_app_deb, list_app_flatpak
global selected_apps, installed, columnas, tamanio


class StoreMWindow(QMainWindow, EventsMixin):
	def __init__(self):
		super(StoreMWindow, self).__init__()
		# Inicializamos la gui
		global ui
		ui = Ui_MainWindow(width, height)
		ui.setupUi(self)
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.install_thread = None
		self.refresh_app_grid_timer = QTimer(self)
		self.refresh_app_grid_timer.setSingleShot(True)
		self.refresh_app_grid_timer.timeout.connect(self.refresh_app_grid)

		global selected_apps, installed,\
			lista_inicio, lista_global, \
			selected_type_app, uninstalled, list_app_deepines, \
			list_app_flatpak, list_app_show_temp
		
		repo_file = "/etc/apt/sources.list.d/deepines.list"
		if os.path.exists(repo_file):
			self.deepines_app_list = list_app_deepines
			# Variables globales
			selected_apps = list()
			uninstalled = list()
			# Almacenamos la lista, para cargarla solo al inicio
			self.lista_app_deb = list_app_deb
			self.total_apps_deb = len(self.lista_app_deb)
			self.lista_app_flatpak = list_app_flatpak
			self.total_apps_flatpak = len(self.lista_app_flatpak)

			selected_type_app = AppType.DEB_PACKAGE
			if self.lista_app_deb and self.lista_app_flatpak:
				# Obtenemos aplicaciones para la lista de apps
				self.inicio_apps_deb = self.Apps_inicio(self.lista_app_deb)
				self.inicio_apps_flatpak = self.Apps_inicio(self.lista_app_flatpak)
				lista_global = self.lista_app_deb
				lista_inicio = self.inicio_apps_deb
				list_app_show_temp = lista_inicio
				self.primer_inicio = True
				self.show_apps_selected = False
			else:
				self.error(ui.error_no_server_text)
		else:
			self.error(ui.error_no_deepines_repo_text)
			

		ui.btn_install.setEnabled(False)
		ui.btn_install.clicked.connect(self.confirm_app_installation)
		ui.lbl_list_apps.setText(ui.list_apps_text)
		ui.lbl_list_apps.setEnabled(False)
		ui.icon_car.clicked.connect(self.confirm_app_installation)
		ui.lbl_list_apps.clicked.connect(self.confirm_app_installation)
		ui.lw_categories.itemClicked.connect(self.listwidgetclicked)
		ui.lineEdit.textChanged.connect(self.search_app)
		self.about_dialog = AboutDialog(self) #  Intentional preloading.
		ui.label_2.clicked.connect(self.show_about_dialog)
		ui.btn_close.clicked.connect(self.close)
		ui.btn_zoom.clicked.connect(self.maximize)
		ui.btn_minimize.clicked.connect(self.showMinimized)
		ui.widget_1.installEventFilter(self)
		ui.label.clicked.connect(self.show_about_dialog)
		ui.btn_app_deb.clicked.connect(self.change_type_app_selected)
		ui.btn_app_flatpak.clicked.connect(self.change_type_app_selected)
		shadow = set_shadow(self, QColor(255, 255, 255))
		ui.btn_install.setGraphicsEffect(shadow)

		center_window(self)

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
		self.status_widgets(False)

	#			 /Control de errores			  #
	################################################

	def status_widgets(self, status = False):
		ui.lw_categories.setEnabled(status)
		ui.frame_4.setEnabled(status)
		ui.btn_app_deb.setEnabled(status)
		ui.btn_app_flatpak.setEnabled(status)
		ui.widget.setEnabled(status)

	def resizeEvent(self, event):
		# is running a process
		if self.install_thread and self.install_thread.isRunning():
			return
		else:
			event.accept()
			if hasattr(self, 'primer_inicio') and self.primer_inicio:
				self.primer_inicio = False
			if 'list_app_show_temp' in globals():
				self.refresh_app_grid_timer.start(200)

	def refresh_app_grid(self):
		try:
			self.clear_gridLayout()
			self.do_list_apps(list_app_show_temp)
		except NameError:
			pass  # There are no apps?


	################################################
	#			  Cambiar tipo de app			#

	def change_type_app_selected(self):
		global selected_type_app, lista_inicio, lista_global
		style_flatpak = """
		background-color: rgb(169, 144, 122);
		color: #fff;
		border-color: #fff;
		border: 2px solid;
		border-radius: 15px;
		"""
		style_deb = """
		background-color: #A80030;
		color: #fff;
		border-color: #fff;
		border: 2px solid;
		border-radius: 15px;
		"""
		style_disabled = """
		color: rgb(0, 0, 0);
		background-color: rgba(0, 255, 255, 160);
		border-color: #00ffff;
		border: 2px solid;
		border-radius: 15px;
		"""
		if selected_type_app == AppType.DEB_PACKAGE:
			# Seleccionamos flatpak
			selected_type_app = AppType.FLATPAK_APP
			ui.btn_app_flatpak.setEnabled(False)
			ui.btn_app_deb.setEnabled(True)
			ui.btn_app_flatpak.setStyleSheet(style_disabled)
			ui.btn_app_deb.setStyleSheet(style_deb)
			lista_global = self.lista_app_flatpak
			list_app_show_temp = self.inicio_apps_flatpak
			ui.lw_categories.item(1).setHidden(True)
		else:
			# Seleccionamos deb
			selected_type_app = AppType.DEB_PACKAGE
			ui.btn_app_flatpak.setEnabled(True)
			ui.btn_app_deb.setEnabled(False)
			ui.btn_app_flatpak.setStyleSheet(style_flatpak)
			ui.btn_app_deb.setStyleSheet(style_disabled)
			lista_global = self.lista_app_deb
			list_app_show_temp = self.inicio_apps_deb
			ui.lw_categories.item(1).setHidden(False)


		self.clear_search_txt()
			
		self.do_list_apps(list_app_show_temp)
		item = ui.lw_categories.item(0)
		item.setSelected(True)

	#			  /Cambiar tipo de app			#
	################################################

	################################################
	#			  Busqueda de apps				#

	def search_app(self):
		text = ui.lineEdit.text().lower()

		lista_search = list()
		global list_app_show_temp
		if len(text) != 0 and len(text) > 2:
			ui.lw_categories.clearSelection()
			for app_item in self.lista_app_deb:
				if text in str(app_item.name).lower() or text in str(app_item.description).lower():
					indice = self.lista_app_deb.index(app_item)
					item = self.lista_app_deb[indice]
					lista_search.append(item)
			for app_item in self.lista_app_flatpak:
				if text in str(app_item.name).lower() or text in str(app_item.description).lower():
					indice = self.lista_app_flatpak.index(app_item)
					item = self.lista_app_flatpak[indice]
					lista_search.append(item)
			else:
				list_app_show_temp = lista_search
		
		self.do_list_apps(list_app_show_temp)

	def clear_search_txt(self):
		ui.lineEdit.setText("")

	#			  /Busqueda de apps			   #
	################################################

	################################################
	#				Filtro de apps				#

	def listwidgetclicked(self, item):
		filter = list()
		global lista_global, list_app_show_temp

		filter_mapping = {
			0: ["home"],
			1: ["deepines"],
			2: ["web", "net", "mail", "networking", "network"],
			3: ["sound", "audio", "video", "audiovideo"],
			4: ["graphics", "media"],
			5: ["games", "game"],
			6: ["editors", "office", "productivity"],
			7: ["devel", "shells", "development"],
			8: ["admin", "python", "system", "utility"],
			9: ["other", "education", "science"],

			11: ["installed"]
		}

		index = ui.lw_categories.currentRow()
		filter.extend(filter_mapping.get(index, []))

		if "home" not in filter and "installed" not in filter:
			# TODO: Change the way of filtering apps to a dictionary of lists when loading the store.
			global list_app_show_temp
			list_app_show_temp = self.Get_App_Filter(lista_global, filter)
		elif "installed" in filter:
			list_app_show_temp = installed
		else:
			if selected_type_app == AppType.DEB_PACKAGE:
				list_app_show_temp = self.inicio_apps_deb
			if selected_type_app == AppType.FLATPAK_APP:
				list_app_show_temp = self.inicio_apps_flatpak
		self.change_color_btn_install()
		self.do_list_apps(list_app_show_temp)
		self.clear_search_txt()

	#			   /Filtro de apps				#
	################################################

	################################################
	#				Lista de apps				 #

	#		   Filtrar aplicaciones			 #
	def Get_App_Filter(self, list_app: List[AppInfo], category_filter: List[str]):
		filtered_list = list()
		app_categories = ['web', 'net', 'mail', 'sound', 'audio', 'video', 'audiovideo',
					'graphics', 'office','media', 'games', 'game', 'editors', 'devel', 'shell',
					'admin', 'python', 'development','network', 'networking',
					'productivity', 'system', 'utility']
		if 'deepines' in category_filter:
			for app in self.deepines_app_list:
				for app_data in list_app:
					if app_data.name == app:
						filtered_list.append(app_data)
		else:
			if "other" not in category_filter:
				for app_data in list_app:
					category_app = app_data.category.lower().split("/")
					for filtro_uno in category_app:
						if filtro_uno in category_filter:
							filtered_list.append(app_data)
			else:
				for app_data in list_app:
					if app_data.category.lower() not in app_categories:
						filtered_list.append(app_data)

		return filtered_list

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

	def clear_gridLayout(self):
		while ui.gridLayout.count():
			item = ui.gridLayout.takeAt(0)
			if item is not None:
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					# If the item is another layout, clear it recursively
					layout = item.layout()
					if layout is not None:
						self.clear_sub_layout(layout)
			else:
				break

	def clear_sub_layout(self, layout):
		if layout is not None:
			while layout.count():
				item = layout.takeAt(0)
				if item is not None:
					widget = item.widget()
					if widget is not None:
						widget.deleteLater()
					else:
						sub_layout = item.layout()
						if sub_layout is not None:
							self.clear_sub_layout(sub_layout)

	def do_list_apps(self, lista):
		global lista_inicio, list_app_show_temp
		equal = lista_inicio == list_app_show_temp
		if equal:
			item = ui.lw_categories.item(0)
			item.setSelected(True)

		self.clear_gridLayout()

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
		self.change_color_btn_install()
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

		color=QColor(r, g, b)
		shadow = set_shadow(self, color)
		ui.btn_install.setGraphicsEffect(shadow)

		ui.lbl_list_apps.setText(texto)

	################################################
	#				  Instalacion				 #

	def change_color_btn_install(self):
		if self.show_apps_selected:			
			ui.btn_install.clicked.disconnect(self.window_install)
			ui.btn_install.clicked.connect(self.confirm_app_installation)
			ui.lbl_list_apps.setEnabled(True)
			ui.icon_car.setEnabled(True)
			ui.btn_install.setText(ui.btn_install_review_text)
			ui.btn_install.setStyleSheet(
				"#btn_install{\n"
				"padding: 2px;\n"
				"border-radius: 5px;\n"
				"background-color: rgb(45, 45, 45);\n"
				"border: 2px solid rgb(45, 45, 45);\n"
				"}\n"
				"#btn_install:hover{\n"
				"padding: 2px;\n"
				"color:white;\n"
				"background-color: rgb(65, 159, 217);\n"
				"border: 1px solid rgb(142, 231, 255);\n"
				"border-radius: 5px;\n"
				"}")
			self.show_apps_selected = False

	def change_color_btn_start_install(self):
		ui.btn_install.clicked.disconnect(self.confirm_app_installation)
		ui.btn_install.clicked.connect(self.window_install)
		ui.lbl_list_apps.setEnabled(False)
		ui.icon_car.setEnabled(False)
		ui.btn_install.setText(ui.btn_install_start_text)
		ui.btn_install.setStyleSheet(
			"#btn_install{\n"
			"padding: 2px;\n"
			"border-radius: 5px;\n"
			"background-color: rgb(45, 45, 45);\n"
			"border: 2px solid rgb(151, 255, 0);\n"
			"}\n"
			"#btn_install:hover{\n"
			"padding: 2px;\n"
			"color:white;\n"
			"background-color: rgb(65, 217, 153);\n"
			"border: 1px solid rgb(151, 255, 0);\n"
			"border-radius: 5px;\n"
			"}")

	def confirm_app_installation(self):
		self.change_color_btn_start_install()
		self.show_apps_selected = True
		ui.lw_categories.clearSelection()
		self.do_list_apps(selected_apps)

	def window_install(self):
		self.clear_gridLayout()

		layout = QVBoxLayout()

		self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		layout.addItem(self.verticalSpacer)

		spinner = get_res('Deepines', ext='.gif')
		self.spinner_label = QLabel(self)
		self.spinner = QMovie(spinner)
		self.spinner_label.setMovie(self.spinner)
		self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		max_size = 300
		original_size = self.spinner.scaledSize()
		aspect_ratio = original_size.width() / original_size.height()

		if original_size.width() > original_size.height():
			new_width = max_size
			new_height = new_width / aspect_ratio
		else:
			new_height = max_size
			new_width = new_height * aspect_ratio

		self.spinner.setScaledSize(QSize(int(new_width), int(new_height)))
		self.spinner.start()
		layout.addWidget(self.spinner_label)

		self.process_label = QLabel(ui.process_install_text, self)
		self.process_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.process_label.setStyleSheet("font-size: 22px;")
		self.process_label.setWordWrap(True)
		self.process_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.process_label.adjustSize()
		layout.addWidget(self.process_label)

		self.status_label = QLabel(ui.status_ready_to_install_text, self)
		self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.status_label.setStyleSheet("font-size: 18px;")
		self.status_label.setWordWrap(True)
		self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.status_label.adjustSize()
		layout.addWidget(self.status_label)
		
		self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
		layout.addItem(self.verticalSpacer)

		ui.gridLayout.addLayout(layout, 0, 0)
		ui.btn_install.setText(ui.process_install_text)
		self.status_widgets(False)
		self.start_installation()
	
	def update_status(self, message):
		if self.status_label:
			self.status_label.setText(message)
	
	def change_process_name(self, name):
		self.process_label.setText(name)

	def start_installation(self):
		self.status_label.setText(ui.status_starting_install_text)
		if hasattr(self, 'install_thread') and self.install_thread and self.install_thread.isRunning():			
			self.install_thread.stop()
			self.install_thread.wait()

		self.install_thread = InstallThread(selected_apps)
		self.install_thread.update_signal.connect(self.update_status)
		self.install_thread.name_process_signal.connect(self.change_process_name)
		self.install_thread.finished_signal.connect(self.installation_finished)
		self.install_thread.start()

	def change_spinner(self, new_spinner_name):
		# 1. Detener la animación actual
		self.spinner.stop()

		# 2. Cargar el nuevo GIF
		new_spinner_path = get_res(new_spinner_name, ext='.gif')
		new_spinner = QMovie(new_spinner_path)

		# 3. Establecer el nuevo GIF en el QLabel
		self.spinner_label.setMovie(new_spinner)

		# 4. Iniciar la nueva animación
		new_spinner.start()

		# 5. Actualizar la referencia al spinner actual
		self.spinner = new_spinner

	def installation_finished(self, success):
		if success:
			self.installation_completed()
		else:
			self.process_label.setText(ui.process_install_failed_text)

			self.change_color_btn_install()
			self.change_spinner('strawhats-one-piece')

		self.status_widgets(True)

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
	#		      New installed apps 			   #

	def installation_completed(self):
		global selected_apps, installed, lista_global, uninstalled
		lista_complete = list()
		for app in selected_apps:
			lista_complete.append(app)
			if app.process == ProcessType.INSTALL:
				installed.append(app) # FIXME: Check if it is really installed
				if app.type == AppType.DEB_PACKAGE:
					index = self.lista_app_deb.index(app)
					self.lista_app_deb[index].state = AppState.INSTALLED
					self.lista_app_deb[index].process = ProcessType.UNINSTALL
				else:
					index = self.lista_app_flatpak.index(app)
					self.lista_app_flatpak[index].state = AppState.INSTALLED
					self.lista_app_flatpak[index].process = ProcessType.UNINSTALL

				if app in uninstalled:
					uninstalled.remove(app)
			elif app.process == ProcessType.UNINSTALL:
				installed.remove(app)
				uninstalled.append(app)
				if app.type == AppType.DEB_PACKAGE:
					lista_global = self.lista_app_deb
					index = self.lista_app_deb.index(app)
					self.lista_app_deb[index].state = AppState.UNINSTALLED
					self.lista_app_deb[index].process = ProcessType.INSTALL
					
				else:
					lista_global = self.lista_app_flatpak
					index = self.lista_app_flatpak.index(app)
					self.lista_app_flatpak[index].state = AppState.UNINSTALLED
					self.lista_app_flatpak[index].process = ProcessType.INSTALL

			
		selected_apps = list()
		self.contar_apps()
		self.change_color_btn_install()
		self.do_list_apps(lista_complete)

	#			  /New installed apps 			   #
	################################################

	def maximize(self):
		if self.isMaximized():  # Restauramos al tamaño original
			self.showNormal()
			ui.widget_1.installEventFilter(self)
		else:  # Agrandamos la ventana
			self.showMaximized()
			ui.widget_1.removeEventFilter(self)


################################################
#		   Card para la aplicacion			#


class Card(QFrame):
	def __init__(self, application: list, parent):
		super(Card, self).__init__()
		self.parentWindow = parent
		self.cd = Ui_Frame()
		self.cd.setupUi(self)
		# Establecemos los atributos de la app
		self.application = application
		self.titulo = self.application.name
		self.descripcion = self.application.description
		self.cd.lbl_name_app.setText(self.titulo)
		self.cd.image_app.setToolTip(
			"<p wrap='hard'>{}</p>".format(self.descripcion))
		self.cd.image_app.setWordWrap(True)
		self.setMinimumSize(QSize(tamanio+30, int((tamanio+115)*0.72222)))
		self.setMaximumSize(QSize(tamanio+30, int((tamanio+155)*0.72222)))
		self.cd.image_app.setMinimumSize(QSize(tamanio, int(tamanio*0.72222)))
		if self.application.version:
			self.cd.lbl_version.setText("v: {}".format(self.application.version))

		global installed, uninstalled
		if self.application not in installed:
			state = AppState.DEFAULT
			if self.application in selected_apps:
				state = AppState.SELECTED
		else:
			state = AppState.INSTALLED
			if self.application in selected_apps:
				state = AppState.UNINSTALL
		
		if self.application in uninstalled and self.application in selected_apps:
			state = AppState.SELECTED
		elif self.application in uninstalled:
			state = AppState.UNINSTALLED

		#if self.application not in selected_apps and self.application not in installed:
		self.installEventFilter(self)

		self.update_app_card_status(state)

		# Establecemos la imagen
		if (self.application.type == AppType.DEB_PACKAGE):
			app_banner = QPixmap(self.get_banner_path(self.application.id))
			self.cd.image_app.setPixmap(app_banner)
		if (self.application.type == AppType.FLATPAK_APP):
			# use app id, if not found, then use the alternative app names
			alt_app_name_1 = str(self.application.name).lower().replace(" ", "-")
			alt_app_name_2 = str(self.application.name).lower().replace(" ", "")
			alt_app_name_3 = str(self.application.name).lower().replace(" ", "_")
			alt_app_name_4 = str(self.application.id).split('.')[-1]
			# make unique
			alt_app_names = list(set([alt_app_name_1, alt_app_name_2, alt_app_name_3, alt_app_name_4]))
			app_banner_path = self.get_banner_path(self.application.id, alt_app_names, self.application.icons)
			app_banner = self.fixed_banner_pixmap(app_banner_path)
			app_overlay = QPixmap(get_res('flatpak'))
			app_pixmap = QPixmap(app_banner)
			painter = QPainter(app_pixmap)
			painter.drawPixmap(0, 0, app_overlay)
			painter.end()
			self.cd.image_app.setPixmap(app_pixmap)

		self.cd.lbl_version.clicked.connect(
			lambda: self.select_app())
		self.cd.image_app.clicked.connect(lambda: self.select_app())
		self.cd.lbl_name_app.clicked.connect(
			lambda: self.select_app())
		self.cd.btn_select_app.clicked.connect(lambda: self.select_app())

	def fixed_banner_pixmap(self, banner_path):
		pixmap = QPixmap(banner_path)
		if banner_path.endswith('.png'):
			new_pixmap = QPixmap(324, 234)
			new_pixmap.fill(Qt.transparent)
			painter = QPainter(new_pixmap)
			painter.drawPixmap((324 - pixmap.width()) // 2, (234 - pixmap.height()) // 2, pixmap)
			painter.end()
			pixmap = new_pixmap
		return pixmap

	def eventFilter(self, object, event):
		if event.type() == QEvent.Enter:
			radius = 20
		elif event.type() == QEvent.Leave and not (self.application in selected_apps or self.application in installed or self.application in uninstalled):
			radius = 0
		else:
			return False

		if self.application.state == AppState.SELECTED:
			shadow_color = QColor(0, 255, 255)
		elif self.application.state == AppState.UNINSTALL:
			shadow_color = QColor(234, 93, 41)
		elif self.application.state == AppState.INSTALLED:
			shadow_color = QColor(0, 212, 0)
		elif self.application.state == AppState.UNINSTALLED:
			shadow_color = QColor(238, 81, 56)
		else:
			shadow_color = QColor(255, 255, 255)

		shadow = set_shadow(self, shadow_color,radius)
		self.setGraphicsEffect(shadow)
		return True

	def get_banner_path(self, app_name: str, alt_app_names: List[str] = [], icons: Dict[str, str] = {}) -> str:
		path = get_res(app_name, 'resources/apps')

		if not os.path.exists(path):
			if alt_app_names: # means flatpak app
				for alt_app_name in alt_app_names:
					if alt_app_name != app_name:
						alt_res_path = get_res(alt_app_name, 'resources/apps')
						if os.path.exists(alt_res_path):
							return alt_res_path
				else:
					png_path = get_res(app_name, 'resources/apps', ext='.png')
					if os.path.exists(png_path):
						return png_path

					# use "cached" value from icons
					cached_icon_names = icons.get('cached')
					if cached_icon_names is not None:
						for cached_icon_name in cached_icon_names:
							remote_icon_path = get_res(cached_icon_name, 'resources/apps', ext='')
							if os.path.exists(remote_icon_path):
								return remote_icon_path

							flatpak_path = '/var/lib/flatpak/appstream/flathub/x86_64/active/icons/flatpak/{}x{}/' + cached_icon_name
							for size in ['128', '64']:
								flatpak_path = flatpak_path.format(size, size)
								if os.path.exists(flatpak_path):
									return flatpak_path

					# try to download from "remote" url
					remote_icon_urls = icons.get('remote')
					if remote_icon_urls is not None:
						for remote_icon_url in remote_icon_urls:
							remote_icon_path = get_res(app_name, 'resources/apps', ext='.png')
							try:
								print(f'Downloading icon from: {remote_icon_url}')
								PNG_BANNER_REMOTE = get_dl(remote_icon_url)
								status_code = PNG_BANNER_REMOTE.status_code
								if status_code == 200:
									with open(remote_icon_path, 'wb') as f:
										f.write(PNG_BANNER_REMOTE.content)
									return remote_icon_path
							except Exception as e:
								print(f'Error downloading icon: {e}')

			# if not found, use the default image
			path = get_res('no-img', 'resources/apps')

		return path

	def select_app(self):
		global lista_global, selected_apps, installed

		lista_global_temp = lista_global
		if (self.application.type == AppType.DEB_PACKAGE):
			lista_global = self.parentWindow.lista_app_deb
		if (self.application.type == AppType.FLATPAK_APP):
			lista_global = self.parentWindow.lista_app_flatpak
		indice = lista_global.index(self.application)

		if self.application not in selected_apps and self.application not in installed:
			selected_apps.append(self.application)
			new_state = AppState.SELECTED
		elif self.application not in selected_apps and self.application in installed:
			selected_apps.append(self.application)
			new_state = AppState.UNINSTALL
		else:
			selected_apps.remove(self.application)
			if self.application not in installed:
				new_state = AppState.DEFAULT
			else:
				new_state = AppState.INSTALLED
		self.installEventFilter(self)

		lista_global[indice].state = new_state
		lista_global = lista_global_temp

		self.update_app_card_status(new_state)

		self.parentWindow.contar_apps()

	def update_app_card_status(self, state: AppState):
		color_map = {
			AppState.SELECTED: (0, 255, 255, "#00bbc8", ui.selected_to_install_app_text),
			AppState.UNINSTALL: (234, 93, 41, "#ea4329", ui.uninstall_app_text),
			AppState.INSTALLED: (0, 212, 0, "#009800", ui.selected_installed_app_text),
			AppState.UNINSTALLED: (238, 81, 56, "#d54000", ui.uninstalled_app_text),
			AppState.DEFAULT: (30, 30, 30, "transparent", ui.select_app_text)
		}

		r, g, b, border_color, btn_text = color_map.get(state, color_map[AppState.DEFAULT])

		text_color = "#000" if state == AppState.SELECTED else "#fff"

		btn_select_app_style = ("QPushButton#btn_select_app{"
					"color: " + text_color + ";"
					"background-color: rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ");"
					"margin: 5px 10px;"
					"border-width: 0px;"
					"border-radius: 10px;"
					"}")

		self.cd.btn_select_app.setText(btn_text)

		self.setStyleSheet("#Frame{"
						   "background-color: #2d2d2d;"
						   "border-radius: 10px;"
						   "margin: 10px;"
						   "border-color: " + border_color + ";"
						   "border-width: 1px;"
						   "border-style: solid;"
						   "}" + btn_select_app_style)

		color = QColor(r, g, b)
		shadow = set_shadow(self, color, 20)
		self.setGraphicsEffect(shadow)


#		   /Card para la aplicacion		   #
################################################

def set_shadow(widget, color: QColor, radius=10):
	shadow = QGraphicsDropShadowEffect(widget,
									   color=color,
									   blurRadius=radius,
									   offset=QPointF(0, 0)
									   )
	shadow.setXOffset(0)
	shadow.setYOffset(0)
	return shadow


def center_window(widget):
	# Obtener desktop de la instancia QApplication actual
	app = QApplication.instance()
	if app is None:
		return
	desktop: QDesktopWidget = app.desktop() # type: ignore

	# Obtener la pantalla donde se encuentra el cursor
	screen = QDesktopWidget().screenNumber(desktop.cursor().pos())
	screen_rect = desktop.screenGeometry(screen)

	# Calcular el centro de la pantalla
	screen_center = screen_rect.center()

	# Calcular el centro del widget
	widget_center = widget.rect().center()

	# Mover el widget al centro de la pantalla
	widget.move(screen_center - widget_center)

class LoaderThread(QThread):
	progress = pyqtSignal(str)
	finished = pyqtSignal()

	def __init__(self, parent):
		super().__init__()
		self.parent = parent

	def run(self):
		global list_app_deepines, list_app_deb, \
		list_app_flatpak, installed
		self.progress.emit(self.parent.fetchingString)
		list_app_deepines = setup.Get_App_Deepines()
		list_app_exclude = setup.Get_App_Exclude()
		self.progress.emit(self.parent.initializingString)
		list_app_deb = fetch_list_app_deb(list_app_exclude)
		list_app_flatpak = app_list_flatpak()
		self.progress.emit(self.parent.finalizingString)
		installed = setup.get_installed_apps(list_app_deb, list_app_flatpak)
		setup.download_control()
		self.finished.emit()

class LoadingScreen(QMainWindow, EventsMixin):
	def __init__(self):
		super().__init__()
		self.setWindowFlags(QtCore.FramelessWindowHint)
		self.setStyleSheet("background-color: rgba(30, 30, 30, 200); color: #b5c5d1;")

		self.drag_position = None

		layout = QVBoxLayout()
		self.label_title = QLabel(self)
		self.label_title.setText(self.windowTitle())
		self.label_title.setAlignment(QtCore.AlignCenter)
		self.label_title.setStyleSheet("font-size: 24px;")

		spinner = get_res('Deepines', ext='.gif')
		self.spinner_label = QLabel(self)
		self.spinner = QMovie(spinner)
		self.spinner_label.setMovie(self.spinner)
		self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		max_size = 300
		original_size = self.spinner.scaledSize()
		aspect_ratio = original_size.width() / original_size.height()

		if original_size.width() > original_size.height():
			new_width = max_size
			new_height = new_width / aspect_ratio
		else:
			new_height = max_size
			new_width = new_height * aspect_ratio

		self.spinner.setScaledSize(QSize(int(new_width), int(new_height)))
		self.spinner.start()

		self.progress_label = QLabel(self)
		self.progress_label.setAlignment(QtCore.AlignCenter)
		self.progress_label.setStyleSheet("font-size: 20px;")

		layout.addWidget(self.label_title)
		layout.addWidget(self.spinner_label)
		layout.addWidget(self.progress_label)

		container = QWidget()
		container.setLayout(layout)
		#container.setStyleSheet("background-color: rgb(30, 30, 30);")
		self.setCentralWidget(container)

		self.retranslateUi()

		self.loader_thread = LoaderThread(self)
		self.loader_thread.progress.connect(self.update_progress)
		self.loader_thread.finished.connect(self.on_finish)
		self.loader_thread.start()

	def retranslateUi(self):
		_translate = QCoreApplication.translate
		self.setWindowTitle(_translate("LoadingScreen", "Loading..."))
		self.label_title.setText(_translate("Ui_MainWindow", "Deepines Store"))
		self.startingString = _translate("LoadingScreen", "Starting...")
		self.progress_label.setText(self.startingString)
		self.fetchingString = _translate("LoadingScreen", "Fetching files...")
		self.initializingString = _translate("LoadingScreen", "Initializing components...")
		self.finalizingString = _translate("LoadingScreen", "Finalizing setup...")

	def update_progress(self, message):
		self.progress_label.setText(message)

	def on_finish(self):
		self.main_window = StoreMWindow()
		self.main_window.calcular_anchos()
		set_blur(self.main_window)
		self.main_window.show()
		self.close()

def run_gui():
	app = QApplication(sys.argv)
	app.setWindowIcon(get_app_icon())

	translator = QTranslator()
	translator.load(QLocale(), "", "", get_res('', 'translations', ''), ".qm")
	app.installTranslator(translator)

	loading_screen = LoadingScreen()
	loading_screen.show()
	center_window(loading_screen)

	global width, height
	screen_rect = app.desktop().screenGeometry()
	width, height = screen_rect.width(), screen_rect.height()
	sys.exit(app.exec_())