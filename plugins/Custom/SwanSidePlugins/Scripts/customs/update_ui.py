import sys


from qtpy.QtCore import *
from qtpy.QtWidgets import *
import swan_updatePrism as updater


class Worker(QThread):
    progressChanged = Signal(int, str)
    updateFinished = Signal()

    def run(self):
        self.progressChanged.emit(1, "Archiving the current pipeline...")
        updater.save_archive_curr_pipe()
        self.progressChanged.emit(50, "Downloading new pipeline...")
        zip_file = updater.download_and_unzip_last_pipe()
        self.progressChanged.emit(100, "Copy files...")

        github_folder = updater.get_downloaded_folder()
        self.progressChanged.emit(0, github_folder)
        for progress in updater.copy_files(github_folder):
            self.progressChanged.emit(progress, "Coping files...")

        self.progressChanged.emit(100, "Removed downloaded files.")
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
        self.resize(357, 150)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel("Une nouvelle version du pipeline est disponible.\nVoulez-vous le mettre à jour :", self)
        self.verticalLayout.addWidget(self.label)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.accepted.connect(self.onAccepted)
        self.buttonBox.rejected.connect(self.onRejected)
        self.verticalLayout.addWidget(self.buttonBox)

        self.progressBar = QProgressBar(self)
        self.progressBar.setVisible(False)
        self.verticalLayout.addWidget(self.progressBar)

        self.progressLabel = QLabel("", self)
        self.verticalLayout.addWidget(self.progressLabel)

        self.setWindowTitle("Dialog")

    def onAccepted(self):
        self.buttonBox.setEnabled(False)
        self.progressBar.setVisible(True)
        self.worker.start()

    def onRejected(self):
        self.reject()

    def updateProgress(self, value, msg):
        if value == 0:
            github_folder = updater.get_downloaded_folder()
            length = updater.length_files(github_folder)
            self.progressBar.setMaximum(length+1)
        else:
            self.progressBar.setValue(value)
        self.progressLabel.setText(msg)

    def onUpdateFinished(self):
        self.accept()
        QMessageBox.information(self, "Mise à jour", "La mise à jour est terminée avec succès.")


if __name__ == '__main__':


    app = QApplication(sys.argv)
    dialog = UpdateUi()
    dialog.show()
    sys.exit(app.exec_())
