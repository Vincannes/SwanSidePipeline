#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import utils
import logging

try:
    from qtpy.QtCore import *
    from qtpy.QtGui import *
    from qtpy.QtWidgets import *
except:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *


class SwanSideLoginUI(QDialog):

    def __init__(self, user_conf):
        super().__init__(None)
        self.user_conf_file = user_conf
        self.buildUI()

    def buildUI(self):
        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 150)
        self.center()

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()

        email_label = QLabel("Mail :")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your_mail@gmail.com")
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)

        password_label = QLabel("Password :")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.acceptBtn)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        hlayout.addWidget(self.ok_button)
        hlayout.addWidget(self.cancel_button)
        layout.addLayout(hlayout)

        self.setLayout(layout)

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def acceptBtn(self):
        data = {
            "credentials": {
                "mail": self.email_input.text(),
                "password": self.password_input.text()
            }
        }
        utils.writeConfig(self.user_conf_file, data)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    publ = SwanSideLoginUI(None)
    publ.show()
    app.exec_()
