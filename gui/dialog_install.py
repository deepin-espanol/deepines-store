# -*- coding: utf-8 -*-

# UI Source 'gui/dialog_install.ui'

from PyQt5 import QtCore, QtWidgets


class Ui_DialogInstall(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(547, 331)
		self.gridLayout = QtWidgets.QGridLayout(Form)
		self.gridLayout.setObjectName("gridLayout")
		self.boton_install = QtWidgets.QPushButton(Form)
		self.boton_install.setObjectName("boton_install")
		self.gridLayout.addWidget(self.boton_install, 1, 0, 1, 1)
		self.boton = QtWidgets.QPushButton(Form)
		self.boton.setObjectName("boton")
		self.gridLayout.addWidget(self.boton, 1, 1, 1, 1)
		self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
		self.plainTextEdit.setReadOnly(True)
		self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.plainTextEdit.setCenterOnScroll(True)
		self.plainTextEdit.setObjectName("plainTextEdit")
		self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def __tr(self, txt, disambiguation=None, n=-1):
		return QtCore.QCoreApplication.translate(self.__class__.__name__, txt, disambiguation, n)

	def retranslateUi(self, Form):
		Form.setWindowTitle(self.__tr("Form"))
		self.boton_install.setText(self.__tr("Install"))
		self.boton.setText(self.__tr("Close"))
