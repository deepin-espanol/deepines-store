# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/dialog_install.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets as W
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
import subprocess


class Ui_Form(W.QWidget):
    def __init__(self, main, lista):
        super(Ui_Form, self).__init__()
        self.main = main
        self.lista = lista
        self.resize(600, 300)
        icon = QIcon()
        icon.addPixmap(QPixmap("./resources/deepines_logo_beta.svg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.plainTextEdit = W.QPlainTextEdit(self)
        self.center()

        # Layout principal
        self.layoutPrincipal = W.QGridLayout()

        self.setLayout(self.layoutPrincipal)

        # Line edit para capturar texto
        self.plainTextEdit.setObjectName("plainTextEdit")
        count_apps = len(lista)
        if count_apps != 1:
            articulo = "aplicaciones"
        else:
            articulo = "aplicacion"

        self.plainTextEdit.insertPlainText(
            "Se comenzara la instalacion de {} {} \n".format(count_apps, articulo))
        self.plainTextEdit.setReadOnly(True)
        

        # Botón para devolver el contenido
        self.boton = W.QPushButton("Cerrar")
        self.boton.setEnabled(False)

        # Añadiendo widgets
        self.layoutPrincipal.addWidget(self.plainTextEdit, 0, 0, 2, 5)
        self.layoutPrincipal.addWidget(self.boton, 3, 2, 1, 3)

        self.instalar()

    def instalar(self):
        for elemento in self.lista:
            self.plainTextEdit.insertPlainText("Instalando {} \n".format(elemento))
            subprocess.call('gksudo apt install update', shell=True)
            self.plainTextEdit.insertPlainText("...\n")
            self.plainTextEdit.insertPlainText("Se ha instalado correctamente\n")

    def center(self):
        frameGm = self.frameGeometry()
        screen = W.QApplication.desktop().screenNumber(W.QApplication.desktop().cursor().pos())
        centerPoint = W.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())