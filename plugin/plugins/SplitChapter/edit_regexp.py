# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_regexp.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_edit_regexp(object):
    def setupUi(self, edit_regexp):
        edit_regexp.setObjectName("edit_regexp")
        edit_regexp.setWindowModality(QtCore.Qt.ApplicationModal)
        edit_regexp.resize(423, 221)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        edit_regexp.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(edit_regexp)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.exp_listview = QtWidgets.QListWidget(edit_regexp)
        self.exp_listview.setStyleSheet("alternate-background-color:rgb(235, 235, 235);")
        self.exp_listview.setAlternatingRowColors(True)
        self.exp_listview.setObjectName("exp_listview")
        self.verticalLayout.addWidget(self.exp_listview)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.toolButton_4 = QtWidgets.QToolButton(edit_regexp)
        self.toolButton_4.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/arrow-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon1)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout.addWidget(self.toolButton_4)
        self.toolButton = QtWidgets.QToolButton(edit_regexp)
        self.toolButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/arrow-down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon2)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.toolButton_2 = QtWidgets.QToolButton(edit_regexp)
        self.toolButton_2.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_2.setIcon(icon3)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout.addWidget(self.toolButton_2)
        self.toolButton_3 = QtWidgets.QToolButton(edit_regexp)
        self.toolButton_3.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_3.setIcon(icon4)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout.addWidget(self.toolButton_3)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(3, 4)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(edit_regexp)
        self.toolButton_4.clicked.connect(edit_regexp.move_up_item) # type: ignore
        self.toolButton.clicked.connect(edit_regexp.move_down_item) # type: ignore
        self.toolButton_2.clicked.connect(edit_regexp.add_item) # type: ignore
        self.toolButton_3.clicked.connect(edit_regexp.dec_item) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(edit_regexp)

    def retranslateUi(self, edit_regexp):
        _translate = QtCore.QCoreApplication.translate
        edit_regexp.setWindowTitle(_translate("edit_regexp", "编辑预置正则"))
import res_rc
