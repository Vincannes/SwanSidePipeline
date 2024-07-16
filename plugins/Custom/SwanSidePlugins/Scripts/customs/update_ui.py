
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

class UpdateUi(QDialog):

    def __init__(self, funct, parent=None):
        super(UpdateUi, self).__init__(parent)
        self.funct = funct
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(357, 80)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel("Une nouvelle version du pipeline est disponible.\nVoulez vous le mettre à jour :", self)
        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.onAccepted)
        self.buttonBox.rejected.connect(self.onRejected)
        self.verticalLayout.addWidget(self.buttonBox)

        self.setWindowTitle("Dialog")

    def onAccepted(self):
        self.funct()
        self.accept()

    def onRejected(self):
        self.reject()
