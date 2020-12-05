# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guis/main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from os.path import join, abspath, dirname


class QLabelClickable(QtWidgets.QLabel):

    clicked = QtCore.pyqtSignal()
    
    def __init__(self, *args):
        QtWidgets.QLabel.__init__(self, *args)
   
    def mouseReleaseEvent(self, ev):
        self.clicked.emit()

class Ui_MainWindow(object):
    def __init__(self, width, height):
        #print("El ancho del monitor es: {}".format(width))

        self.width_screen = int(width * 0.7)
        if self.width_screen < 945: self.width_screen = 945
        #print("El width_screen ({}*0.7) es: {}".format(width, self.width_screen))

        self.height_screen = int(height * 0.85)
        if self.height_screen < 700: self.height_screen = 700
        #print("El height_screen ({}*0.8) es: {}".format(height, self.height_screen))

        self.size_frame = int(width * 0.14)
        if self.size_frame < 200: self.size_frame = 200
        if self.size_frame > 300: self.size_frame = 300
        #print("El frame ({}*0.14) es: {}".format(width, self.size_frame))

    def setupUi(self, MainWindow):
        ruta_logo = abspath(join(dirname(__file__), 'resources', 'deepines.svg'))
        ruta_fondo = abspath(join(dirname(__file__), 'resources', 'icono.svg'))
        ruta_star = abspath(join(dirname(__file__), 'resources', 'star.svg'))
        ruta_deepines = abspath(join(dirname(__file__), 'resources', 'deepines_filter.svg'))
        ruta_internet = abspath(join(dirname(__file__), 'resources', 'internet.svg'))
        ruta_music = abspath(join(dirname(__file__), 'resources', 'music.svg'))
        ruta_picture = abspath(join(dirname(__file__), 'resources', 'picture.svg'))
        ruta_console = abspath(join(dirname(__file__), 'resources', 'console.svg'))
        ruta_board = abspath(join(dirname(__file__), 'resources', 'board.svg'))
        ruta_terminal = abspath(join(dirname(__file__), 'resources', 'terminal.svg'))
        ruta_computer = abspath(join(dirname(__file__), 'resources', 'computer.svg'))
        ruta_pamela = abspath(join(dirname(__file__), 'resources', 'pamela.svg'))
        ruta_search = abspath(join(dirname(__file__), 'resources', 'magnifying-glass.svg'))
        ruta_car = abspath(join(dirname(__file__), 'resources', 'carDisable.svg'))
        ruta_minimizar = abspath(join(dirname(__file__), 'resources', 'minimizar.svg'))
        ruta_maximizar = abspath(join(dirname(__file__), 'resources', 'maximizar.svg'))
        ruta_cerrar = abspath(join(dirname(__file__), 'resources', 'cerrar.svg'))

        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(self.width_screen, self.height_screen))
        MainWindow.resize(self.width_screen, self.height_screen)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ruta_logo), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QScrollBar:vertical {\n"
            "    background: transparent;\n"
            "    width: 10px;\n"
            "    margin: 0px 0px 0px 0px;\n"
            "}\n"
            "QScrollBar::handle:vertical {\n"
            "    background-color: #545454;\n"
            "    border-radius: 4px;\n"
            "    min-height: 5px;\n"
            "}\n"
            "QScrollBar::add-line:vertical {\n"
            "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
            "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
            "    height: 0px;\n"
            "    subcontrol-position: bottom;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::sub-line:vertical {\n"
            "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
            "    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));\n"
            "    height: 0 px;\n"
            "    subcontrol-position: top;\n"
            "    subcontrol-origin: margin;\n"
        "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgba(30, 30, 30, 200);"
            "color: #b5c5d1;")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Frame apps seleccionadas
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 80))
        self.widget.setStyleSheet("background-color: rgba(16, 16, 16, 0);")
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        
        self.icon_car = QLabelClickable(self.widget)
        self.icon_car.setStyleSheet("margin-left: 0px;\n"
        "background-color: transparent;\n"
        "border-color: transparent;\n"
        
        "border: 0px solid;")
        self.icon_car.setText("")
        pix_car = QtGui.QPixmap(ruta_car)
        self.icon_car.setPixmap(pix_car)
        self.icon_car.setScaledContents(True)
        self.icon_car.setMinimumSize(QtCore.QSize(20, 20))
        self.icon_car.setMaximumSize(QtCore.QSize(20, 20))
        
        self.icon_car.setObjectName("icon_car")
        self.horizontalLayout_3.addWidget(self.icon_car)
        self.lbl_list_apps = QLabelClickable(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_list_apps.setFont(font)
        self.lbl_list_apps.setStyleSheet("background-color: transparent;\n"
"")
        self.lbl_list_apps.setObjectName("lbl_list_apps")
        self.horizontalLayout_3.addWidget(self.lbl_list_apps)
        self.btn_install = QtWidgets.QPushButton(self.widget)
        self.btn_install.setMinimumSize(QtCore.QSize(80, 0))
        self.btn_install.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_install.setStyleSheet("#btn_install{\n"
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
        self.frame_2.setMinimumSize(QtCore.QSize(self.size_frame, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(self.size_frame, 16777215))
        self.frame_2.setStyleSheet("background-color: rgba(16, 16, 16, 0);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        # Primer item, spaciador vertical
        self.verticalLayout.addItem(spacerItem2)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 35))
        self.frame_4.setStyleSheet("border-radius: 10px;\n"
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
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.frame_4)
        self.pushButton.setStyleSheet("margin-left: 0px;\n"
"background-color: transparent;\n"
"border-color: transparent;\n"
"border: 0px solid;")
        self.pushButton.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(ruta_search), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon11)
        self.pushButton.setIconSize(QtCore.QSize(13, 13))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        # Segundo item, cuadro busqueda
        self.verticalLayout.addWidget(self.frame_4)
        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setStyleSheet("#listWidget{\n"
"  padding-left:10px;\n"
"  padding-top:6px;\n"
"  padding-bottom:6px;\n"
"  border-radius: 10px;\n"
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
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setAutoScroll(False)
        self.listWidget.setIconSize(QtCore.QSize(24, 24))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(ruta_star), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(ruta_deepines), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(ruta_internet), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(ruta_music), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon4)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(ruta_picture), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon5)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(ruta_console), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon6)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(ruta_board), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon7)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(ruta_terminal), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon8)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(ruta_computer), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon9)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(ruta_pamela), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon10)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
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
        self.label_2 = QLabelClickable(self.widget_2)
        self.label_2.setMinimumSize(QtCore.QSize(180, 180))
        self.label_2.setMaximumSize(QtCore.QSize(180, 180))
        self.label_2.setStyleSheet("background-color: transparent;")
        self.label_2.setText("")
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_2.setPixmap(QtGui.QPixmap(ruta_fondo))
        self.label_2.setToolTip("Acerca de nosotros")
        self.label_2.setScaledContents(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        # Cuarto item, img deepines
        self.verticalLayout.addWidget(self.widget_2)
        self.label = QLabelClickable(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: transparent;\n")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label.setObjectName("label")
        # Quinto item, label version
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 2, 1)
        self.frame = QtWidgets.QScrollArea(self.centralwidget)
        self.frame.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.frame.setWidgetResizable(True)
        self.frame.setAlignment(QtCore.Qt.AlignCenter)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color: rgba(16, 16, 16, 0);")
        self.scroll_apps = QtWidgets.QWidget()
        self.scroll_apps.setGeometry(QtCore.QRect(0, 0, 774, 459))
        self.scroll_apps.setObjectName("scroll_apps")
        self.scroll_apps.setStyleSheet("#scroll_apps{ padding-left: 30px; padding-right: 30px;}")
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
                background-color: rgba(16, 16, 16, 180);
            }
            #label_3{
                background-color: transparent;
            }
            #btn_cerrar{
                margin-right: 10px;
            }
            #btn_maximizar{
                margin-right: 3px;
                margin-left: 3px;
            }
            QPushButton{
                min-width: 36px;
                min-height: 36px;
                border-radius: 10px;
                background-color: transparent;
            }
            QPushButton:hover{
                background-color: rgba(50, 50, 50, 100);
            }
            """)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0,5,0,5)
        self.horizontalLayout_4.setSpacing(1)
        
        spacerItem = QtWidgets.QSpacerItem(130, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)

        self.label_3 = QtWidgets.QLabel(self.widget_1)
        self.label_3.setObjectName("label_3")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setText("Tienda Deepines")
        self.horizontalLayout_4.addWidget(self.label_3)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)

        self.btn_minimizar= QtWidgets.QPushButton(self.widget_1)
        self.btn_minimizar.setObjectName("btn_minimizar")
        self.btn_minimizar.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(ruta_minimizar), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_minimizar.setIcon(icon12)
        self.btn_minimizar.setIconSize(QtCore.QSize(13, 13))
        self.horizontalLayout_4.addWidget(self.btn_minimizar)

        self.btn_maximizar = QtWidgets.QPushButton(self.widget_1)
        self.btn_maximizar.setObjectName("btn_maximizar")
        self.btn_maximizar.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(ruta_maximizar), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_maximizar.setIcon(icon13)
        self.horizontalLayout_4.addWidget(self.btn_maximizar)

        self.btn_cerrar = QtWidgets.QPushButton(self.widget_1)
        self.btn_cerrar.setObjectName("btn_cerrar")
        self.btn_cerrar.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(ruta_cerrar), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cerrar.setIcon(icon14)
        self.btn_cerrar.setIconSize(QtCore.QSize(20, 20))

        self.horizontalLayout_4.addWidget(self.btn_cerrar)
        self.gridLayout_2.addWidget(self.widget_1, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.listWidget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tienda Deepines"))
        self.lbl_list_apps.setText(_translate("MainWindow", "TextLabel"))
        self.btn_install.setText(_translate("MainWindow", "Instalar"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Inicio"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Deepines"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Internet"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Multimedia"))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "Gráficos"))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "Juegos"))
        item = self.listWidget.item(6)
        item.setText(_translate("MainWindow", "Ofimática"))
        item = self.listWidget.item(7)
        item.setText(_translate("MainWindow", "Desarrollo"))
        item = self.listWidget.item(8)
        item.setText(_translate("MainWindow", "Sistema"))
        item = self.listWidget.item(9)
        item.setText(_translate("MainWindow", "Otros"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Búsqueda"))
        self.label.setText(_translate("MainWindow", "Acerca de \nVersion: 1.3.3"))
