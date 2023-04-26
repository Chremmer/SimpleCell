import pandas
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import *
from openpyxl.utils import dataframe
from pandas import DataFrame as DataframeObject
import matplotlib.pyplot as plt
import Dataframe
from GraphMenu import GraphMenu
from GraphModel import GraphModel
from LoadedSheets import LoadedSheets
from PandasModel import PandasModel
import sys

from openpyxl import *


class MainWindow(QMainWindow):
    sheetsDir: LoadedSheets
    tabs: QTabWidget
    graph: GraphModel
    graph_window: list[QWidget]
    data: list[DataframeObject]
    menu: list[GraphMenu]

    def __init__(self, parent=None):
        super().__init__(parent)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QGridLayout()
        container.setLayout(layout)

        self.sheetsDir = LoadedSheets(self)
        self.tabs = QTabWidget(self)
        self.data = []
        self.menu = []
        self.graph_window = []

        self.sheetsDir.loadedSheets.itemDoubleClicked.connect(self.loadSheet)
        self.sheetsDir.saveButton.clicked.connect(self.save)

        layout.addWidget(self.sheetsDir, 0, 0, 5, 2)
        layout.addWidget(self.tabs, 0, 2, 5, 7)

        self.tabs.tabBarDoubleClicked.connect(self.del_tab)

        self.setWindowTitle("Simple Cell")
        self.setMinimumSize(1067, 600)
        self.show()

    def add_tab(self, widget: QWidget, name):
        tab = QWidget()
        layout = QGridLayout()
        tab.setLayout(layout)

        layout.addWidget(widget, 0, 0)

        m = GraphMenu()
        m.graph_type.currentIndexChanged.connect(self.set_combobox)
        m.create.clicked.connect(self.create_graph)
        layout.addWidget(m, 1, 0)
        self.menu.append(m)
        self.tabs.addTab(tab, name)
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    def del_tab(self):
        if len(self.data) > 0:
            tab_index = self.tabs.currentIndex()
            self.tabs.removeTab(tab_index)
            del self.menu[tab_index]
            del self.data[tab_index]

    def loadSheet(self, file: QListWidgetItem):

        if not self.tab_exists(file.text()):
            excel_sheet_path = self.sheetsDir.getPath(file)
            sheet = excel_sheet_path[excel_sheet_path.rfind(" - ") + 3:]
            path = excel_sheet_path[:excel_sheet_path.rfind(" - ")]

            df = Dataframe.excel_to_dataframe(path, sheet)
            self.data.append(df)
            df_model = self.create_dataframe_model(df)
            self.add_tab(df_model, file.text())

            df_cols = list(df.columns)

            for col in df_cols:
                self.menu[len(self.menu) - 1].column1.addItem(col)
                self.menu[len(self.menu) - 1].column2.addItem(col)
        else:
            return

    def tab_exists(self, name):
        tab_count = self.tabs.count()

        if tab_count > 0:
            for tab in range(0, self.tabs.count()):
                if self.tabs.tabText(tab) == name:
                    return True

            return False
        else:
            return False

    def create_dataframe_model(self, df: DataframeObject):
        model = PandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.model().dataChanged.connect(self.changedData)

        return view

    def create_graph(self):
        tab_index = self.tabs.currentIndex()
        self.graph = GraphModel()
        layout = QVBoxLayout()
        selected_graph = self.menu[tab_index].graph_type.currentText()
        selected_col1 = self.menu[tab_index].column1.currentText()
        selected_col2 = self.menu[tab_index].column2.currentText()

        if selected_graph == "Line" and selected_col1 != "Select Column 1":
            try:
                self.graph.axes.plot(self.data[tab_index][selected_col1])
            except Exception:
                return

        elif selected_graph == "Bar" and selected_col1 != "Select Column 1" and \
                selected_col2 != "Select Column 2":
            try:
                self.graph.axes.bar(self.data[tab_index][selected_col1], self.data[tab_index][selected_col2])
            except Exception:
                return
        else:
            return

        layout.addWidget(self.graph)

        w = QWidget()
        w.setLayout(layout)
        if selected_graph == "Line":
            w.setWindowTitle("Line Graph [" + selected_col1 + "]  |  " + self.tabs.tabText(tab_index))
        elif selected_graph == "Bar":
            w.setWindowTitle("Bar Graph [" + selected_col1 + ", " + selected_col2 + "]  |  " \
                             + self.tabs.tabText(tab_index))
        self.graph_window.append(w)

        self.graph_window[len(self.graph_window) - 1].show()

    def set_combobox(self):
        tab_index = self.tabs.currentIndex()
        selected = self.menu[tab_index].graph_type.currentText()

        if selected == "Line":
            self.menu[tab_index].column1.setEnabled(True)
            self.menu[tab_index].column2.setEnabled(False)
        elif selected == "Bar":
            self.menu[tab_index].column1.setEnabled(True)
            self.menu[tab_index].column2.setEnabled(True)
        else:
            self.menu[tab_index].column1.setEnabled(False)
            self.menu[tab_index].column2.setEnabled(False)

    def changedData(self, item):
        print(item.row())
        print(item.column())

    def save(self):
        tab_index = self.tabs.currentIndex()
        tab_title = self.tabs.tabText(tab_index)
        path = self.sheetsDir.getPath(fileName=tab_title)
        filename = path[:path.rfind(" - ")]
        sheet = tab_title[tab_title.rfind(" - ") + 3:]

        with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
            workBook = writer.book
            try:
                workBook.remove(workBook[sheet])
            except:
                print("Worksheet does not exist")
            finally:
                self.data[tab_index].to_excel(writer, sheet_name=sheet, index=False)
                writer.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowExample = MainWindow()
    sys.exit(app.exec_())
