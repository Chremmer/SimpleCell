from PyQt5.QtWidgets import *

class ShowFrames(QWidget):
    tabList: QTabWidget

    def __init__(self, parent = None):
        super().__init__()

        layout = QBoxLayout(QBoxLayout.Direction.Up)
        self.setLayout(layout)
        tabList = QTabWidget()

        layout.addWidget(tabList)
