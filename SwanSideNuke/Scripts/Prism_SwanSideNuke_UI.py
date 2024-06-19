#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import re

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from import_layers_ui import Ui_MainWindow


# C:\Users\User\AppData\Local\Programs\Python\Python37\Scripts\pyside2-uic C:\ProgramData\Prism2\plugins\Custom\SwanSideNuke\Scripts\ui\import_layers_ui.ui -o C:\ProgramData\Prism2\plugins\Custom\SwanSideNuke\Scripts\import_layers_ui.py

def get_version_from_filename(filename):
    version_pattern = r'_v(\d{4})_'
    match = re.search(version_pattern, filename)

    if match:
        return int(match.group(1))
    else:
        return None


class ReadManagerUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.files = files

        self.setupUi(self)
        self.load_ui()

        self.tabWidget.currentChanged.connect(self.getCurrentTab)
        self.assetListWidget.itemSelectionChanged.connect(
            lambda: self.getCurrentEntity(self.assetListWidget.selectedItems())
        )
        self.shotListWidget.itemSelectionChanged.connect(
            lambda: self.getCurrentEntity(self.shotListWidget.selectedItems())
        )
        self.pushButton.clicked.connect(self.importLayers)

    def load_ui(self):
        for asset, files in self.files.get("Assets").items():
            self.assetListWidget.addItem(asset)
        for shot, files in self.files.get("Shots").items():
            self.shotListWidget.addItem(shot)

        self.dataTableWidget.setColumnCount(3)
        self.dataTableWidget.setHorizontalHeaderLabels(["Name", "Version", "Extension"])
        self.dataTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def getCurrentTab(self, index):
        tab_text = self.tabWidget.tabText(index)

    def getCurrentEntity(self, selected_items):
        if not selected_items:
            return
        item = selected_items[0].text()
        self.loadScenes(item)

    def loadScenes(self, shot_item):
        self.dataTableWidget.clearContents()
        for shot, files in self.files.get("Shots").items():
            if shot != shot_item:
                continue
            self.dataTableWidget.setRowCount(len(files))

            for row, item in enumerate(files):
                basename = os.path.basename(item).split(".")[0]
                version = get_version_from_filename(os.path.basename(item))
                ext = os.path.basename(item).split(".")[-1]
                item_widget = QtWidgets.QTableWidgetItem(basename)
                item_widget.setData(QtCore.Qt.UserRole, item)
                self.dataTableWidget.setItem(row, 0, item_widget)
                self.dataTableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(version)))
                self.dataTableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(ext))

        self.dataTableWidget.resizeColumnsToContents()

    def importLayers(self):
        selected_item = self.dataTableWidget.selectedItems()
        if not selected_item:
            return
        row = selected_item[0].row()
        selected_data = self.dataTableWidget.item(row, 0).text()
        path = self.dataTableWidget.item(row, 0).data(QtCore.Qt.UserRole)
        print(selected_data)
        print(path)


if __name__ == "__main__":
    import sys

    files = {
        "Assets": {},
        "Shots": {
            'vinc_sh_010': [],
            'vinc_sh_020': [
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0001\\beauty\\vinc-vinc_sh_020_Animation_v0001_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0002\\beauty\\vinc-vinc_sh_020_Animation_v0002_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0003\\beauty\\vinc-vinc_sh_020_Animation_v0003_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0004\\beauty\\vinc-vinc_sh_020_Animation_v0004_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0005\\beauty\\vinc-vinc_sh_020_Animation_v0005_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0006\\beauty\\vinc-vinc_sh_020_Animation_v0006_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0007\\beauty\\vinc-vinc_sh_020_Animation_v0007_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0008\\beauty\\vinc-vinc_sh_020_Animation_v0008_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0009\\beauty\\vinc-vinc_sh_020_Animation_v0009_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0010\\beauty\\vinc-vinc_sh_020_Animation_v0010_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0011\\beauty\\vinc-vinc_sh_020_Animation_v0011_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0012\\beauty\\vinc-vinc_sh_020_Animation_v0012_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0013\\beauty\\vinc-vinc_sh_020_Animation_v0013_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0014\\beauty\\vinc-vinc_sh_020_Animation_v0014_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0015\\beauty\\vinc-vinc_sh_020_Animation_v0015_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0016\\beauty\\vinc-vinc_sh_020_Animation_v0016_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0017\\beauty\\vinc-vinc_sh_020_Animation_v0017_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0018\\beauty\\vinc-vinc_sh_020_Animation_v0018_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0019\\beauty\\vinc-vinc_sh_020_Animation_v0019_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0020\\beauty\\vinc-vinc_sh_020_Animation_v0020_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0021\\beauty\\vinc-vinc_sh_020_Animation_v0021_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0022\\beauty\\vinc-vinc_sh_020_Animation_v0022_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0023\\beauty\\vinc-vinc_sh_020_Animation_v0023_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0024\\beauty\\vinc-vinc_sh_020_Animation_v0024_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0025\\beauty\\vinc-vinc_sh_020_Animation_v0025_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0027\\beauty\\vinc-vinc_sh_020_Animation_v0027_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0029\\beauty\\vinc-vinc_sh_020_Animation_v0029_beauty.%04d.exr',
                'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0031\\beauty\\vinc-vinc_sh_020_Animation_v0031_beauty.%04d.exr']
        }
    }

    app = QtWidgets.QApplication(sys.argv)
    main_window = ReadManagerUI(files)
    main_window.show()
    sys.exit(app.exec_())
