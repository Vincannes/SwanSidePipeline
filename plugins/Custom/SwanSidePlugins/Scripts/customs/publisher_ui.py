#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import constants
import logging

try:
    from qtpy.QtCore import *
    from qtpy.QtGui import *
    from qtpy.QtWidgets import *
    from qtpy.QtSvg import *
    from qtpy.QtSvgWidgets import *
except:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtSvg import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

logger = logging.getLogger(__name__)

IMG_EXTENSIONS = ["png", "jpg", "dpx", "exr"]


class SwanSidePublisher(QDialog):

    def __init__(self, parent=None):
        super().__init__(None)
        self._parent = parent
        self._media = parent.media
        self._publisher = parent.publisher

        self.setupUi()
        self.set_connections()
        self.setWindowTitle('SwanSide SwanSidePlugins')

    def setupUi(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.btFile = QPushButton(self)
        self.btFile.setObjectName(u"btFile")

        self.horizontalLayout.addWidget(self.btFile)

        self.label_3 = QLabel(self)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.label_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.textBrowser = QPlainTextEdit(self)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(100, 250))

        self.verticalLayout_2.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.image = QLabel(self)
        self.image.setObjectName(u"image")
        self.image.setMinimumSize(QSize(250, 250))
        self.image.setMaximumSize(QSize(450, 250))
        self.image.setScaledContents(True)

        self.gridLayout.addWidget(self.image, 1, 1, 1, 1)

        self.publishBtn = QPushButton(self)
        self.gridLayout.addWidget(self.publishBtn, 2, 0, 1, 2)

        self.progressContainer = QVBoxLayout()
        self.progressContainer.setAlignment(Qt.AlignCenter)
        self.progressBar = BusyIndicator(self)
        self.progressBar.setFixedSize(80, 80)
        self.progressContainer.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.progressContainer, 3, 0, 1, 2, alignment=Qt.AlignCenter)

        self.label.setText("Path :")
        self.btFile.setText("Open")
        self.label_2.setText("Description :")
        self.image.setText("")
        self.lineEdit.setText("")
        self.publishBtn.setText("Publish")
        self.label_3.setText("Frame Range: 0-0")
        self.setMinimumSize(700, 450)

    def set_connections(self):
        self.btFile.clicked.connect(self._open_file_dialog)
        self.publishBtn.clicked.connect(self._publishing)

    # PRIVATES

    @err_catcher(name=__name__)
    def _open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()", "", "All Files (*)",
            options=options
        )
        if not file_path:
            self.lineEdit.setText("")
            self.label_3.setText("Frame Range: 0-0")
            return

        _, file_extension = os.path.splitext(file_path)
        frame_range = self._media.get_first_last_frames(
            os.path.dirname(file_path), file_extension
        )
        self.lineEdit.setText(file_path)
        self.label_3.setText("Frame Range: {}-{}".format(frame_range[0], frame_range[1]))

        # Convert exr to png
        if file_extension == ".exr":
            filename = self._media.generate_tmp_file()
            tmp_png = os.path.join(
                os.path.dirname(filename), os.path.basename(filename) + ".png"
            )
            file_path = file_path.replace("&", "^&")
            cmds = [
                "-y", "-i",
                f"{file_path}",
                f"{tmp_png}"
            ]
            try:
                self._media.process_custom_ffmpeg(cmds)
                file_path = tmp_png
            except RuntimeError as e:
                self.image.setText("Impossible de charger l'image:\n{}".format(e))

        # set Thumbnail
        pixmap = QPixmap(file_path)
        self.image.setPixmap(pixmap)
        self.image.setMinimumSize(1, 1)

    @err_catcher(name=__name__)
    def _publishing(self):
        self.publishBtn.setText("Publishing.....")
        description = self.textBrowser.toPlainText()
        path = self.lineEdit.text()
        self.progressBar.show()

        self.thread = PublishingThread(
            parent=self._parent,
            path=path,
            comment=description,
            publisher=self._publisher,
            media_processor=self._media
        )
        self.thread.finished.connect(self._on_publishing_finished)
        self.thread.error.connect(self._on_publishing_error)
        self.thread.start()

    def _on_publishing_finished(self, result):
        logger.info(result)
        QMessageBox.information(None, "Publish Completed", f"Publishing completed:\n{result}")
        self.publishBtn.setText("Publish")
        self.close()

    def _on_publishing_error(self, exception):
        QMessageBox.critical(None, "Publish Failed", f"Error during publishing:\n{str(exception)}")


class PublishingThread(QThread):
    finished = Signal(str)
    error = Signal(Exception)

    def __init__(self, parent, path, comment, publisher, media_processor):
        super(PublishingThread, self).__init__()
        self.path = path
        self.comment = comment
        self.publisher = publisher
        self.media_processor = media_processor
        self.parent = parent

    def run(self):
        preview_file = self.path
        try:
            if any([self.path.endswith(ext) for ext in IMG_EXTENSIONS]):
                try:
                    preview_file = self.media_processor.process_mov_file_from_sequence(self.path)
                except RuntimeError as e:
                    print(f"Error during processing: {str(e)}")

            fields = self.parent.get_fields_from_path(self.path)
            entity_type = fields.get("type")
            msg = (
                f"Process Publish {entity_type}   name: {fields.get(entity_type)}   "
                f"task: {fields.get('task')}\n{self.path}\n{self.comment}\n{preview_file}"
            )

            logger.debug(msg)

            result = self.publisher.publish(
                shot=fields.get(entity_type),
                task=fields.get("task"),
                path=self.path,
                entity=entity_type,
                status="wfa",
                comment=self.comment,
                preview_file=preview_file,
            )

            logger.debug(result)
            self.finished.emit(result)
        except Exception as e:
            logger.error(f"Failed: {str(e)}")
            self.error.emit(e)


class BusyIndicator(QWidget):
    def __init__(self, parent=None):
        super(BusyIndicator, self).__init__(parent)
        self.resize(80, 80)
        layout = QHBoxLayout()
        svg = QSvgWidget()
        icon_path = os.path.join(
            os.path.dirname(constants.SCRIPTS_DIR),
            "resources", "tail-spin.svg"
        )
        svg.load(icon_path)
        layout.addWidget(svg)
        self.setLayout(layout)

        self.hide()

    def show(self):
        self.move(self.parent().rect().center() - self.rect().center())
        super(BusyIndicator, self).show()

    def hide(self):
        super(BusyIndicator, self).hide()

    def paintEvent(self, event):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    publ = SwanSidePublisher(None)
    publ.show()
    app.exec_()
