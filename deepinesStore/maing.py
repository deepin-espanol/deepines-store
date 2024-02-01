# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QMetaObject, QRect, QSize, Qt, pyqtSignal

from deepinesStore.core import get_res, tr, get_text_link, STORE_VERSION
from deepinesStore.widgets import ClickableLabel


# https://stackoverflow.com/a/67711660
size = 19
border = 0.2
TitleBarButtonStylesheet = '''
			QRadioButton {{
				background-color: transparent;
				padding: 3px;
			}}
			QRadioButton::indicator {{
				border: {border}px solid {borderColor}; 
				height: {size}px;
				width: {size}px;
				border-radius: {radius}px;
			}}
			QRadioButton::indicator:checked, QRadioButton::indicator:unchecked {{
				background: qradialgradient(
					cx:.5, cy:.5, radius: {innerRatio},
					fx:.5, fy:.5,
					stop:0 {uncheckColor},
					stop:0.49 {uncheckColor2},
					stop:0.54 transparent,
					stop:1 transparent
					);
			}}
			QRadioButton::indicator:hover {{
				background: rgba(245, 245, 245, 72);
			}}
		'''.format(
	size=size - border * 2,
	border=border,
	borderColor='black',
	radius=size // 2,
	innerRatio=1 - (border * 2 + 1) / size,
	uncheckColor='rgba(245, 245, 245, 38)',
	uncheckColor2='rgba(247, 247, 247, 38)',
	checkColor='black'
)


class Ui_MainWindow(object):

	def __init__(self, width, height):
		#print("El ancho del monitor es: {}".format(width))

		self.width_screen = int(width * 0.7)
		if self.width_screen < 945:
			self.width_screen = 945
		#print("El width_screen ({}*0.7) es: {}".format(width, self.width_screen))

		self.height_screen = int(height * 0.85)
		if self.height_screen < 700:
			self.height_screen = 700
		#print("El height_screen ({}*0.8) es: {}".format(height, self.height_screen))

		self.size_frame = int(width * 0.14)
		if self.size_frame < 200:
			self.size_frame = 200
		if self.size_frame > 300:
			self.size_frame = 300
		#print("El frame ({}*0.14) es: {}".format(width, self.size_frame))

	def setupUi(self, MainWindow):
		svg_fondo = get_res('icono')
		svg_star = get_res('star')
		svg_deepines = get_res('deepines_filter')
		svg_internet = get_res('internet')
		svg_music = get_res('music')
		svg_picture = get_res('picture')
		svg_console = get_res('console')
		svg_board = get_res('board')
		svg_terminal = get_res('terminal')
		svg_computer = get_res('computer')
		svg_pamela = get_res('pamela')
		svg_search = get_res('magnifying-glass')
		svg_car = get_res('carDisable')

		MainWindow.setObjectName("MainWindow")
		MainWindow.setMinimumSize(QSize(self.width_screen, self.height_screen))
		MainWindow.resize(self.width_screen, self.height_screen)
		MainWindow.setStyleSheet(
			"QScrollBar:vertical {\n"
			"	background: transparent;\n"
			"	width: 10px;\n"
			"	margin: 0px 0px 0px 0px;\n"
			"}\n"
			"QScrollBar::handle:vertical {\n"
			"	background-color: #545454;\n"
			"	border-radius: 4px;\n"
			"	min-height: 5px;\n"
			"}\n"
			"QScrollBar::add-line:vertical {\n"
			"	background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
			"	stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
			"	height: 0px;\n"
			"	subcontrol-position: bottom;\n"
			"	subcontrol-origin: margin;\n"
			"}\n"
			"QScrollBar::sub-line:vertical {\n"
			"	background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
			"	stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
			"	height: 0 px;\n"
			"	subcontrol-position: top;\n"
			"	subcontrol-origin: margin;\n"
			"}")
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setStyleSheet(
			"background-color: rgba(30, 30, 30, 200);" "color: #b5c5d1;")
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setSpacing(0)
		self.gridLayout_2.setObjectName("gridLayout_2")

		# Frame apps seleccionadas
		self.widget = QtWidgets.QWidget(self.centralwidget)
		self.widget.setMinimumSize(QSize(0, 40))
		self.widget.setMaximumSize(QSize(16777215, 80))
		self.widget.setStyleSheet("background-color: rgba(16, 16, 16, 0);")
		self.widget.setObjectName("widget")
		self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
		self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
		self.horizontalLayout_3.setSpacing(10)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")

		self.icon_car = ClickableLabel(self.widget)
		self.icon_car.setStyleSheet("margin-left: 0px;\n"
									"background-color: transparent;\n"
									"border-color: transparent;\n"
									"border: 0px solid;")
		self.icon_car.setText("")
		pix_car = QtGui.QPixmap(svg_car)
		self.icon_car.setPixmap(pix_car)
		self.icon_car.setScaledContents(True)
		self.icon_car.setMinimumSize(QSize(20, 20))
		self.icon_car.setMaximumSize(QSize(20, 20))

		self.icon_car.setObjectName("icon_car")
		self.horizontalLayout_3.addWidget(self.icon_car)
		self.lbl_list_apps = ClickableLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(11)
		self.lbl_list_apps.setFont(font)
		self.lbl_list_apps.setStyleSheet("background-color: transparent;\n" "")
		self.lbl_list_apps.setObjectName("lbl_list_apps")
		self.horizontalLayout_3.addWidget(self.lbl_list_apps)
		self.btn_install = QtWidgets.QPushButton(self.widget)
		self.btn_install.setMinimumSize(QSize(80, 0))
		self.btn_install.setMaximumSize(QSize(100, 16777215))
		self.btn_install.setStyleSheet(
			"#btn_install{\n"
			"padding: 2px;\n"
			"border-radius: 5px;\n"
			"background-color: rgb(45, 45, 45);\n"
			"border: 2px solid rgb(45, 45, 45);\n"
			"}\n"
			"#btn_install:hover{\n"
			"padding: 2px;\n"
			"color:white;\n"
			"background-color: rgb(65, 159, 217);\n"
			"border: 1px solid rgb(142, 231, 255);\n"
			"border-radius: 5px;\n"
			"}")
		self.btn_install.setObjectName("btn_install")
		self.horizontalLayout_3.addWidget(self.btn_install)
		self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
		self.gridLayout_2.addWidget(self.widget, 2, 1, 1, 1)

		# Frame side bar
		self.frame_2 = QtWidgets.QFrame(self.centralwidget)
		self.frame_2.setMinimumSize(QSize(self.size_frame, 0))
		self.frame_2.setMaximumSize(QSize(self.size_frame, 16777215))
		self.frame_2.setStyleSheet("background-color: rgba(16, 16, 16, 0);")
		self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame_2.setObjectName("frame_2")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
		self.verticalLayout.setObjectName("verticalLayout")
		spacerItem2 = QtWidgets.QSpacerItem(20, 2,
											QtWidgets.QSizePolicy.Minimum,
											QtWidgets.QSizePolicy.Fixed)
		# Primer item, spaciador vertical
		self.verticalLayout.addItem(spacerItem2)
		self.frame_4 = QtWidgets.QFrame(self.frame_2)
		self.frame_4.setMinimumSize(QSize(0, 35))
		self.frame_4.setMaximumSize(QSize(16777215, 35))
		self.frame_4.setStyleSheet("border-radius: 15px;\n"
								   "background-color: rgba(16, 16, 16, 122);\n"
								   "color: white;")
		self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame_4.setObjectName("frame_4")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.lineEdit = QtWidgets.QLineEdit(self.frame_4)
		self.lineEdit.setStyleSheet("background-color: transparent;\n"
									"color: white;\n"
									"border-color: transparent;\n"
									"border: 0px solid;")
		self.lineEdit.setAlignment(Qt.AlignCenter)
		self.lineEdit.setObjectName("lineEdit")
		self.horizontalLayout_2.addWidget(self.lineEdit)
		self.pushButton = QtWidgets.QPushButton(self.frame_4)
		self.pushButton.setStyleSheet("margin-left: 0px;\n"
									  "background-color: transparent;\n"
									  "border-color: transparent;\n"
									  "border: 0px solid;")
		self.pushButton.setText("")
		icon11 = QtGui.QIcon()
		icon11.addPixmap(QtGui.QPixmap(svg_search),
						 QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton.setIcon(icon11)
		self.pushButton.setIconSize(QSize(13, 13))
		self.pushButton.setObjectName("pushButton")
		self.horizontalLayout_2.addWidget(self.pushButton)
		# Segundo item, cuadro busqueda
		self.verticalLayout.addWidget(self.frame_4)
		self.listWidget = QtWidgets.QListWidget(self.frame_2)
		self.listWidget.setStyleSheet(
			"#listWidget{\n"
			"  padding-left:10px;\n"
			"  padding-top:6px;\n"
			"  padding-bottom:6px;\n"
			"  border-radius: 15px;\n"
			"  background-color: rgba(16, 16, 16, 163);\n"
			"}\n"
			"#listWidget:item{\n"
			# Top Right Bottom Left
			"  padding: 3px 5px 3px 5px;\n"
			"}\n"
			"#listWidget:item:selected{\n"
			"  background-color: transparent;\n"
			"  border: 0px solid transparent;\n"
			"  color: #419fd9;\n"
			"}")
		self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.listWidget.setAutoScroll(False)
		self.listWidget.setIconSize(QSize(24, 24))
		self.listWidget.setObjectName("listWidget")
		item = QtWidgets.QListWidgetItem()
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(svg_star),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon1)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(svg_deepines),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon2)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(svg_internet),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon3)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon4 = QtGui.QIcon()
		icon4.addPixmap(QtGui.QPixmap(svg_music),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon4)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon5 = QtGui.QIcon()
		icon5.addPixmap(QtGui.QPixmap(svg_picture),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon5)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon6 = QtGui.QIcon()
		icon6.addPixmap(QtGui.QPixmap(svg_console),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon6)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon7 = QtGui.QIcon()
		icon7.addPixmap(QtGui.QPixmap(svg_board),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon7)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon8 = QtGui.QIcon()
		icon8.addPixmap(QtGui.QPixmap(svg_terminal),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon8)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon9 = QtGui.QIcon()
		icon9.addPixmap(QtGui.QPixmap(svg_computer),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon9)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon10 = QtGui.QIcon()
		icon10.addPixmap(QtGui.QPixmap(svg_pamela),
						 QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon10)
		item.setFlags(Qt.ItemIsSelectable | 
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		item.setFlags(Qt.NoItemFlags)
		self.listWidget.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon11 = QtGui.QIcon()
		icon11.addPixmap(QtGui.QPixmap(svg_pamela),
						 QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon11)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.listWidget.addItem(item)
		# Tercer item, lista de filtros
		self.verticalLayout.addWidget(self.listWidget)

		self.widget_2 = QtWidgets.QWidget(self.frame_2)
		self.widget_2.setStyleSheet("background-color:transparent;")
		self.widget_2.setObjectName("widget_2")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setSpacing(0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.label_2 = ClickableLabel(self.widget_2)
		self.label_2.setMinimumSize(QSize(180, 180))
		self.label_2.setMaximumSize(QSize(180, 180))
		self.label_2.setStyleSheet("background-color: transparent;")
		self.label_2.setText("")
		self.label_2.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
		self.label_2.setPixmap(QtGui.QPixmap(svg_fondo))
		self.label_2.setScaledContents(True)
		self.label_2.setOpenExternalLinks(True)
		self.label_2.setObjectName("label_2")
		self.horizontalLayout.addWidget(self.label_2)

		# Cuarto item, img deepines
		self.verticalLayout.addWidget(self.widget_2)
		self.label = ClickableLabel(self.frame_2)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.label.setFont(font)
		self.label.setStyleSheet("background-color: transparent;\n")
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
		self.label.setObjectName("label")

		# Quinto item, label version
		self.verticalLayout.addWidget(self.label)
		self.gridLayout_2.addWidget(self.frame_2, 0, 0, 3, 1)
		self.frame = QtWidgets.QScrollArea(self.centralwidget)
		self.frame.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.frame.setWidgetResizable(True)
		self.frame.setAlignment(Qt.AlignCenter)
		self.frame.setObjectName("frame")
		self.frame.setStyleSheet("background-color: rgba(16, 16, 16, 0);")
		self.scroll_apps = QtWidgets.QWidget()
		self.scroll_apps.setGeometry(QRect(0, 0, 774, 459))
		self.scroll_apps.setObjectName("scroll_apps")
		self.scroll_apps.setStyleSheet(
			"#scroll_apps{ padding-left: 30px; padding-right: 30px;}")
		self.gridLayout = QtWidgets.QGridLayout(self.scroll_apps)
		self.gridLayout.setObjectName("gridLayout")
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setSpacing(2)
		self.frame.setWidget(self.scroll_apps)
		self.gridLayout_2.addWidget(self.frame, 1, 1, 1, 1)

		# Title bar
		self.widget_1 = QtWidgets.QWidget(self.centralwidget)
		self.widget_1.setObjectName("widget_1")
		self.widget_1.setStyleSheet("""
			#widget_1{
				background-color: transparent;
			}
			#label_3{
				background-color: transparent;
			}
			""")
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_1)
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.horizontalLayout_4.setContentsMargins(0, 12, 0, 5)
		self.horizontalLayout_4.setSpacing(1)
		
		self.btn_app_deb = QtWidgets.QPushButton(self.widget_1)
		self.btn_app_deb.setObjectName(u"btn_app_deb")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.btn_app_deb.sizePolicy().hasHeightForWidth())
		self.btn_app_deb.setSizePolicy(sizePolicy)
		self.btn_app_deb.setStyleSheet("""
								 background-color: rgb(169, 144, 122);
								 color: #fff;
								 border-color: #fff;
								 border: 2px solid;
								 border-radius: 15px;""")
		self.btn_app_deb.setIcon(QtGui.QIcon(QtGui.QPixmap(get_res('flatpak'))))
		self.btn_app_deb.setMinimumSize(QSize(150, 35))

		self.horizontalLayout_4.addWidget(self.btn_app_deb)

		spacerItem1 = QtWidgets.QSpacerItem(
			40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem1)

		self.label_3 = QtWidgets.QLabel(self.widget_1)
		self.label_3.setObjectName("label_3")
		font = QtGui.QFont()
		font.setPointSize(20)
		self.label_3.setFont(font)
		self.horizontalLayout_4.addWidget(self.label_3)


		spacerItem2 = QtWidgets.QSpacerItem(
			40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem2)

		self.btn_minimize = QtWidgets.QRadioButton(self.widget_1)
		self.btn_minimize.setObjectName("btn_minimize")
		self.btn_minimize.setStyleSheet(TitleBarButtonStylesheet)
		self.horizontalLayout_4.addWidget(self.btn_minimize)

		self.btn_zoom = QtWidgets.QRadioButton(self.widget_1)
		self.btn_zoom.setObjectName("btn_zoom")
		self.btn_zoom.setStyleSheet(TitleBarButtonStylesheet)
		self.horizontalLayout_4.addWidget(self.btn_zoom)

		self.btn_close = QtWidgets.QRadioButton(self.widget_1)
		self.btn_close.setObjectName("btn_close")
		self.btn_close.setStyleSheet(TitleBarButtonStylesheet)
		self.horizontalLayout_4.addWidget(self.btn_close)

		self.gridLayout_2.addWidget(self.widget_1, 0, 1, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		self.listWidget.setCurrentRow(-1)
		QMetaObject.connectSlotsByName(MainWindow)

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(self.__tr("Deepines Store"))
		self.label_2.setToolTip(self.__tr("About us"))
		self.label_3.setText(self.__tr("Deepines Store"))
		self.lbl_list_apps.setText(self.__tr("TextLabel"))
		self.btn_install.setText(self.__tr("Install"))
		__sortingEnabled = self.listWidget.isSortingEnabled()
		self.listWidget.setSortingEnabled(False)
		item = self.listWidget.item(0)
		item.setText(self.__tr("Home"))
		item = self.listWidget.item(1)
		item.setText(self.__tr("Deepines"))
		item = self.listWidget.item(2)
		item.setText(self.__tr("Internet"))
		item = self.listWidget.item(3)
		item.setText(self.__tr("Multimedia"))
		item = self.listWidget.item(4)
		item.setText(self.__tr("Graphics"))
		item = self.listWidget.item(5)
		item.setText(self.__tr("Games"))
		item = self.listWidget.item(6)
		item.setText(self.__tr("Office automation"))
		item = self.listWidget.item(7)
		item.setText(self.__tr("Development"))
		item = self.listWidget.item(8)
		item.setText(self.__tr("System"))
		item = self.listWidget.item(9)
		item.setText(self.__tr("Other"))
		item = self.listWidget.item(10)
		item.setText(self.__tr(""))
		item = self.listWidget.item(11)
		item.setText(self.__tr("Installed apps"))
		self.listWidget.setSortingEnabled(__sortingEnabled)
		self.lineEdit.setPlaceholderText(self.__tr("Search"))
		self.about_version_text = self.__tr("About \nVersion: {version}")
		self.btn_minimize.setToolTip(self.__tr("Minimize"))
		self.btn_zoom.setToolTip(self.__tr("Zoom"))
		self.btn_close.setToolTip(self.__tr("Close"))
		self.label.setText(self.about_version_text.format(version=STORE_VERSION))
		self.btn_app_deb.setText(self.__tr("Apps Flatpak"))
		
		# StoreWindow
		self.list_apps_text = self.__tr("Select the apps to install")
		self.selected_to_install_app_text = self.__tr("Selected")
		self.selected_installed_app_text = self.__tr("Installed")
		self.single_app_text = self.__tr("{app_count} app selected to install, click here to review it")
		self.multi_apps_text = self.__tr("{app_count} apps selected to install, click here to review them")
		self.error_no_server_text = self.__tr("Unable to establish connection with the server, <br>"
											  "please check your internet connection.<br>"
											  "If the problem persists, please contact us via Telegram <br>"
											  "at {atTlURL}.<br><br>"
											  "Visit Deepin en Español for more information: {siteURL}").format(atTlURL=get_text_link("@deepinenespanol"), siteURL=get_text_link("deepinenespañol.org"))
		self.error_no_deepines_repo_text = self.__tr("Deepines repository is not installed on your system,<br>"
													 "Deepines Store needs this repository to work.<br>"
													 "In the following link you will find the instructions to install it:<br><br>"
													 "{repoURL}").format(repoURL=get_text_link("deepinenespañol.org/deepines/"))
