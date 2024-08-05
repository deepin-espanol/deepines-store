#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from deepinesStore.core import tr, get_app_icon, get_text_link, STORE_VERSION
from deepinesStore.widgets import G, add_people_to_list, LinkLabel, CreditsListWidget

people = [G("Car", "@Xhafas"), G("Sebastian Trujillo", "@SebTrujillo"), G("Amaro Martínez", "@xoascf"),
G("Freddy", "@Akibaillusion"), G("jhalo", "@jhalo"),
G("Isaías Gätjens M", "@igatjens"), G("Jose Fenoll", "@fenoll"), G("Hugo Florentino", "@geekmidget"),
G("Eli", "@RealAct"), G("Diego", "@s_d1112"), G("Filho Arrais", "@filhoarrais"),
G("Alvaro Samudio", "@G4SP3R"), G("José Siapo", "@jsiapodev"),
G("Oscar Ortiz", "@oscararg"),  G("Edwinsiño C", "@Shokatsuo"),
]

class AboutDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(380, 460)
		icon = get_app_icon()
		self.setWindowIcon(icon)
		self.setModal(True)
		self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
		self.setAutoFillBackground(True)
		self.app_icon_btn = QtWidgets.QPushButton(self)
		self.app_icon_btn.setEnabled(True)
		self.app_icon_btn.setIconSize(QtCore.QSize(120, 120))
		self.app_icon_btn.setFlat(True)
		self.app_icon_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
		self.app_icon_btn.setIcon(icon)
		self.app_icon_btn.setStyleSheet("background-color: transparent;")

		self.app_icon_btn.installEventFilter(self)
		self.app_name_lbl = QtWidgets.QLabel(self)
		self.version_lbl = QtWidgets.QLabel(self)
		self.version_lbl.setAlignment(QtCore.Qt.AlignCenter)
		self.web_lbl = LinkLabel(self)
		self.web_lbl.setAlignment(QtCore.Qt.AlignCenter)
		self.web_lbl.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
		font = QtGui.QFont()
		font.setBold(True)
		font.setPointSize(10)
		self.app_name_lbl.setFont(font)
		self.app_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
		self.description_lbl = QtWidgets.QLabel(self)
		font.setBold(False)
		self.description_lbl.setFont(font)
		self.description_lbl.setAlignment(QtCore.Qt.AlignCenter)

		list_ppl = CreditsListWidget(self)
		list_ppl.setSpacing(2)
		self.pplP = add_people_to_list(people, list_ppl)
		fntLst = QtGui.QFont()
		fntLst.setPointSize(11)
		list_ppl.setFont(fntLst)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.app_icon_btn)
		layout.addWidget(self.app_name_lbl)
		layout.addWidget(self.version_lbl)
		layout.addWidget(list_ppl)
		layout.addWidget(self.web_lbl)
		layout.addWidget(self.description_lbl)
		self.setLayout(layout)

		self.retranslateUi(self) # TODO: Add translator credits.
		QtCore.QMetaObject.connectSlotsByName(self)

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, AboutDialog):
		self.setWindowTitle(self.__tr("About"))
		self.app_name_lbl.setText(AboutDialog.parent().windowTitle())
		self.version_lbl.setText(self.__tr("Version {version}").format(version=STORE_VERSION))
		self.web_lbl.setText(get_text_link("deepinenespañol.org"))
		self.description_lbl.setText(self.__tr("The App Store of Deepin en Español"))
