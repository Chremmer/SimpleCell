import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from pandas import DataFrame as DataframeObject
import Dataframe
from GraphMenu import GraphMenu
from GraphModel import GraphModel
from LoadedSheets import LoadedSheets
from PandasModel import PandasModel
import sys


# Main window creation
class MainWindow(QMainWindow):
    # Excel sheets
    sheetsDir: LoadedSheets
    # Tabs
    tabs: QTabWidget
    # Graph list
    graph_window: list[QWidget]
    # Dataframe list
    data: list[DataframeObject]
    # Graph menu
    menu: list[GraphMenu]

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialization
        container = QWidget()
        self.setCentralWidget(container)
        layout = QGridLayout()
        container.setLayout(layout)

        self.sheetsDir = LoadedSheets(self)
        self.tabs = QTabWidget(self)
        self.data = []
        self.menu = []
        self.graph_window = []

        # Set functions for click events
        self.sheetsDir.loadedSheets.itemDoubleClicked.connect(self.loadSheet)
        self.sheetsDir.saveButton.clicked.connect(self.save)
        self.tabs.tabBarDoubleClicked.connect(self.del_tab)

        # Add widgets to window
        layout.addWidget(self.sheetsDir, 0, 0, 5, 2)
        layout.addWidget(self.tabs, 0, 2, 5, 7)

        # Window setup
        self.setWindowTitle("Simple Cell")
        self.setMinimumSize(1067, 600)
        self.setWindowIcon(QtGui.QIcon('logo.jpg'))
        self.show()

    # Add tab to window
    def add_tab(self, widget: QWidget, name):
        tab = QWidget()
        layout = QGridLayout()
        tab.setLayout(layout)

        layout.addWidget(widget, 0, 0)

        # Add graph menu to tab
        m = GraphMenu()
        m.graph_type.currentIndexChanged.connect(self.set_combobox)
        m.create.clicked.connect(self.create_graph)
        layout.addWidget(m, 1, 0)
        self.menu.append(m)

        # Add tab
        self.tabs.addTab(tab, name)
        self.tabs.setCurrentIndex(len(self.tabs) - 1)

    # Delete tab from double click
    def del_tab(self):
        if len(self.data) > 0:
            tab_index = self.tabs.currentIndex()
            self.tabs.removeTab(tab_index)
            del self.menu[tab_index]
            del self.data[tab_index]

    # Load sheet
    def loadSheet(self, file: QListWidgetItem):

        # If sheet doesn't already exist, load it
        if not self.tab_exists(file.text()):
            excel_sheet_path = self.sheetsDir.getPath(file)
            sheet = excel_sheet_path[excel_sheet_path.rfind(" - ") + 3:]
            path = excel_sheet_path[:excel_sheet_path.rfind(" - ")]

            # Create dataframe
            df = Dataframe.excel_to_dataframe(path, sheet)
            self.data.append(df)
            df_model = self.create_dataframe_model(df)
            self.add_tab(df_model, file.text())

            df_cols = list(df.columns)

            # Add dataframe columns to graph menu
            for col in df_cols:
                self.menu[len(self.menu) - 1].column1.addItem(col)
                self.menu[len(self.menu) - 1].column2.addItem(col)
        else:
            return

    # Check if tab already exists
    def tab_exists(self, name):
        tab_count = self.tabs.count()

        if tab_count > 0:
            for tab in range(0, self.tabs.count()):
                if self.tabs.tabText(tab) == name:
                    return True

            return False
        else:
            return False

    # Create dataframe model for table widget
    def create_dataframe_model(self, df: DataframeObject):
        model = PandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.model().dataChanged.connect(self.changedData)

        return view

    # Create a graph
    def create_graph(self):
        # Get selected graph menu options
        tab_index = self.tabs.currentIndex()
        graph = GraphModel()
        selected_graph = self.menu[tab_index].graph_type.currentText()
        selected_col1 = self.menu[tab_index].column1.currentText()
        selected_col2 = self.menu[tab_index].column2.currentText()

        # Create line graph
        if selected_graph == "Line" and selected_col1 != "Select Column 1":
            try:
                graph.axes.plot(self.data[tab_index][selected_col1])
                self.create_graph_window(graph)
            except Exception:
                self.error_window()
                return

        # Create bar graph
        elif selected_graph == "Bar" and selected_col1 != "Select Column 1" and \
                selected_col2 != "Select Column 2":
            try:
                graph.axes.bar(self.data[tab_index][selected_col1], self.data[tab_index][selected_col2])
                self.create_graph_window(graph)
            except Exception:
                self.error_window()
                return
        # If options are not correctly selected, don't make graph
        else:
            return

    # Create new window for graph
    def create_graph_window(self, graph):

        # Create save button
        save = QPushButton("Save as PNG")

        layout = QGridLayout()
        layout.addWidget(save, 0, 0)
        layout.addWidget(graph, 1, 0)

        tab_index = self.tabs.currentIndex()
        selected_graph = self.menu[tab_index].graph_type.currentText()
        selected_col1 = self.menu[tab_index].column1.currentText()
        selected_col2 = self.menu[tab_index].column2.currentText()

        w = QWidget()
        w.setLayout(layout)
        w.setWindowIcon(QtGui.QIcon('logo.jpg'))

        # Set proper title
        if selected_graph == "Line":
            w.setWindowTitle("Line Graph [" + selected_col1 + "]")
        elif selected_graph == "Bar":
            w.setWindowTitle("Bar Graph [" + selected_col1 + ", " + selected_col2 + "]")

        # Get click event for save graph
        save.clicked.connect(self.save_graph)

        self.graph_window.append(w)
        self.graph_window[len(self.graph_window) - 1].show()
        self.graph_window[len(self.graph_window) - 1].setMinimumSize(w.size())

    # Save graph as png
    def save_graph(self):
        # Get graph and file name
        graph = self.graph_window[len(self.graph_window) - 1].findChild(GraphModel)
        file_name = self.graph_window[len(self.graph_window) - 1].windowTitle()

        tab_index = self.tabs.currentIndex()
        tab_title = self.tabs.tabText(tab_index)
        path = self.sheetsDir.getPath(fileName=tab_title)

        # Get correct path
        last_char = path[-1]
        while last_char != "/":
            path = path[:-1]
            last_char = path[-1]

        # Save as png
        graph.axes.figure.savefig(path + file_name + ".png")

    # Error window that displays when graph creation throws error
    def error_window(self):
        error = QLabel("Graph Error: Unable to create graph\n\nCheck for bad data")
        error.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(error)

        w = QWidget()
        w.setLayout(layout)
        w.setWindowTitle("Graph Error")
        w.setFixedSize(300, 100)
        w.setWindowIcon(QtGui.QIcon('logo.jpg'))

        self.graph_window.append(w)
        self.graph_window[len(self.graph_window) - 1].show()

    # Enable or disable graph menu widgets accordingly
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

    # Overwrite Excel file with edited data
    def save(self):
        tab_index = self.tabs.currentIndex()

        if tab_index >= 0:
            # Get path and file name
            tab_title = self.tabs.tabText(tab_index)
            path = self.sheetsDir.getPath(fileName=tab_title)
            filename = path[:path.rfind(" - ")]
            sheet = tab_title[tab_title.rfind(" - ") + 3:]

            # Write to file
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                workBook = writer.book
                try:
                    workBook.remove(workBook[sheet])
                except:
                    print("Worksheet does not exist")
                finally:
                    self.data[tab_index].to_excel(writer, sheet_name=sheet, index=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowExample = MainWindow()
    sys.exit(app.exec_())
