from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtGui, QtCore


class LoadedSheets(QWidget):

    loadButton: QPushButton
    delButton: QPushButton
    newButton: QPushButton
    loadedSheets: QListWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.loadButton = QPushButton("Load")
        self.delButton = QPushButton("Del")
        self.newButton = QPushButton("New")

        self.setButtonWidth()
        self.loadButton.setMinimumWidth(1)
        self.delButton.setMinimumWidth(1)
        self.newButton.setMinimumWidth(1)

        layout.addWidget(self.loadButton, 0, 0)
        layout.addWidget(self.delButton, 0, 1)
        layout.addWidget(self.newButton, 0, 2)

        self.loadedSheets = QListWidget()

        layout.addWidget(self.loadedSheets, 1, 0, 5, 3)


    def setButtonWidth(self):
        width = self.width()

        self.loadButton.setMaximumWidth(width // 3)
        self.delButton.setMaximumWidth(width // 3)
        self.newButton.setMaximumWidth(width // 3)


    def resizeEvent(self, event):
        self.setButtonWidth()
