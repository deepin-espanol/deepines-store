# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QMetaObject, QRect, QSize, Qt

from deepinesStore.core import get_dtk_window_radius
from deepinesStore.core import get_res, tr, get_text_link, STORE_VERSION
from deepinesStore.widgets import ClickableLabel, ClickableList

class Ui_MainWindow(QtWidgets.QMainWindow):

	def __init__(self, width, height):
		super().__init__()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.radius_dtk = get_dtk_window_radius()
		self.setStyleSheet(
			"background-color: rgb(30, 30, 30);\n"
			"color: #b5c5d1;\n"
			f"border-radius: {self.radius_dtk}px;\n"
			)
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

	def setupUi(self):
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
		svg_minimizar = get_res('minimizar')
		svg_maximizar = get_res('maximizar')
		svg_cerrar = get_res('cerrar')
		
		MainWindow = QtWidgets.QWidget(self)
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

		# Grilla principal
		self.gridLayout_2 = QtWidgets.QGridLayout(MainWindow)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setSpacing(0)
		self.gridLayout_2.setObjectName("gridLayout_2")

		# Frame apps seleccionadas
		self.widget = QtWidgets.QWidget(MainWindow)
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
		self.btn_install.setMaximumSize(QSize(150, 16777215))
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
		self.frame_2 = QtWidgets.QFrame(MainWindow)
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
		
		self.lw_categories = ClickableList(self.frame_2)
		self.lw_categories.setStyleSheet(
			"#lw_categories{\n"
			"  padding-left:10px;\n"
			"  padding-top:6px;\n"
			"  padding-bottom:6px;\n"
			"  border-radius: 15px;\n"
			"  background-color: rgba(16, 16, 16, 163);\n"
			"}\n"
			"#lw_categories:item{\n"
			# Top Right Bottom Left
			"  padding: 3px 5px 3px 5px;\n"
			"}\n"
			"#lw_categories:item:selected{\n"
			"  background-color: transparent;\n"
			"  border: 0px solid transparent;\n"
			"  color: #419fd9;\n"
			"}")
		self.lw_categories.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.lw_categories.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.lw_categories.setAutoScroll(False)
		self.lw_categories.setIconSize(QSize(24, 24))
		self.lw_categories.setObjectName("lw_categories")
		item = QtWidgets.QListWidgetItem()
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(svg_star),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon1)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(svg_deepines),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon2)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon3 = QtGui.QIcon()
		icon3.addPixmap(QtGui.QPixmap(svg_internet),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon3)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon4 = QtGui.QIcon()
		icon4.addPixmap(QtGui.QPixmap(svg_music),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon4)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon5 = QtGui.QIcon()
		icon5.addPixmap(QtGui.QPixmap(svg_picture),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon5)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon6 = QtGui.QIcon()
		icon6.addPixmap(QtGui.QPixmap(svg_console),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon6)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon7 = QtGui.QIcon()
		icon7.addPixmap(QtGui.QPixmap(svg_board),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon7)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon8 = QtGui.QIcon()
		icon8.addPixmap(QtGui.QPixmap(svg_terminal),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon8)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon9 = QtGui.QIcon()
		icon9.addPixmap(QtGui.QPixmap(svg_computer),
						QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon9)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon10 = QtGui.QIcon()
		icon10.addPixmap(QtGui.QPixmap(svg_pamela),
						 QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon10)
		item.setFlags(Qt.ItemIsSelectable | 
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		item.setFlags(Qt.NoItemFlags)
		self.lw_categories.set_skip_item_action_indices([10])

		self.lw_categories.addItem(item)
		item = QtWidgets.QListWidgetItem()
		icon11 = QtGui.QIcon()
		icon11.addPixmap(QtGui.QPixmap(svg_pamela),
						 QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon11)
		item.setFlags(Qt.ItemIsSelectable |
					  Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		self.lw_categories.addItem(item)
		# Tercer item, lista de filtros
		self.verticalLayout.addWidget(self.lw_categories)

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
		self.gridLayout_2.addWidget(self.frame_2, 1, 0, 3, 1)
		self.frame = QtWidgets.QScrollArea(MainWindow)
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
		self.widget_1 = QtWidgets.QWidget(MainWindow)
		self.widget_1.setObjectName("widget_1")
		self.widget_1.setStyleSheet("""
			#widget_1{
				background-color: transparent;
			}
			#label_3{
				background-color: transparent;
			}
			#btn_close{
                margin-right: 10px;
				min-width: 36px;
                min-height: 36px;
            }
            #btn_zoom{
				min-width: 36px;
                min-height: 36px;
                margin-right: 3px;
                margin-left: 3px;
            }
			#btn_minimize{
				min-width: 36px;
                min-height: 36px;
			}
            QPushButton{
                border-radius: 10px;
                background-color: transparent;
            }
            QPushButton:hover{
                background-color: rgba(50, 50, 50, 100);
            }
			""")
		
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_1)
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.horizontalLayout_4.setContentsMargins(10, 15, 10, 5)
		self.horizontalLayout_4.setSpacing(20)

		self.frame_4 = QtWidgets.QFrame(self.widget_1)
		self.frame_4.setMinimumSize(QSize((self.size_frame-20), 35))
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
		self.horizontalLayout_4.addWidget(self.frame_4)
		spacerItem1 = QtWidgets.QSpacerItem(
			40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem1)
		
		self.btn_app_deb = QtWidgets.QPushButton(self.widget_1)
		self.btn_app_deb.setObjectName(u"btn_app_deb")
		self.btn_app_deb.setStyleSheet("""
									color: rgb(0, 0, 0);
									background-color: rgba(0, 255, 255, 160);
									border-color: #00ffff;
									border: 2px solid;
									border-radius: 15px;""")
		self.btn_app_deb.setIcon(QtGui.QIcon(QtGui.QPixmap(get_res('debian'))))
		self.btn_app_deb.setMinimumSize(QSize(150, 35))
		self.btn_app_deb.setEnabled(False)

		self.horizontalLayout_4.addWidget(self.btn_app_deb)

		self.label_3 = QtWidgets.QLabel(self.widget_1)
		self.label_3.setObjectName("label_3")
		font = QtGui.QFont()
		font.setPointSize(20)
		self.label_3.setFont(font)
		self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.horizontalLayout_4.addWidget(self.label_3)

		self.btn_app_flatpak = QtWidgets.QPushButton(self.widget_1)
		self.btn_app_flatpak.setObjectName(u"btn_app_flatpak")
		self.btn_app_flatpak.setStyleSheet("""
							background-color: rgb(169, 144, 122);
							color: #fff;
							border-color: #fff;
							border: 2px solid;
							border-radius: 15px;""")
		self.btn_app_flatpak.setIcon(QtGui.QIcon(QtGui.QPixmap(get_res('flatpak_sin_texto'))))
		self.btn_app_flatpak.setMinimumSize(QSize(150, 35))

		self.horizontalLayout_4.addWidget(self.btn_app_flatpak)


		spacerItem2 = QtWidgets.QSpacerItem(
			40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem2)

		self.btn_minimize = QtWidgets.QPushButton(self.widget_1)
		self.btn_minimize.setObjectName("btn_minimize")
		self.btn_minimize.setText("")
		icon12 = QtGui.QIcon()
		icon12.addPixmap(QtGui.QPixmap(svg_minimizar), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.btn_minimize.setIcon(icon12)
		self.btn_minimize.setIconSize(QSize(13, 13))
		self.horizontalLayout_4.addWidget(self.btn_minimize)

		self.btn_zoom = QtWidgets.QPushButton(self.widget_1)
		self.btn_zoom.setObjectName("btn_zoom")
		self.btn_zoom.setText("")
		icon13 = QtGui.QIcon()
		icon13.addPixmap(QtGui.QPixmap(svg_maximizar), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.btn_zoom.setIcon(icon13)
		self.horizontalLayout_4.addWidget(self.btn_zoom)

		self.btn_close = QtWidgets.QPushButton(self.widget_1)
		self.btn_close.setObjectName("btn_close")
		self.btn_close.setText("")
		icon14 = QtGui.QIcon()
		icon14.addPixmap(QtGui.QPixmap(svg_cerrar), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.btn_close.setIcon(icon14)
		self.btn_close.setIconSize(QSize(20, 20))

		self.horizontalLayout_4.addWidget(self.btn_close)

		self.gridLayout_2.addWidget(self.widget_1, 0, 0, 1, 2)
		self.setCentralWidget(MainWindow)

		self.retranslateUi(MainWindow)
		self.lw_categories.setCurrentRow(-1)
		QMetaObject.connectSlotsByName(MainWindow)

	def __tr(self, txt, disambiguation=None, n=-1):
		return tr(self, txt, disambiguation, n)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(self.__tr("Deepines Store"))
		self.label_2.setToolTip(self.__tr("About us"))
		self.label_3.setText(self.__tr("Deepines Store"))
		self.lbl_list_apps.setText(self.__tr("TextLabel"))
		self.btn_install.setText(self.__tr("Review apps"))
		__sortingEnabled = self.lw_categories.isSortingEnabled()
		self.lw_categories.setSortingEnabled(False)
		item = self.lw_categories.item(0)
		item.setText(self.__tr("Home"))
		item = self.lw_categories.item(1)
		item.setText(self.__tr("Deepines"))
		item = self.lw_categories.item(2)
		item.setText(self.__tr("Internet"))
		item = self.lw_categories.item(3)
		item.setText(self.__tr("Multimedia"))
		item = self.lw_categories.item(4)
		item.setText(self.__tr("Graphics"))
		item = self.lw_categories.item(5)
		item.setText(self.__tr("Games"))
		item = self.lw_categories.item(6)
		item.setText(self.__tr("Office automation"))
		item = self.lw_categories.item(7)
		item.setText(self.__tr("Development"))
		item = self.lw_categories.item(8)
		item.setText(self.__tr("System"))
		item = self.lw_categories.item(9)
		item.setText(self.__tr("Other"))
		item = self.lw_categories.item(10)
		item.setText(self.__tr(""))
		item = self.lw_categories.item(11)
		item.setText(self.__tr("Installed apps"))
		self.lw_categories.setSortingEnabled(__sortingEnabled)
		self.lineEdit.setPlaceholderText(self.__tr("Search"))
		self.about_version_text = self.__tr("About \nVersion: {version}")
		self.btn_minimize.setToolTip(self.__tr("Minimize"))
		self.btn_zoom.setToolTip(self.__tr("Zoom"))
		self.btn_close.setToolTip(self.__tr("Close"))
		self.label.setText(self.about_version_text.format(version=STORE_VERSION))
		self.btn_app_deb.setText(self.__tr("Apps .deb"))
		self.btn_app_flatpak.setText(self.__tr("Apps Flatpak"))
		
		
		# StoreWindow
		self.list_apps_text = self.__tr("Select the apps to install")
		self.select_app_text = self.__tr("Select")
		self.selected_to_install_app_text = self.__tr("Selected")
		self.selected_installed_app_text = self.__tr("Installed")
		self.uninstall_app_text = self.__tr("Uninstall")
		self.uninstalled_app_text = self.__tr("Uninstalled")
		self.single_app_text = self.__tr("{app_count} app selected, click here to review it")
		self.multi_apps_text = self.__tr("{app_count} apps selected, click here to review them")
		self.error_no_server_text = self.__tr("Unable to establish connection with the server, <br>"
											  "please check your internet connection.<br>"
											  "If the problem persists, please contact us via Telegram <br>"
											  "at {atTlURL}.<br><br>"
											  "Visit Deepin en Español for more information: {siteURL}").format(atTlURL=get_text_link("@deepinenespanol"), siteURL=get_text_link("deepinenespañol.org"))
		self.error_no_deepines_repo_text = self.__tr("Deepines repository is not installed on your system,<br>"
													 "Deepines Store needs this repository to work.<br>"
													 "In the following link you will find the instructions to install it:<br><br>"
													 "{repoURL}").format(repoURL=get_text_link("deepinenespañol.org/deepines/"))
