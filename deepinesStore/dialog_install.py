# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QTextCursor

from deepinesStore.app_info import AppType
from deepinesStore.install_thread import External, Code
from deepinesStore.uninstall_thread import ExternalUninstall
from deepinesStore.core import ProcessType

class Ui_DialogInstall(QtWidgets.QWidget):
	def __init__(self, main, list):
		super(Ui_DialogInstall, self).__init__()
		self.main = main
		self.list = list
		self.resize(600, 300)
		self.retranslateUi(self)

		self.gridLayout = QtWidgets.QGridLayout(self)
		self.btn_d_install = QtWidgets.QPushButton(self)
		self.gridLayout.addWidget(self.btn_d_install, 1, 0, 1, 1)
		self.btn_d = QtWidgets.QPushButton(self)
		self.btn_d.setText(self.close_text)
		self.gridLayout.addWidget(self.btn_d, 1, 1, 1, 1)
		# Line edit to display text
		self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
		self.plainTextEdit.setReadOnly(True)
		# self.plainTextEdit.setTextInteractionFlags(Qt.NoTextInteraction)
		self.plainTextEdit.setCenterOnScroll(True)
		self.plainTextEdit.setObjectName("plainTextEdit")
		self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)
		self.center()
		self.btn_d.clicked.connect(self.close)
		# FIXME: Don't install 1 app
		# maybe get state of first app 
		try:
			count_apps = len(list)
			self.process_type = ProcessType.INSTALL
			self.btn_d_install.setText(self.install_text)
		except:
			self.process_type = ProcessType.UNINSTALL

		if self.process_type == ProcessType.INSTALL:
			if count_apps != 1:
				preview_installed = self.multi_apps_to_install_text
			else:
				preview_installed = self.single_app_to_install_text

			self.plainTextEdit.insertPlainText(
				preview_installed.format(app_count=count_apps))
			for item in self.list:
				if item.type == AppType.DEB_PACKAGE:
					format = '.deb'
				if item.type == AppType.FLATPAK_APP:
					format = 'flatpak'
				self.plainTextEdit.insertPlainText(f"\n{item.name}  -  {format}")
			self.btn_d_install.clicked.connect(self.p_install)
		else:
			self.btn_d_install.setText(self.uninstall_text)
			self.btn_d_install.clicked.connect(self.p_uninstall)
			self.plainTextEdit.insertPlainText(self.app_to_uninstall_text.format(item=self.list.name))
		self.plainTextEdit.insertPlainText(self.warning_text)

	def p_uninstall(self):
		self.main.setVisible(False)
		self.btn_d.setEnabled(False)
		self.btn_d_install.setEnabled(False)
		self.obj = ExternalUninstall(self.list)
		self.thread = QThread()
		self.obj.start.connect(self.p_start)
		self.obj.moveToThread(self.thread)
		self.obj.error.connect(self.p_error)
		self.obj.progress.connect(self.p_progress)
		self.obj.update.connect(self.p_update)
		self.obj.finish.connect(self.p_finish)
		self.obj.complete.connect(self.complete)
		self.thread.started.connect(self.obj.run)
		# thread.finished.connect(thread.quit())
		self.thread.start()

	def p_install(self):
		self.main.setVisible(False)
		self.btn_d.setEnabled(False)
		self.btn_d_install.setEnabled(False)
		self.obj = External(self.list)
		self.thread = QThread()
		self.obj.start.connect(self.p_start)
		self.obj.moveToThread(self.thread)
		self.obj.error.connect(self.p_error)
		self.obj.progress.connect(self.p_progress)
		self.obj.update.connect(self.p_update)
		self.obj.finish.connect(self.p_finish)
		self.obj.complete.connect(self.complete)
		self.thread.started.connect(self.obj.run)
		# thread.finished.connect(thread.quit())
		self.thread.start()

	def activate_win(self):
		self.main.setVisible(True)
		self.btn_d.setEnabled(True)
		self.activateWindow()

	def complete(self):
		self.plainTextEdit.insertPlainText(self.all_processes_completed_text)
		self.plainTextEdit.moveCursor(QTextCursor.End)
		if self.process_type == ProcessType.INSTALL:
			self.main.installation_completed()
		else:
			self.main.uninstallation_completed()
		self.activate_win()
		self.thread.quit()

	def p_start(self, item):
		if self.process_type == ProcessType.INSTALL:
			self.plainTextEdit.insertPlainText(self.installing_text.format(item=item))
		else:
			self.plainTextEdit.insertPlainText(self.uninstalling_text.format(item=self.list.name))

	def p_progress(self, item):
		self.plainTextEdit.insertPlainText(f"{item}")
		self.plainTextEdit.moveCursor(QTextCursor.End)

	def p_finish(self, item):
		if self.process_type == ProcessType.INSTALL:
			self.plainTextEdit.insertPlainText(self.finish_install_text.format(item=item))
		else:
			self.plainTextEdit.insertPlainText(self.finish_uninstall_text.format(item=self.list.name))
		self.plainTextEdit.moveCursor(QTextCursor.End)

	def p_error(self, code: Code):
		if code == Code.UNHANDLED_ERROR:
			msg = (self.error_unhandled_text)
		if code == Code.NO_INTERNET:
			msg = (self.error_network_text)
		if code == Code.FAIL_DEPS:
			msg = (self.error_dependencies_text)
		if code == Code.APT_LOCKED:
			msg = (self.error_apt_text)

		self.btn_d_install.setText(self.retry_text)
		self.plainTextEdit.insertPlainText(msg)
		self.btn_d_install.setEnabled(True)
		self.btn_d.setEnabled(True)
		self.activateWindow()
		self.thread.quit()
		# self.activate_win()

	def p_update(self):
		self.plainTextEdit.insertPlainText(self.updating_database_text)

	def center(self):
		frameGm = self.frameGeometry()
		screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
		centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

	def __tr(self, txt, disambiguation=None, n=-1):
		from deepinesStore.core import tr
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, DialogInstall):
		DialogInstall.setWindowTitle(self.__tr("Installation process - Deepines Store"))
		self.single_app_to_install_text = self.__tr("{app_count} app has been selected for installation:\n")
		self.multi_apps_to_install_text = self.__tr("{app_count} apps have been selected for installation:\n")
		self.app_to_uninstall_text = self.__tr("App to uninstall: {item}")
		self.uninstall_text = self.__tr("Uninstall")
		self.install_text = self.__tr("Install")
		self.retry_text = self.__tr("Retry")
		self.close_text = self.__tr("Close")
		self.warning_text = self.__tr("\n\nWarning: do not close the window, interrupting the process may damage your system.\n")
		self.all_processes_completed_text = self.__tr("\nAll processes have been completed.\n")
		self.installing_text = self.__tr("\nInstalling {item}\n")
		self.uninstalling_text = self.__tr("\nUninstalling {item}\n")
		self.finish_install_text = self.__tr("\nThe installation of {item} is finished.\n")
		self.finish_uninstall_text = self.__tr("\nThe uninstallation of {item} is finished.\n")
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