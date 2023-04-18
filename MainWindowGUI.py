import pandas
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import *
from pandas import DataFrame as DataframeObject

import Dataframe
from LoadedSheets import LoadedSheets
from PandasModel import PandasModel
import sys


class MainWindow(QMainWindow):
    sheetsDir: LoadedSheets
    tabs: QTabWidget
    graph: QWidget
    data: list[DataframeObject]

    def __init__(self, parent=None):
        super().__init__(parent)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QGridLayout()
        container.setLayout(layout)

        self.sheetsDir = LoadedSheets(self)
        self.tabs = QTabWidget(self)
        self.graph = QWidget(self)
        self.data = []

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
        excel_sheet = self.sheetsDir.getPath(file)
        df = Dataframe.excel_to_dataframe(excel_sheet)
        self.data.append(df)
        df_model = self.create_dataframe_model(df)
        self.add_tab(df_model, excel_sheet)

    def create_dataframe_model(self, df: DataframeObject):
        model = PandasModel(df)
        self.data.append(df)
        view = QTableView()
        view.setModel(model)
        view.model().dataChanged.connect(self.changedData)

        return view

    def changedData(self, item):
        print(item.row())
        print(item.column())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowExample = MainWindow()
    sys.exit(app.exec_())
