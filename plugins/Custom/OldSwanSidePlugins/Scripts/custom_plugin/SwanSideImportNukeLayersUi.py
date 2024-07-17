#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import re
import sys
import nuke
from pprint import pprint

from PySide2 import QtWidgets, QtCore, QtGui

from .import_aovs_ui import Ui_MainWindow


# C:\Users\User\AppData\Local\Programs\Python\Python37\Scripts\pyside2-uic.exe C:\ProgramData\Prism2\plugins\Custom\SwanSidePlugins\Scripts\custom_plugin\import_aovs_ui.ui -o C:\ProgramData\Prism2\plugins\Custom\SwanSidePlugins\Scripts\custom_plugin\import_aovs_ui.py

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
        # self.tabWidget.setMaximumSize(500, 200)
        self.processBtn.setText("Process Layers..")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Task", "Version", "Extension", "Status"])
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

        for row, item in enumerate(sorted(items, key=lambda x: x[0], reverse=True)):
            path = item[0]
            task = item[1]
            status = item[2]
            version = item[3]

            basename = os.path.basename(path).split(".")[0]
            extension = os.path.basename(path).split(".")[-1]
            table_item_bas = QtWidgets.QTableWidgetItem(str(basename))
            table_item_ver = QtWidgets.QTableWidgetItem(str(version))
            table_item_task = QtWidgets.QTableWidgetItem(str(task))
            table_item_ext = QtWidgets.QTableWidgetItem(str(extension))
            table_item_status = QtWidgets.QTableWidgetItem(str(status))
            table_item_bas.setData(QtCore.Qt.UserRole, path)

            if status == "done":
                for i in [table_item_bas, table_item_task, table_item_ext, 
                          table_item_status, table_item_ver]:
                    i.setBackground(QtGui.QColor(0, 100, 0))

            self.tableWidget.setItem(row, 0, table_item_bas)
            self.tableWidget.setItem(row, 1, table_item_task)
            self.tableWidget.setItem(row, 2, table_item_ver)
            self.tableWidget.setItem(row, 3, table_item_ext)
            self.tableWidget.setItem(row, 4, table_item_status)

        self.tableWidget.resizeColumnsToContents()

    def process_import(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return
        select_item_row = selected_items[0].row()
        path = self.tableWidget.item(select_item_row, 0).data(QtCore.Qt.UserRole)
        files = sorted(os.listdir(os.path.dirname(path)))

        if "versioninfo.json" in files:
            files.remove("versioninfo.json")

        if "\\" in path:
            path = path.replace("\\", "/")

        firstFrame = int(files[0].split('.')[-2])
        lastFrame = int(files[-1].split('.')[-2])

        readNode = nuke.createNode('Read')
        readNode['file'].setValue(path)
        readNode['first'].setValue(firstFrame)
        readNode['last'].setValue(lastFrame)
        readNode['origfirst'].setValue(firstFrame)
        readNode['origlast'].setValue(lastFrame)


if __name__ == "__main__":
    data = {'Assets': {'landscape': [(
                                     'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Assets\\Environment\\landscape\\Renders\\3dRender\\Shading\\v0002\\beauty\\landscape_Shading_v0002_beauty.%04d.exr',
                                     'Shading',
                                     'wip',
                                     'v0002'),
                                     (
                                     'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Assets\\Environment\\landscape\\Renders\\3dRender\\Shading\\v0004\\beauty\\landscape_Shading_v0004_beauty.%04d.exr',
                                     'Shading',
                                     'wip',
                                     'v0004')],
                       'test': []},
            'Shots': {'vinc_sh_010': [(
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_010\\Renders\\2dRender\\base\\v0001\\vinc-vinc_sh_010_base_v0001.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0001'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_010\\Renders\\2dRender\\base\\v0002\\vinc-vinc_sh_010_base_v0002.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0002'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_010\\Renders\\2dRender\\base\\v0003\\vinc-vinc_sh_010_base_v0003.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0003'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_010\\Renders\\2dRender\\zzzz\\v0001\\vinc-vinc_sh_010_zzzz_v0001.####.exr',
                                      'Animation',
                                      'wip',
                                      'v0001')],
                      'vinc_sh_020': [(
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0001\\vinc-vinc_sh_020_test_v0001.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0001'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0002\\vinc-vinc_sh_020_test_v0002.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0002'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0003\\vinc-vinc_sh_020_test_v0003.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0003'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0004\\vinc-vinc_sh_020_test_v0004.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0004'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0005\\vinc-vinc_sh_020_test_v0005.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0005'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0006\\vinc-vinc_sh_020_test_v0006.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0006'),
                                      (
                                      'D:\\Desk\\python\\Projects\\TestProd\\03_Production\\Shots\\vinc\\vinc_sh_020\\Renders\\2dRender\\test\\v0007\\vinc-vinc_sh_020_test_v0007.####.exr',
                                      'Compositing',
                                      'wip',
                                      'v0007')]}}
    app = QtWidgets.QApplication(sys.argv)
    w = ImportNukeLayers(data)
    w.show()
    app.exec_()
