# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/dialog_install.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QIcon
from install_thread import External

class Ui_Form(QtWidgets.QWidget):
    def __init__(self, main, lista):
        super(Ui_Form, self).__init__()
        self.main = main
        self.lista = lista
        self.main.setEnabled(False)
        self.resize(600, 300)
        icon = QIcon()
        icon.addPixmap(QPixmap("./resources/deepines_logo_beta.svg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.boton_install = QtWidgets.QPushButton(self)
        self.boton_install.setText("Instalar")
        self.boton_install.setObjectName("boton_install")
        self.gridLayout.addWidget(self.boton_install, 1, 0, 1, 1)
        self.boton = QtWidgets.QPushButton(self)
        self.boton.setObjectName("boton")
        self.boton.setText("Cerrar")
        self.gridLayout.addWidget(self.boton, 1, 1, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)
        self.center()

        self.boton.clicked.connect(self.close)
        self.boton_install.clicked.connect(self.instalar)

        # Line edit para mostrat texto
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        count_apps = len(lista)
        if count_apps != 1:
            articulo = "aplicaciones"
        else:
            articulo = "aplicacion"

        self.plainTextEdit.insertPlainText("Al comenzar la instalación, esta no"
            " podra detenerse, si por algun motivo se cancela, puede producir un error"
            " catastrofico y es muy probable que el computador explote."
            " Esta seguro que desea instalar??\n\n")
        self.plainTextEdit.insertPlainText(
            "Se han seleccionado {} {} para instalar \n".format(count_apps, articulo))
        for item in self.lista:
            self.plainTextEdit.insertPlainText("{}\n".format(item))


    def instalar(self):
        self.boton.setEnabled(False)
        self.boton_install.setEnabled(False)
        self.obj = External(self.lista)
        self.thread = QThread()
        self.obj.start.connect(self.comenzar)
        self.obj.moveToThread(self.thread)
        self.obj.finish.connect(self.finalizar)
        self.obj.complete.connect(self.complete)
        self.thread.started.connect(self.obj.run)
        #thread.finished.connect(thread.quit())
        self.thread.start()


    def complete(self):
        self.main.setEnabled(True)
        self.boton.setEnabled(True)
        self.thread.quit()

    def comenzar(self, elemento):
        self.plainTextEdit.insertPlainText("Instalando {} \n".format(elemento))

    def finalizar(self):
        self.plainTextEdit.insertPlainText("Se ha instalado correctamente\n")

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())