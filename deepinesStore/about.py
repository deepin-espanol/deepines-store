#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5 import QtWidgets, QtGui
from deepinesStore.core import tr, site, set_blur, get_app_icon
from deepinesStore.widgets import G, ContactListWidget, add_people_to_list

authors = [G("Sebastian", "@SebTrujillo"), G("Amaro", "@xoascf")]

design = [G("Freddy", "@Akibaillusion"), G("jhalo", "@jhalo"), G("André")]

people = [G("Car", "@Xhafas"),
	G("Isaías", "@igatjens"), G("Jose", "@fenoll"), G("Hugo", "@geekmidget"),
	G("Eli", "@RealAct"), G("Diego", "@s_d1112"), G("Filho", "@filhoarrais"), G("Bruno", "@bigbruno"),
	G("Alvaro", "@G4SP3R"), G("Omi", "@peteromio"), G("Opik", "@Prophaniti"), G("Jose", "@jsiapodev"),
	G("Jorge", "@seiyukaras"), G("N1coc4colA", "@n1coc4cola"), G("Oscar", "@oscararg"), G("Jorge", "@jotakenobi"),
	G("Tomás", "@TomasWarynyca"), G("Edwinsiño", "@Shokatsuo"),
]

class AboutDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(580, 480)
		icon = get_app_icon()
		self.setWindowIcon(icon)
		self.setModal(True)
		fntLst = QtGui.QFont()
		fntLst.setPointSize(11)
		layout = QtWidgets.QHBoxLayout()
		list_dev = ContactListWidget()
		list_des = ContactListWidget()
		list_ppl = ContactListWidget()
		self.devP = add_people_to_list(authors, list_dev)
		self.desP = add_people_to_list(design, list_des)
		self.pplP = add_people_to_list(people, list_ppl)
		self.devP.setFont(fntLst)
		self.desP.setFont(fntLst)
		self.pplP.setFont(fntLst)
		layout.addWidget(self.devP)
		layout.addWidget(self.desP)
		layout.addWidget(self.pplP)
		self.setLayout(layout)
		self.setStyleSheet("background-color: rgba(20, 20, 20, 100)")
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.retranslateUi(self)

	def showEvent(self, event):
		set_blur(self)

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, AboutDialog):
		self.setWindowTitle(self.__tr("About"))
		self.devP.setTitle(self.__tr("Authors"))
		self.desP.setTitle(self.__tr("Design"))
		self.pplP.setTitle(self.__tr("Collaborators"))
