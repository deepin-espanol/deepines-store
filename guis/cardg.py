# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/card.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(171, 217)
        Frame.setMinimumSize(QtCore.QSize(171, 0))
        Frame.setMaximumSize(QtCore.QSize(171, 16777215))
        Frame.setStyleSheet("#Frame{\n"
"    background-color: transparent;\n"
"}\n"
"QToolTip {\n"
"    border: 2px solid #419fd9;\n"
"    border-radius: 4px;\n"
"    padding: 2px;\n"
"    font-size: 12px;\n"
"    color: white;\n"
"    background-color: transparent;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_card = QtWidgets.QLabel(Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_card.sizePolicy().hasHeightForWidth())
        self.image_card.setSizePolicy(sizePolicy)
        self.image_card.setMinimumSize(QtCore.QSize(153, 135))
        self.image_card.setMaximumSize(QtCore.QSize(153, 135))
        self.image_card.setStyleSheet("background-color: rgb(45, 45, 45);\n"
"border-radius: 15px;")
        self.image_card.setText("")
        self.image_card.setPixmap(QtGui.QPixmap("../resources/apps/4kslideshowmaker.svg"))
        self.image_card.setScaledContents(True)
        self.image_card.setAlignment(QtCore.Qt.AlignCenter)
        self.image_card.setObjectName("image_card")
        self.verticalLayout.addWidget(self.image_card)
        self.label_titulo_card = QtWidgets.QLabel(Frame)
        self.label_titulo_card.setStyleSheet("color: white;\n"
"background-color: transparent;")
        self.label_titulo_card.setText("")
        self.label_titulo_card.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo_card.setObjectName("label_titulo_card")
        self.verticalLayout.addWidget(self.label_titulo_card)
        self.boton_ver_card = QtWidgets.QPushButton(Frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setItalic(False)
        self.boton_ver_card.setFont(font)
        self.boton_ver_card.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.boton_ver_card.setStyleSheet("#boton_ver_card{\n"
"padding: 7px;\n"
"color: white;\n"
"border-radius: 5px;\n"
"    background-color: rgb(45, 45, 45);\n"
"}\n"
"#boton_ver_card:hover{\n"
"border: 1px solid rgb(142, 231, 255);\n"
"padding: 7px;\n"
"color:white;\n"
"background-color: rgb(65, 159, 217);\n"
"border-radius: 5px;\n"
"}")
        self.boton_ver_card.setObjectName("boton_ver_card")
        self.verticalLayout.addWidget(self.boton_ver_card)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Card"))
        self.image_card.setToolTip(_translate("Frame", "asdadadad"))
        self.boton_ver_card.setText(_translate("Frame", "Instalar"))


