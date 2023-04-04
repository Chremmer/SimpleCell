from PyQt5.QtWidgets import *
from LoadedSheets import LoadedSheets
from ShowFrames import ShowFrames

import sys


class MainWindow(QMainWindow):
    sheetsDir: LoadedSheets
    tabs: ShowFrames
    graph: QWidget

    def __init__(self, parent=None):
        super().__init__(parent)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QGridLayout()
        container.setLayout(layout)

        self.sheetsDir = LoadedSheets(self)
        self.tabs = ShowFrames(self)
        self.graph = QWidget(self)

        layout.addWidget(self.sheetsDir, 0, 0, 5, 2)
        layout.addWidget(self.tabs, 0, 2, 3, 7)
        layout.addWidget(self.graph, 3, 2, 2, 7)

        self.show()




if( __name__ == "__main__"):
    app = QApplication(sys.argv)
    windowExample = MainWindow()
    sys.exit(app.exec_())