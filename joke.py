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
    def __init__(self, main):
        super(Ui_Form, self).__init__()
        self.main = main
        self.main.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.main.setEnabled(False)
        self.resize(600, 300)
        icon = QIcon()
        icon.addPixmap(QPixmap("./resources/deepines_logo_beta.svg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Line edit para mostrat texto
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)
        self.center()



    def instalar(self):
        self.main.setEnabled(False)
        self.boton.setEnabled(False)
        self.boton_install.setEnabled(False)
        self.obj = External(self.lista)
        self.thread = QThread()
        self.obj.start.connect(self.comenzar)
        self.obj.moveToThread(self.thread)
        self.obj.error.connect(self.error)
        self.obj.update.connect(self.update)
        self.obj.finish.connect(self.finalizar)
        self.obj.complete.connect(self.complete)
        self.thread.started.connect(self.obj.run)
        #thread.finished.connect(thread.quit())
        self.thread.start()


    def complete(self):
        self.main.setEnabled(True)
        self.boton.setEnabled(True)
        self.thread.quit()
        self.plainTextEdit.insertPlainText("\nTodo ha finalizado correctamente.")


    def comenzar(self, elemento):
        self.plainTextEdit.insertPlainText("\nInstalando {}".format(elemento))


    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())