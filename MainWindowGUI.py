import pandas as pd
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
        self.sheetsDir.saveButton.clicked.connect(self.save)

        layout.addWidget(self.sheetsDir, 0, 0, 5, 2)
        layout.addWidget(self.tabs, 0, 2, 3, 7)
        layout.addWidget(self.graph, 3, 2, 2, 7)

        self.tabs.tabBarDoubleClicked.connect(self.del_tab)

        self.show()

    def add_tab(self, widget: QWidget, name):
        tab = QWidget()
        tab.setLayout(QGridLayout())
        tab.layout().addWidget(widget)
        self.tabs.addTab(tab, name)

    def del_tab(self):
        if(len(self.data) > 0):
            tab_index = self.tabs.currentIndex()
            self.tabs.removeTab(tab_index)

            self.data.pop(tab_index)

    def loadSheet(self, file: QListWidgetItem):
        excel_sheet_path = self.sheetsDir.getPath(file)
        sheet = excel_sheet_path[excel_sheet_path.rfind(" - ") + 3:]
        path = excel_sheet_path[:excel_sheet_path.rfind(" - ")]

        df = Dataframe.excel_to_dataframe(path, sheet)
        self.data.append(df)
        df_model = self.create_dataframe_model(df)
        self.add_tab(df_model, file.text())

    def create_dataframe_model(self, df: DataframeObject):
        model = PandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.model().dataChanged.connect(self.changedData)

        return view

    def changedData(self, item):
        print(item.row())
        print(item.column())

    def save(self):
        tab_index = self.tabs.currentIndex()
        tab_title = self.tabs.tabText(tab_index)
        path = self.sheetsDir.getPath(fileName=tab_title)
        self.data[tab_index].to_excel(path[:path.rfind(" - ")], tab_title[tab_title.rfind(" - ") + 1:], index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowExample = MainWindow()
    sys.exit(app.exec_())
