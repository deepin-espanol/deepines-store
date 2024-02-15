# -*- coding: utf-8 -*-


from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QMetaObject, QSize, Qt, QRect
from deepinesStore.widgets import ClickableLabel


class Ui_Frame(object):
	def setupUi(self, Frame):
		Frame.setObjectName("Frame")
		Frame.resize(230, 249)
		Frame.setMinimumSize(QSize(226, 249))
		Frame.setMaximumSize(QSize(230, 16777215))
		self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(0)
		self.image_app = ClickableLabel(Frame)
		self.image_app.setText("")
		self.image_app.setScaledContents(True)
		self.image_app.setAlignment(Qt.AlignCenter)
		self.image_app.setObjectName("image_app")
		self.image_app.setStyleSheet("#image_app{margin-top: 10px;}")
		self.verticalLayout.addWidget(self.image_app)
		self.lbl_name_app = ClickableLabel(Frame)
		self.lbl_name_app.setStyleSheet("background-color: transparent;" "margin-top:5px;")
		self.lbl_name_app.setText("")
		self.lbl_name_app.setAlignment(Qt.AlignCenter)
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setItalic(False)
		self.lbl_name_app.setFont(font)
		self.lbl_name_app.setWordWrap(True)
		self.lbl_name_app.setObjectName("lbl_name_app")
		self.verticalLayout.addWidget(self.lbl_name_app)
		self.btn_select_app = ClickableLabel(Frame)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setItalic(False)
		self.btn_select_app.setFont(font)
		self.btn_select_app.setWordWrap(True)
		self.btn_select_app.setAlignment(Qt.AlignCenter)
		self.btn_select_app.setObjectName("btn_select_app")
		self.verticalLayout.addWidget(self.btn_select_app)
		self.pushButton = QtWidgets.QPushButton(Frame)
		self.pushButton.setObjectName(u"pushButton")
		self.pushButton.setMinimumSize(QSize(100, 30))
		self.pushButton.setText(u"Desinstalar")
		self.pushButton.setVisible(False)
		self.verticalLayout.addWidget(self.pushButton)

		QMetaObject.connectSlotsByName(Frame)
