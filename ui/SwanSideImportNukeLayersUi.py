#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import re
import sys
from pprint import pprint

from PySide2 import QtWidgets, QtCore, QtGui

from import_aovs_ui import Ui_MainWindow


# C:\Users\User\AppData\Local\Programs\Python\Python37\Scripts\pyside2-uic.exe C:\ProgramData\Prism2\plugins\Custom\ui\import_aovs_ui.ui -o C:\ProgramData\Prism2\plugins\Custom\ui\import_aovs_ui.py

def get_version_from_filename(filename):
    version_pattern = r'_v(\d{4})_'
    match = re.search(version_pattern, filename)

    if match:
        return int(match.group(1))
    else:
        return None


class ImportNukeLayers(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.data = data

        self.processBtn.clicked.connect(self.process_import)
        self.listWidget.itemSelectionChanged.connect(lambda: self.on_selection_changed(self.listWidget))
        self.listWidget_2.itemSelectionChanged.connect(lambda: self.on_selection_changed(self.listWidget_2))
        self.loadUi()

    def loadUi(self):
        self.processBtn.setText("Process Layers..")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Version", "Extension"])
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.load_entity()

    def load_entity(self):
        assets = self.data.get("Assets")
        for asset_name, files in assets.items():
            self.listWidget.addItem(asset_name)
        shots = self.data.get("Shots")
        for shot_name, files in shots.items():
            self.listWidget_2.addItem(shot_name)

    def on_selection_changed(self, table_widget):
        selected_item = table_widget.selectedItems()
        if not selected_item:
            return
        entity = "Assets" if table_widget == self.listWidget else "Shots"
        shot_asset = selected_item[0].text()
        self.build_table_data(entity, shot_asset)

    def build_table_data(self, entity, shot_asset):
        items = self.data.get(entity).get(shot_asset)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(items))

        for row, item in enumerate(items):
            basename = os.path.basename(item).split(".")[0]
            version = get_version_from_filename(basename)
            extension = os.path.basename(item).split(".")[-1]
            table_item_bas = QtWidgets.QTableWidgetItem(str(basename))
            table_item_ver = QtWidgets.QTableWidgetItem(str(version))
            table_item_ext = QtWidgets.QTableWidgetItem(str(extension))
            table_item_bas.setData(QtCore.Qt.UserRole, item)
            self.tableWidget.setItem(row, 0, table_item_bas)
            self.tableWidget.setItem(row, 1, table_item_ver)
            self.tableWidget.setItem(row, 2, table_item_ext)

        self.tableWidget.resizeColumnsToContents()

    def process_import(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return
        select_item_row = selected_items[0].row()
        path = self.tableWidget.item(select_item_row, 0).data(QtCore.Qt.UserRole)
        print(path)

if __name__ == "__main__":
    data = {
        "Assets": {'landscape': [
            'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Assets\\Environment\\landscape\\Renders\\3dRender\\Shading\\v0002\\beauty\\landscape_Shading_v0002_beauty.%04d.exr'],
                   'test': []},
        "Shots": {'vinc_sh_010': [],
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
                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0031\\beauty\\vinc-vinc_sh_020_Animation_v0031_beauty.%04d.exr',
                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0032\\beauty\\vinc-vinc_sh_020_Animation_v0032_beauty.%04d.exr',
                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\3dRender\\Animation\\v0033\\beauty\\vinc-vinc_sh_020_Animation_v0033_beauty.%04d.exr']}
    }
    app = QtWidgets.QApplication(sys.argv)
    w = ImportNukeLayers(data)
    w.show()
    app.exec_()
