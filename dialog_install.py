# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/dialog_install.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QIcon, QTextCursor
from install_thread import External
from os.path import join, abspath, dirname

class Ui_Form(QtWidgets.QWidget):
    def __init__(self, main, lista):
        super(Ui_Form, self).__init__()
        ruta_logo = abspath(join(dirname(__file__), 'resources', 'deepines.svg'))
        self.main = main
        self.lista = lista
        self.resize(600, 300)
        icon = QIcon()
        icon.addPixmap(QPixmap(ruta_logo),QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Deepines Store - Instalacion de apps")
        #self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

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
        # Line edit para mostrat texto
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)
        self.center()

        self.boton.clicked.connect(self.close)
        self.boton_install.clicked.connect(self.instalar)

        count_apps = len(lista)

        if count_apps != 1:
            articulo = "aplicaciones"
            haber = "han"
        else:
            articulo = "aplicación"
            haber = "ha"

        self.plainTextEdit.insertPlainText(
            "Se {} seleccionado {} {} para instalar \n".format(haber, count_apps, articulo))
        for item in self.lista:
            self.plainTextEdit.insertPlainText("\n{}".format(item))
   
        self.plainTextEdit.insertPlainText("\n\nAdvertencia: no cierre la ventana, "
            "interrumpir la instalación puede dañar su sistema.\n")

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
        #thread.finished.connect(thread.quit())
        self.thread.start()

    def ventana(self):
        self.main.setVisible(True)
        self.boton.setEnabled(True)
        self.activateWindow()

    def complete(self):
        self.plainTextEdit.insertPlainText(
            "\nSe han terminado todos los procesos.\n")
        self.plainTextEdit.moveCursor(QTextCursor.End)
        self.main.instalacion_completada()
        self.ventana()
        self.thread.quit()

    def comenzar(self, elemento):
        self.plainTextEdit.insertPlainText("\nInstalando {}".format(elemento))

    def progreso(self, elemento):
        self.plainTextEdit.insertPlainText("{}".format(elemento))
        self.plainTextEdit.moveCursor(QTextCursor.End)

    def finalizar(self, elemento):
        self.plainTextEdit.insertPlainText(
            "\nSe han terminado de instalar {}.\n".format(elemento))
        self.plainTextEdit.moveCursor(QTextCursor.End)

    def error(self):
        self.plainTextEdit.insertPlainText("\n\nHa ocurrido un error, intentelo"
            " nuevamente.\n"
            "Si el problema persiste, comuniquese con el administrador.\n")
        self.ventana()

    def update(self):
        self.plainTextEdit.insertPlainText("\nSe esta actualizando la base de datos.\n\n")

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())