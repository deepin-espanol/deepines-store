#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

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
		self.app_icon_btn.setStyleSheet("background-color: transparent; border: none;")
		self.app_icon_btn.installEventFilter(self)

		self.app_name_lbl = QtWidgets.QLabel(self)
		self.app_name_lbl.setAlignment(QtCore.Qt.AlignCenter)
		self.version_lbl = QtWidgets.QLabel(self)
		self.version_lbl.setAlignment(QtCore.Qt.AlignCenter)
		self.web_lbl = LinkLabel(self)
		self.web_lbl.setAlignment(QtCore.Qt.AlignCenter)
		self.web_lbl.setText(get_text_link("deepinenespañol.org", additional_style="color: #419fd9;"))
		self.description_lbl = QtWidgets.QLabel(self)
		self.description_lbl.setAlignment(QtCore.Qt.AlignCenter)

		list_ppl = CreditsListWidget(self)
		list_ppl.setSpacing(2)
		self.pplP = add_people_to_list(people, list_ppl)

		layout = QtWidgets.QVBoxLayout(self)
		layout.addWidget(self.app_icon_btn)
		layout.addWidget(self.app_name_lbl)
		layout.addWidget(self.version_lbl)
		layout.addWidget(list_ppl)
		layout.addWidget(self.web_lbl)
		layout.addWidget(self.description_lbl)
		self.setLayout(layout)

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, AboutDialog):
		about_text = self.__tr("About")
		app_name_text = AboutDialog.parent().windowTitle()
		app_version_text = self.__tr("Version {version}").format(version=STORE_VERSION)
		description_text = self.__tr("The App Store of Deepin en Español")
		self.setWindowTitle(about_text)
		self.app_name_lbl.setText("<b>" + app_name_text + "</b>")
		self.version_lbl.setText(app_version_text)
		self.description_lbl.setText(description_text)