from PyQt5.QtWidgets import *

import openpyxl


# Widget for loaded sheets pane
class LoadedSheets(QWidget):

    # Button and list widget setup
    loadButton: QPushButton
    delButton: QPushButton
    newButton: QPushButton
    loadedSheets: QListWidget
    path: list

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize GUI componenets
        layout = QGridLayout()
        self.setLayout(layout)

        self.path = list()
        self.loadButton = QPushButton("Load")
        self.delButton = QPushButton("Delete")
        self.loadedSheets = QListWidget(self)
        self.saveButton = QPushButton("Save")

        self.loadButton.clicked.connect(self.loadWorkBook)
        self.delButton.clicked.connect(self.removeItem)

        self.loadButton.setMinimumWidth(1)
        self.delButton.setMinimumWidth(1)
        self.saveButton.setMinimumWidth(1)
        self.setButtonWidth()

        layout.addWidget(self.loadButton, 0, 0)
        layout.addWidget(self.delButton, 0, 1)
        layout.addWidget(self.saveButton, 0, 2)

        layout.addWidget(self.loadedSheets, 1, 0, 5, 3)

    # Set width
    def setButtonWidth(self):
        width = self.width()

        self.loadButton.setMaximumWidth(width // 3)
        self.delButton.setMaximumWidth(width // 3)
        self.saveButton.setMaximumWidth(width // 3)

    # Resize buttons
    def resizeEvent(self, event):
        self.setButtonWidth()

    def loadSheets(self, fileName : QListWidgetItem):
        pass

    # Remove item from list widget
    def removeItem(self):
        selected = self.loadedSheets.selectedItems()

        remove = list()
        # Remove selected item when delete is clicked
        for item in selected:
            remove.append(self.loadedSheets.indexFromItem(item).row())
            self.loadedSheets.takeItem(self.loadedSheets.indexFromItem(item).row())

        for num in reversed(remove):
            self.path.pop(num)

    # Get path of file
    def getPath(self, listItem: QListWidgetItem = None, fileName: str = None) -> str:
        if(listItem != None):
            return self.path[self.loadedSheets.indexFromItem(listItem).row()]

        for check in self.path:
            if(fileName == str(check)[str(check).rfind("/") + 1:]):
                return str(check)

        return ""

    # Load an Excel workbook after file is selected
    def loadWorkBook(self):
        fileDir = self.getOpenFilesAndDirs()

        if(fileDir != None):
            for file in fileDir:
                fileType = file[file.rindex('.'):]

                if(fileType == '.xlsx'):
                    workbook = openpyxl.load_workbook(filename=file)
                    sheets = workbook.sheetnames

                    for sheet in sheets:
                        self.path.append(file + " - " + sheet)
                        self.loadedSheets.addItem(QListWidgetItem(file[file.rindex('/') + 1:] + " - " + sheet))


    """
    This was found at https://stackoverflow.com/questions/64336575/select-a-file-or-a-folder-in-qfiledialog-pyqt5
    for opening a file directory
    """
    def getOpenFilesAndDirs(parent=None, caption='', directory='',
                            filter='', initialFilter='', options=None):
        def updateText():
            # update the contents of the line edit widget with the selected files
            selected = []
            for index in view.selectionModel().selectedRows():
                selected.append('"{}"'.format(index.data()))
            lineEdit.setText(' '.join(selected))

        dialog = QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)

        # by default, if a directory is opened in file listing mode,
        # QFileDialog.accept() shows the contents of that directory, but we
        # need to be able to "open" directories as we can do with files, so we
        # just override accept() with the default QDialog implementation which
        # will just return exec_()
        dialog.accept = lambda: QDialog.accept(dialog)

        # there are many item views in a non-native dialog, but the ones displaying
        # the actual contents are created inside a QStackedWidget; they are a
        # QTreeView and a QListView, and the tree is only used when the
        # viewMode is set to QFileDialog.Details, which is not this case
        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QLineEdit)
        # clear the line edit contents whenever the current directory changes
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec_()
        return dialog.selectedFiles()
