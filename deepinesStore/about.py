#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: FramelessDialog
@description: 无边框圆角对话框 
"""
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget,\
    QPushButton, QGridLayout, QSpacerItem,\
    QSizePolicy, QLabel, QFrame, QSizePolicy, QDesktopWidget
from PyQt5.QtGui import QFont, QPixmap
from os import system
from os.path import join, abspath, dirname

Stylesheet = """

#Custom_Dialog{
  background-color: transparent;
  border-radius: 10px;
}

#Custom_Widget{
  background-color: rgba(30, 30, 30, 150);
}

#label_3{
    margin-bottom: 10px;
}
#label_14{
    margin-top: 10px;
}

#label, #label_2, #label_3,
#label_4, #label_5, #label_6,
#label_7, #label_8, #label_9,
#label_10, #label_11, #label_12,
#label_13, #label_14{
  color: white;  
}

#frame{
  border: transparent;
}

#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
    margin-top: 5px;
    margin-right: 5px;
}
#closeButton:hover {
    color: white;
    background: red;
}
"""


class Dialog(QDialog):

  def __init__(self, width, height):
    super(Dialog, self).__init__()
    self.setObjectName('Custom_Dialog')
    self.calcular_tamanio(width, height)
    #self.setMinimumSize(QSize(r_width, r_height))
    #self.setMaximumSize(QSize(r_width, r_height))
    self.resize(r_width, r_height)
    self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
    self.setAttribute(Qt.WA_TranslucentBackground, True )
    self.setStyleSheet(Stylesheet)
    self.initUi()
    self.center()
    
    system('xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {}'.format(int(self.winId())))

  def initUi(self):
    ruta_logo = abspath(join(dirname(__file__), 'resources', 'deepines.svg'))

    self.gridLayout = QGridLayout(self)
    self.gridLayout.setContentsMargins(0, 0, 0, 0)
    self.gridLayout.setSpacing(0)
    self.gridLayout.setObjectName("gridLayout")
    self.widget = QWidget(self)
    self.widget.setObjectName("Custom_Widget")

    self.verticalLayout = QVBoxLayout(self.widget)
    self.verticalLayout.setContentsMargins(30, 0, 30, 30)
    self.verticalLayout.setSpacing(0)
    self.verticalLayout.setObjectName("verticalLayout")

    self.verticalLayout_2 = QHBoxLayout()
    self.verticalLayout_2.setObjectName("verticalLayout_2")
    self.verticalLayout_2.addItem(QSpacerItem(
        40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    self.verticalLayout_2.addWidget(QPushButton(
        'r', self, clicked=self.accept, objectName='closeButton'))

    self.verticalLayout.addLayout(self.verticalLayout_2)
    spacerItem2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
    self.verticalLayout.addItem(spacerItem2)
    self.label_2 = QLabel(self)
    font = QFont()
    font.setPointSize(20)
    self.label_2.setFont(font)
    self.label_2.setAlignment(Qt.AlignCenter)
    self.label_2.setText("Tienda Deepines")
    self.label_2.setObjectName("label_2")
    self.verticalLayout.addWidget(self.label_2)
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
    self.label.setPixmap(QPixmap(ruta_logo))
    self.label.setObjectName("label")
    self.horizontalLayout.addWidget(self.label)
    self.verticalLayout.addWidget(self.frame)
    self.label_3 = QLabel(self)
    font = QFont()
    font.setPointSize(14)
    self.label_3.setFont(font)
    self.label_3.setAlignment(Qt.AlignCenter)
    self.label_3.setWordWrap(True)
    self.label_3.setText("Desarrollado por la comunidad de Deepin en Español")
    self.label_3.setObjectName("label_3")
    self.verticalLayout.addWidget(self.label_3)
    font = QFont()
    font.setPointSize(12)
    self.label_6 = QLabel(self)
    self.label_6.setFont(font)
    self.label_6.setAlignment(Qt.AlignCenter)
    self.label_6.setObjectName("label_6")
    self.label_6.setText("Proyecto: Car @Xhafas ")
    self.verticalLayout.addWidget(self.label_6)
    self.label_4 = QLabel(self)
    self.label_4.setAlignment(Qt.AlignCenter)
    self.label_4.setFont(font)
    self.label_4.setText("Desarrollo: Sebastian @SebTrujillo")
    self.label_4.setObjectName("label_4")
    self.verticalLayout.addWidget(self.label_4)
    self.label_7 = QLabel(self)
    self.label_7.setAlignment(Qt.AlignCenter)
    self.label_7.setObjectName("label_7")
    self.label_7.setFont(font)
    self.label_7.setText("Interfaz: Freddy @Akibaillusion")
    self.verticalLayout.addWidget(self.label_7)
    self.label_10 = QLabel(self)
    self.label_10.setAlignment(Qt.AlignCenter)
    self.label_10.setFont(font)
    self.label_10.setText("Redaccion: Isaías @igatjens")
    self.label_10.setObjectName("label_10")
    self.verticalLayout.addWidget(self.label_10)
    self.label_8 = QLabel(self)
    self.label_8.setAlignment(Qt.AlignCenter)
    self.label_8.setText("Diseño: Jhalo @jhalo; @Dziban; Alejandro @durantdurant")
    self.label_8.setObjectName("label_8")
    self.label_8.setFont(font)
    self.verticalLayout.addWidget(self.label_8)
    self.label_9 = QLabel(self)
    self.label_9.setAlignment(Qt.AlignCenter)
    self.label_9.setFont(font)
    self.label_9.setText("Sys Admin: Jose @fenoll; Hugo @geekmidget")
    self.label_9.setObjectName("label_9")
    self.verticalLayout.addWidget(self.label_9)
    self.label_11 = QLabel(self)
    self.label_11.setAlignment(Qt.AlignCenter)
    self.label_11.setFont(font)
    self.label_11.setText("Web: Eli @RealAct; Diego @s_d1112")
    self.label_11.setObjectName("label_11")
    self.verticalLayout.addWidget(self.label_11)
    self.label_12 = QLabel(self)
    self.label_12.setAlignment(Qt.AlignCenter)
    self.label_12.setFont(font)
    self.label_12.setText("Servidores: @filhoarrais; Bruno @bigbruno")
    self.label_12.setObjectName("label_12")
    self.verticalLayout.addWidget(self.label_12)
    self.label_13 = QLabel(self)
    self.label_13.setAlignment(Qt.AlignCenter)
    self.label_13.setFont(font)
    self.label_13.setText("Colaboradores: Alvaro @G4SP3R; Omi @peteromio; Opik @Prophaniti ; Pablo @dev86x; Jose @ProgramacionJS; Jorge @seiyukaras; @n1coc4cola; Oscar @oscararg; Jorge @jotakenobi")
    self.label_13.setObjectName("label_13")
    self.label_13.setWordWrap(True)
    self.verticalLayout.addWidget(self.label_13)
    self.label_14 = QLabel(self)
    self.label_14.setAlignment(Qt.AlignCenter)
    self.label_14.setFont(font)
    self.label_14.setText("deepinenespañol.org")
    self.label_14.setObjectName("label_14")
    self.verticalLayout.addWidget(self.label_14)
    self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)



  def calcular_tamanio(self, width, height):
    global r_width, r_height
    r_width = width * 0.6
    r_height = height * 0.9

  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
