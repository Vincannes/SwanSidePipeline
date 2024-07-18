import swan_updatePrism as updater

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Worker(QThread):
    progressChanged = Signal(int)
    updateFinished = Signal()

    def run(self):
        updater.save_archive_curr_pipe()
        zip_file = updater.download_and_unzip_last_pipe()
        github_folder = updater.get_downloaded_folder()

        length = updater.length_files(github_folder)
        self.progressChanged.emit(0)

        for progress in updater.copy_files(github_folder):
            self.progressChanged.emit(progress)

        updater.remove_downloaded_file(zip_file, github_folder)
        self.updateFinished.emit()


class UpdateUi(QDialog):

    def __init__(self, parent=None):
        super(UpdateUi, self).__init__(parent)
        self.setupUi()
        self.worker = Worker()
        self.worker.progressChanged.connect(self.updateProgress)
        self.worker.updateFinished.connect(self.onUpdateFinished)

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

        self.progressBar = QProgressBar(self)
        self.verticalLayout.addWidget(self.progressBar)

        self.setWindowTitle("Dialog")

    def onAccepted(self):

        for progress in updater.copy_files(github_folder):
            self.progress_bar.setValue(progress)

        updater.remove_downloaded_file(zip_file, github_folder)

        self.buttonBox.setEnabled(False)  # Disable buttons during update
        self.worker.start()

    def onRejected(self):
        self.reject()

    def updateProgress(self, value):
        if value == 0:  # This is the signal to set the max value of the progress bar
            github_folder = updater.get_downloaded_folder()
            length = updater.length_files(github_folder)
            self.progressBar.setMaximum(length)

        else:
            self.progressBar.setValue(value)

    def onUpdateFinished(self):
        self.accept()
        QMessageBox.information(self, "Mise à jour", "La mise à jour est terminée avec succès.")

