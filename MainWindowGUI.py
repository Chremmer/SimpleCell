import pandas
from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtWidgets import *

import Dataframe
from LoadedSheets import LoadedSheets
from PandasModel import PandasModel
import sys


class MainWindow(QMainWindow):
    sheetsDir: LoadedSheets
    tabs: QTabWidget
    graph: QWidget

    def __init__(self, parent=None):
        super().__init__(parent)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QGridLayout()
        container.setLayout(layout)

        self.sheetsDir = LoadedSheets(self)
        self.tabs = QTabWidget(self)
        self.graph = QWidget(self)

        self.sheetsDir.loadedSheets.itemDoubleClicked.connect(self.loadSheet)

        layout.addWidget(self.sheetsDir, 0, 0, 5, 2)
        layout.addWidget(self.tabs, 0, 2, 3, 7)
        layout.addWidget(self.graph, 3, 2, 2, 7)

        self.show()

    def add_tab(self, widget: QWidget, name):
        tab = QWidget()
        tab.setLayout(QGridLayout())
        tab.layout().addWidget(widget)
        self.tabs.addTab(tab, name)

    def loadSheet(self, file: QListWidgetItem):
        print(self.sheetsDir.getPath(file))


if __name__ == "__main__":
    df = pandas.DataFrame({'a': ['Mary', 'Jim', 'John'],
                       'b': [100, 200, 300],
                       'c': ['a', 'b', 'c']})

    app = QApplication(sys.argv)
    windowExample = MainWindow()

    df_model = Dataframe.create_dataframe_model(df)
    df_model2 = df_model

    windowExample.add_tab(df_model, "Tab 1")
    windowExample.add_tab(df_model2, "Tab 2")

    sys.exit(app.exec_())
