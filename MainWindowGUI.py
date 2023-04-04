from PyQt5.QtWidgets import *
from LoadedSheets import LoadedSheets
import sys

class mainWindow(QMainWindow):
    sheets: LoadedSheets

    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        sheets = LoadedSheets()

        layout.addWidget(sheets, 1, 1, 5, 2)

        self.show()




if( __name__ == "__main__"):
    app = QApplication(sys.argv)
    windowExample = mainWindow()
    windowExample.show()
    sys.exit(app.exec_())