#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

try:
    import nuke
    from PySide2 import QtWidgets, QtCore, QtGui
except:
    pass

from exceptions import PublishNukeFailed


class WriteNodeItem(QtWidgets.QWidget):
    def __init__(self, node, root_path):
        super().__init__()
        self.node = node
        self.node_name = node.name()
        self.sequence = node["fileName"].value()
        self.root_path = root_path
        layout = QtWidgets.QHBoxLayout()

        self.checkbox = QtWidgets.QCheckBox(self)
        layout.addWidget(self.checkbox)

        self.label = QtWidgets.QLabel(self.node_name, self)
        layout.addWidget(self.label)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.checkbox.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        self.setLayout(layout)


class SwanSideNukePublisher(QtWidgets.QWidget):
    def __init__(self, pcore=None, parent=None):
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.Window)

        self.pcore = pcore
        self.plugin_swanside = pcore.getPlugin("SwanSidePlugins")

        self.setWindowTitle('SwanSide SwanSidePlugins: ')
        self.setGeometry(300, 300, 250, 150)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel('Select Write Nodes to publish', self)
        layout.addWidget(self.label)

        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        layout.addSpacerItem(spacer)

        self.list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.list_widget)

        self.label_2 = QtWidgets.QLabel("Comment: ", self)
        layout.addWidget(self.label_2)

        self.comment = QtWidgets.QTextEdit()
        layout.addWidget(self.comment)

        self.button = QtWidgets.QPushButton('Publish', self)
        self.button.clicked.connect(self.on_publish)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.populateUi()

    def on_publish(self):
        msgs = []
        comment = self.comment.toPlainText()
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            node_item = self.list_widget.itemWidget(item)
            if not node_item.checkbox.isChecked():
                continue
            msg = self.plugin_swanside.swanside_nuke.publish_nuke(
                node_item.sequence, node_item.root_path, comment
            )
            msgs.append(msg.message if isinstance(msg, PublishNukeFailed) else msg)
        nuke.message("\n".join(msgs))

    def populateUi(self):
        for n in nuke.allNodes("WritePrism"):
            item = QtWidgets.QListWidgetItem()
            custom_widget = WriteNodeItem(n, nuke.root().name())

            item.setSizeHint(custom_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, custom_widget)

# SwanSidePublisher(QtWidgets.QApplication.activeWindow()).show()
