# -*- coding: utf-8 -*-

# UI Source 'gui/dialog_install.ui'

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon, QTextCursor
from deepinesStore.maing import get_res
from deepinesStore.install_thread import External
from deepinesStore.notification import notification


class Ui_DialogInstall(QtWidgets.QWidget):
	def __init__(self, main, lista):
		super(Ui_DialogInstall, self).__init__()
		svg_logo = get_res('deepines')
		self.main = main
		self.lista = lista
		self.resize(600, 300)
		icon = QIcon()
		icon.addPixmap(QPixmap(svg_logo), QIcon.Normal, QIcon.Off)
		self.retranslateUi(self)
		self.setWindowIcon(icon)
		#self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

		self.gridLayout = QtWidgets.QGridLayout(self)
		self.gridLayout.setObjectName("gridLayout")
		self.boton_install = QtWidgets.QPushButton(self)
		self.boton_install.setText(self.install_text)
		self.boton_install.setObjectName("boton_install")
		self.gridLayout.addWidget(self.boton_install, 1, 0, 1, 1)
		self.boton = QtWidgets.QPushButton(self)
		self.boton.setObjectName("boton")
		self.boton.setText(self.close_text)
		self.gridLayout.addWidget(self.boton, 1, 1, 1, 1)
		# Line edit para mostrar texto
		self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
		self.plainTextEdit.setReadOnly(True)
		# self.plainTextEdit.setTextInteractionFlags(Qt.NoTextInteraction)
		self.plainTextEdit.setCenterOnScroll(True)
		self.plainTextEdit.setObjectName("plainTextEdit")
		self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)
		self.center()

		self.boton.clicked.connect(self.close)
		self.boton_install.clicked.connect(self.instalar)

		count_apps = len(lista)

		if count_apps != 1:
			preview_installed = self.multi_apps_to_install_text
		else:
			preview_installed = self.single_app_to_install_text

		self.plainTextEdit.insertPlainText(
			preview_installed.format(app_count=count_apps))
		for item in self.lista:
			self.plainTextEdit.insertPlainText("\n{}".format(item))

		self.plainTextEdit.insertPlainText(self.warning_text)

	def instalar(self):
		self.main.setVisible(False)
		self.boton.setEnabled(False)
		self.boton_install.setEnabled(False)
		self.obj = External(self.lista)
		self.thread = QThread()
		self.obj.start.connect(self.comenzar)
		self.obj.moveToThread(self.thread)
		self.obj.error.connect(self.error)
		self.obj.progress.connect(self.progreso)
		self.obj.update.connect(self.update)
		self.obj.finish.connect(self.finalizar)
		self.obj.complete.connect(self.complete)
		self.thread.started.connect(self.obj.run)
		# thread.finished.connect(thread.quit())
		self.thread.start()

	def ventana(self):
		self.main.setVisible(True)
		self.boton.setEnabled(True)
		self.activateWindow()

	def complete(self):
		self.plainTextEdit.insertPlainText(self.all_processes_completed_text)
		self.plainTextEdit.moveCursor(QTextCursor.End)
		self.main.instalacion_completada()
		self.ventana()
		self.thread.quit()

	def comenzar(self, elemento):
		self.plainTextEdit.insertPlainText(
			self.installing_text.format(item=elemento))

	def progreso(self, elemento):
		self.plainTextEdit.insertPlainText(f"{elemento}")
		self.plainTextEdit.moveCursor(QTextCursor.End)

	def finalizar(self, elemento):
		#message = "Se han terminado de instalar {}.\n".format(elemento)
		# notification(message)
		self.plainTextEdit.insertPlainText(
			self.finish_install_text.format(item=elemento))
		self.plainTextEdit.moveCursor(QTextCursor.End)

	def error(self, codigo_error):
		if codigo_error == 1:  # Excepcion no controlada
			mensaje = (self.error_unhandled_text)
		if codigo_error == 2:  # Error de red
			mensaje = (self.error_network_text)
		if codigo_error == 3:  # Error dependencias incumplidas
			mensaje = (self.error_dependencies_text)
		if codigo_error == 4:  # Error de apt
			mensaje = (self.error_apt_text)

		self.boton_install.setText(self.retry_text)
		self.plainTextEdit.insertPlainText(mensaje)
		self.boton_install.setEnabled(True)
		self.boton.setEnabled(True)
		self.activateWindow()
		self.thread.quit()
		# self.ventana()

	def update(self):
		self.plainTextEdit.insertPlainText(self.updating_database_text)

	def center(self):
		frameGm = self.frameGeometry()
		screen = QtWidgets.QApplication.desktop().screenNumber(
			QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def __tr(self, txt, disambiguation=None, n=-1):
	  return QCoreApplication.translate(self.__class__.__name__, txt, disambiguation, n)

	def retranslateUi(self, DialogInstall):
		DialogInstall.setWindowTitle(self.__tr("Installation process - Deepines Store"))
		self.single_app_to_install_text = self.__tr("{app_count} app has been selected for installation:\n")
		self.multi_apps_to_install_text = self.__tr("{app_count} apps have been selected for installation:\n")
		self.install_text = self.__tr("Install")
		self.retry_text = self.__tr("Retry")
		self.close_text = self.__tr("Close")
		self.warning_text = self.__tr("\n\nWarning: do not close the window, interrupting the installation may damage your system.\n")
		self.all_processes_completed_text = self.__tr("\nAll processes have been completed.\n")
		self.installing_text = self.__tr("\nInstalling {item}\n")
		self.finish_install_text = self.__tr("\nThe installation of {item} is finished.\n")
		self.error_unhandled_text = self.__tr("\n\nAn error has occurred, please try again.\n"
											   "If the problem persists, contact the administrator.\n")
		self.error_network_text = self.__tr("\n\nThe network connection has failed and the installation has not been completed.\n"
											 "Check that your computer is connected to the Internet and click Retry.\n"
											 "If the problem persists, send a report to t.me/deepinenespanol.\n")
		self.error_dependencies_text = self.__tr("\n\nOne or more apps could not be installed because\n"
												  "they depend on other packages that cannot be installed.\n\n"
												  "You can look for help in our forum at deepinenespanol.org/comunidad\n"
												  "or in our Telegram group t.me/deepinenespanol.")
		self.error_apt_text = self.__tr("\n\nThe installation system is locked by \n"
										 "another installation or upgrade process, \n"
										 "wait until it finishes and click Retry. \n"
										 "If you use Synaptic, make sure it is closed.")
		self.updating_database_text = self.__tr("\nThe database is being updated.\n\n")