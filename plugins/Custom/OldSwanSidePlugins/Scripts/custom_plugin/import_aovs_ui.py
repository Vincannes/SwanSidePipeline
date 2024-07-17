# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_aovs_ui.ui'
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
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMaximumSize(QSize(250, 16777215))
        self.assetTab = QWidget()
        self.assetTab.setObjectName(u"assetTab")
        self.verticalLayout = QVBoxLayout(self.assetTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = QListWidget(self.assetTab)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.tabWidget.addTab(self.assetTab, "")
        self.shotTab = QWidget()
        self.shotTab.setObjectName(u"shotTab")
        self.verticalLayout_2 = QVBoxLayout(self.shotTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listWidget_2 = QListWidget(self.shotTab)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.verticalLayout_2.addWidget(self.listWidget_2)

        self.tabWidget.addTab(self.shotTab, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Policy.Maximum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_3.addWidget(self.tableWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.processBtn = QPushButton(self.centralwidget)
        self.processBtn.setObjectName(u"processBtn")

        self.horizontalLayout.addWidget(self.processBtn)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.assetTab), QCoreApplication.translate("MainWindow", u"Assets", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shotTab), QCoreApplication.translate("MainWindow", u"Shots", None))
        self.processBtn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

