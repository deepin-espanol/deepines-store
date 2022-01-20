# -*- coding: utf-8 -*-

# UI Source 'guis/dialog_install.ui'


from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(547, 331)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.boton_install = QtWidgets.QPushButton(Form)
        self.boton_install.setObjectName("boton_install")
        self.gridLayout.addWidget(self.boton_install, 1, 0, 1, 1)
        self.boton = QtWidgets.QPushButton(Form)
        self.boton.setObjectName("boton")
        self.gridLayout.addWidget(self.boton, 1, 1, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.boton_install.setText(_translate("Form", "Install"))
        self.boton.setText(_translate("Form", "Close"))
