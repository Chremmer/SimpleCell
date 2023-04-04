from PyQt5.QtWidgets import *

class LoadedSheets(QWidget):
    loadButton: QPushButton
    delButton: QPushButton
    newButton: QPushButton
    loadedSheets: QListWidget

    def __init__(self):

        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        loadButton = QPushButton("Load Sheet")
        delButton = QPushButton("Remove Selected")
        newButton = QPushButton("Create New")

        layout.addWidget(loadButton, 0, 0)
        layout.addWidget(delButton, 0, 1)
        layout.addWidget(newButton, 0, 2)

        loadedSheets = QListWidget()

        layout.addWidget(loadedSheets, 1, 0, 9, 3)

        self.show()