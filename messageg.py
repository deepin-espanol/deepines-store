# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/message.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 100)
        Dialog.setMinimumSize(QtCore.QSize(300, 0))
        Dialog.setMaximumSize(QtCore.QSize(300, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setStyleSheet("#frame{\n"
"    background-color: rgba(16, 16, 16, 140);\n"
"    border-radius: 10px;\n"
"    border: 2px solid rgb(65, 159, 217);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_close = QtWidgets.QPushButton(self.frame)
        self.btn_close.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_close.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_close.setStyleSheet("#btn_close{\n"
"    background-color: red;\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"}\n"
"#btn_close:hover{\n"
"    background-color: rgba(255, 0, 0, 180);\n"
"    color: black;\n"
"    border-radius: 5px;\n"
"}")
        self.btn_close.setObjectName("btn_close")
        self.gridLayout_2.addWidget(self.btn_close, 0, 4, 1, 1)
        self.lbl_status = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.lbl_status.setFont(font)
        self.lbl_status.setObjectName("lbl_status")
        self.gridLayout_2.addWidget(self.lbl_status, 0, 2, 1, 1)
        self.lbl_text = QtWidgets.QLabel(self.frame)
        self.lbl_text.setStyleSheet("font: italic 12pt \"Noto Sans\";")
        self.lbl_text.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_text.setWordWrap(True)
        self.lbl_text.setObjectName("lbl_text")
        self.gridLayout_2.addWidget(self.lbl_text, 1, 0, 1, 5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.lbl_icono = QtWidgets.QLabel(self.frame)
        self.lbl_icono.setMinimumSize(QtCore.QSize(30, 30))
        self.lbl_icono.setMaximumSize(QtCore.QSize(30, 30))
        self.lbl_icono.setText("")
        self.lbl_icono.setPixmap(QtGui.QPixmap("./resources/information-button.svg"))
        self.lbl_icono.setScaledContents(True)
        self.lbl_icono.setObjectName("lbl_icono")
        self.gridLayout_2.addWidget(self.lbl_icono, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_close.setText(_translate("Dialog", "X"))
        self.lbl_status.setText(_translate("Dialog", "Instalando"))
        self.lbl_text.setText(_translate("Dialog", "Se instalara <nombre-aplicacion>"))
