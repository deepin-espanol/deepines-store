# -*- coding: utf-8 -*-

# UI Source 'guis/card.ui'

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, QMetaObject, QSize, Qt, pyqtSignal


class QLabelClickable(QtWidgets.QLabel):

    clicked = pyqtSignal()
    def __init__(self, *args):
        QtWidgets.QLabel.__init__(self, *args)
    def mouseReleaseEvent(self, ev):
        self.clicked.emit()


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(230, 249)
        Frame.setMinimumSize(QSize(226, 249))
        Frame.setMaximumSize(QSize(230, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_app = QLabelClickable(Frame)
        self.image_app.setText("")
        self.image_app.setScaledContents(True)
        self.image_app.setAlignment(Qt.AlignCenter)
        self.image_app.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.image_app.setObjectName("image_app")
        self.image_app.setStyleSheet("#image_app{margin-top: 10px;}")
        self.verticalLayout.addWidget(self.image_app)
        self.lbl_name_app = QLabelClickable(Frame)
        self.lbl_name_app.setStyleSheet("background-color: transparent;" "margin-top:5px;")
        self.lbl_name_app.setText("")
        self.lbl_name_app.setAlignment(Qt.AlignCenter)
        self.lbl_name_app.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setItalic(False)
        self.lbl_name_app.setFont(font)
        self.lbl_name_app.setWordWrap(True)
        self.lbl_name_app.setObjectName("lbl_name_app")
        self.verticalLayout.addWidget(self.lbl_name_app)
        self.btn_select_app = QLabelClickable(Frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        font.setItalic(False)
        self.btn_select_app.setFont(font)
        self.btn_select_app.setWordWrap(True)
        self.btn_select_app.setAlignment(Qt.AlignCenter)
        self.btn_select_app.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        self.btn_select_app.setObjectName("btn_select_app")
        self.verticalLayout.addWidget(self.btn_select_app)

        self.retranslateUi(Frame)
        QMetaObject.connectSlotsByName(Frame)

    def __tr(self, txt, disambiguation=None, n=-1):
      return QCoreApplication.translate(self.__class__.__name__, txt, disambiguation, n)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(self.__tr("Card"))
        self.btn_select_app.setText(self.__tr("Install"))
