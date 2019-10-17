# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/dialog_install.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets as W
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QIcon
from install_thread import External

class Ui_Form(W.QWidget):
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
        self.plainTextEdit = W.QPlainTextEdit(self)
        self.center()

        # Layout principal
        self.layoutPrincipal = W.QGridLayout()

        self.setLayout(self.layoutPrincipal)

        # Line edit para mostrat texto
        self.plainTextEdit.setObjectName("plainTextEdit")
        count_apps = len(lista)
        if count_apps != 1:
            articulo = "aplicaciones"
        else:
            articulo = "aplicacion"

        self.plainTextEdit.insertPlainText(
            "Se comenzara la instalacion de {} {} \n".format(count_apps, articulo))
        self.plainTextEdit.setReadOnly(True)
        

        self.boton = W.QPushButton("Cerrar")
        self.boton.setEnabled(False)
        self.boton.clicked.connect(self.close)

        # Añadiendo widgets
        self.layoutPrincipal.addWidget(self.plainTextEdit, 0, 0, 2, 5)
        self.layoutPrincipal.addWidget(self.boton, 3, 2, 1, 3)

        self.instalar()

    def instalar(self):
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
        screen = W.QApplication.desktop().screenNumber(W.QApplication.desktop().cursor().pos())
        centerPoint = W.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())