# -*- coding: utf-8 -*-


from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QMetaObject, QSize, Qt

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
		self.lbl_version = ClickableLabel(Frame)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setItalic(False)
		self.lbl_version.setFont(font)
		self.lbl_version.setWordWrap(True)
		self.lbl_version.setAlignment(Qt.AlignCenter)
		self.lbl_version.setObjectName("lbl_version")
		self.verticalLayout.addWidget(self.lbl_version)
		self.btn_select_app = QtWidgets.QPushButton(Frame)
		self.btn_select_app.setObjectName(u"btn_select_app")
		self.btn_select_app.setMinimumSize(QSize(100, 30))
		self.verticalLayout.addWidget(self.btn_select_app)

		self.retranslateUi(Frame)
		QMetaObject.connectSlotsByName(Frame)

	def __tr(self, txt, disambiguation=None, n=-1):
		from deepinesStore.core import tr
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, Frame):
		self.btn_select_app.setText(self.__tr("Select"))