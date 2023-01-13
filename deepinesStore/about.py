#!/usr/bin/python3
# -*- coding: utf-8 -*-

from deepinesStore.core import tr, site, set_blur
from deepinesStore.maing import app_icon, TitleBarButtonStylesheet
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout,\
	QSpacerItem, QSizePolicy, QLabel, QFrame, QDesktopWidget, QRadioButton
from PyQt5.QtGui import QFont, QCursor

Stylesheet = """

#AboutDialog{
  background-color: transparent;
  border-radius: 0px;
}

#AboutWidget{
  background-color: rgba(30, 30, 30, 150);
}

#devBy{
	margin-bottom: 10px;
}
#deepinesLink{
	margin-top: 5px;
	color: rgba(0, 192, 255, 255);
}

#label, #sName,
#devBy, #devPs, #devPr,
#uiDes, #desgn, #saPro,
#uxWrt, #wbPro, #srvPr,
#collb{
  color: white;  
}

#frame{
  border: transparent;
}

#btn_close {
	margin-top: 5px;
	margin-right: -10px;
}
"""

credits = [
"Car @Xhafas",

"Sebastian @SebTrujillo; Amaro M. @xoascf",

"Freddy @Akibaillusion",

"Isaías @igatjens",

"jhalo @jhalo; André",

"Jose @fenoll; Hugo @geekmidget",

"Eli @RealAct; Diego @s_d1112",

"@filhoarrais; Bruno @bigbruno",

"Alvaro @G4SP3R; Omi @peteromio; Opik @Prophaniti; Jose @ProgramacionJS; "
"Jorge @seiyukaras; @n1coc4cola; Oscar @oscararg; Jorge @jotakenobi; "
"Tomás @TomasWarynyca; Edwinsiño @Shokatsuo"
]

class QLabelClickable(QLabel):

	clicked = pyqtSignal()

	def __init__(self, *args):
		QLabel.__init__(self, *args)

	def mouseReleaseEvent(self, ev):
		self.clicked.emit()


class AboutDialog(QDialog):

	def __init__(self, parent):
		super(AboutDialog, self).__init__(parent)
		self.setObjectName('AboutDialog')
		self.setMinimumSize(QSize(720, 700))
		self.setMaximumSize(QSize(720, 1000))
		self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setStyleSheet(Stylesheet)
		self.initUi()
		self.center()
		self.deepinesLink.clicked.connect(site)
		set_blur(self)

	def initUi(self):
		self.gridLayout = QGridLayout(self)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setSpacing(0)
		self.gridLayout.setObjectName("gridLayout")
		self.widget = QWidget(self)
		self.widget.setObjectName("AboutWidget")

		self.verticalLayout = QVBoxLayout(self.widget)
		self.verticalLayout.setContentsMargins(10, 0, 10, 10)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.horizontalLayout_2 = QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.horizontalLayout_2.addItem(QSpacerItem(
			40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

		self.btn_close = QRadioButton(self)
		self.btn_close.setObjectName("btn_close")
		self.btn_close.setStyleSheet(TitleBarButtonStylesheet)
		self.btn_close.clicked.connect(self.close)
		self.horizontalLayout_2.addWidget(self.btn_close)

		self.verticalLayout.addLayout(self.horizontalLayout_2)
		spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.verticalLayout.addItem(spacerItem2)
		self.sName = QLabel(self)
		font = QFont()
		font.setPointSize(20)
		self.sName.setFont(font)
		self.sName.setAlignment(Qt.AlignCenter)
		self.sName.setObjectName("sName")
		self.verticalLayout.addWidget(self.sName)
		self.frame = QFrame(self)
		self.frame.setFrameShape(QFrame.StyledPanel)
		self.frame.setFrameShadow(QFrame.Raised)
		self.frame.setObjectName("frame")
		self.horizontalLayout = QHBoxLayout(self.frame)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.label = QLabel(self.frame)
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(2)
		sizePolicy.setVerticalStretch(2)
		sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
		self.label.setSizePolicy(sizePolicy)
		self.label.setSizeIncrement(QSize(2, 2))
		self.label.setBaseSize(QSize(50, 50))
		self.label.setScaledContents(True)
		self.label.setText("")
		self.label.setPixmap(app_icon.pixmap(222))
		self.label.setObjectName("label")
		self.horizontalLayout.addWidget(self.label)
		self.verticalLayout.addWidget(self.frame)
		self.devBy = QLabel(self)
		font = QFont()
		font.setPointSize(14)
		self.devBy.setFont(font)
		self.devBy.setAlignment(Qt.AlignCenter)
		self.devBy.setWordWrap(True)
		self.devBy.setObjectName("devBy")
		self.verticalLayout.addWidget(self.devBy)
		font = QFont()
		font.setPointSize(12)
		self.devPr = QLabel(self)
		self.devPr.setFont(font)
		self.devPr.setAlignment(Qt.AlignCenter)
		self.devPr.setObjectName("devPr")
		self.verticalLayout.addWidget(self.devPr)
		self.devPs = QLabel(self)
		self.devPs.setAlignment(Qt.AlignCenter)
		self.devPs.setFont(font)
		self.devPs.setObjectName("devPs")
		self.verticalLayout.addWidget(self.devPs)
		self.uiDes = QLabel(self)
		self.uiDes.setAlignment(Qt.AlignCenter)
		self.uiDes.setObjectName("uiDes")
		self.uiDes.setFont(font)
		self.verticalLayout.addWidget(self.uiDes)
		self.uxWrt = QLabel(self)
		self.uxWrt.setAlignment(Qt.AlignCenter)
		self.uxWrt.setFont(font)
		self.uxWrt.setObjectName("uxWrt")
		self.verticalLayout.addWidget(self.uxWrt)
		self.desgn = QLabel(self)
		self.desgn.setAlignment(Qt.AlignCenter)
		self.desgn.setObjectName("desgn")
		self.desgn.setFont(font)
		self.verticalLayout.addWidget(self.desgn)
		self.saPro = QLabel(self)
		self.saPro.setAlignment(Qt.AlignCenter)
		self.saPro.setFont(font)
		self.saPro.setObjectName("saPro")
		self.verticalLayout.addWidget(self.saPro)
		self.wbPro = QLabel(self)
		self.wbPro.setAlignment(Qt.AlignCenter)
		self.wbPro.setFont(font)
		self.wbPro.setObjectName("wbPro")
		self.verticalLayout.addWidget(self.wbPro)
		self.srvPr = QLabel(self)
		self.srvPr.setAlignment(Qt.AlignCenter)
		self.srvPr.setFont(font)
		self.srvPr.setObjectName("srvPr")
		self.verticalLayout.addWidget(self.srvPr)
		self.collb = QLabel(self)
		self.collb.setAlignment(Qt.AlignCenter)
		self.collb.setFont(font)
		self.collb.setObjectName("collb")
		self.collb.setWordWrap(True)
		self.verticalLayout.addWidget(self.collb)

		self.deepinesLink = QLabelClickable(self)
		self.deepinesLink.setAlignment(Qt.AlignCenter)
		font = QFont()
		font.setPointSize(14)
		self.deepinesLink.setFont(font)
		self.deepinesLink.setCursor(QCursor(Qt.PointingHandCursor))
		self.deepinesLink.setObjectName("deepinesLink")
		self.verticalLayout.addWidget(self.deepinesLink)
		self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
		self.retranslateUi(self)

	def calcular_tamanio(self, width, height):
		global r_width, r_height
		r_width = width * 0.6
		r_height = height * 0.9

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, AboutDialog):
		AboutDialog.setWindowTitle(self.__tr("About"))
		self.sName.setText(self.__tr("Deepines Store"))
		self.devBy.setText(self.__tr("Developed by Deepin en Español"))
		self.devPr.setText(self.__tr("Project Leader: {}").format(credits[0]))
		self.devPs.setText(self.__tr("Development: {}").format(credits[1]))
		self.uiDes.setText(self.__tr("UI: {}").format(credits[2]))
		self.uxWrt.setText(self.__tr("OG UX Writer: {}").format(credits[3]))
		self.desgn.setText(self.__tr("Design: {}").format(credits[4]))
		self.saPro.setText(self.__tr("SysAdmin: {}").format(credits[5]))
		self.wbPro.setText(self.__tr("Web: {}").format(credits[6]))
		self.srvPr.setText(self.__tr("Servers: {}").format(credits[7]))
		self.collb.setText(self.__tr("Collaborators: {}").format(credits[8]))
		self.deepinesLink.setText(self.__tr("deepinenespañol.org | Copy link"))
