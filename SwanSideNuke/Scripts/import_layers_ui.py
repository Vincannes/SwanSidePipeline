# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_layers_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(698, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(250, 16777215))
        self.assetTab = QWidget()
        self.assetTab.setObjectName(u"assetTab")
        self.verticalLayout_2 = QVBoxLayout(self.assetTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.assetListWidget = QListWidget(self.assetTab)
        self.assetListWidget.setObjectName(u"assetListWidget")

        self.verticalLayout_2.addWidget(self.assetListWidget)

        self.tabWidget.addTab(self.assetTab, "")
        self.shotTab = QWidget()
        self.shotTab.setObjectName(u"shotTab")
        self.verticalLayout = QVBoxLayout(self.shotTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.shotListWidget = QListWidget(self.shotTab)
        self.shotListWidget.setObjectName(u"shotListWidget")

        self.verticalLayout.addWidget(self.shotListWidget)

        self.tabWidget.addTab(self.shotTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        self.dataTableWidget = QTableWidget(self.centralwidget)
        self.dataTableWidget.setObjectName(u"dataTableWidget")

        self.horizontalLayout.addWidget(self.dataTableWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.assetTab), QCoreApplication.translate("MainWindow", u"Assets", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shotTab), QCoreApplication.translate("MainWindow", u"Shots", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select 3D layers to import ", None))
    # retranslateUi

