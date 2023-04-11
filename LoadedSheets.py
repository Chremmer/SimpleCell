from PyQt5.QtCore import QChildEvent, QEvent
from PyQt5.QtWidgets import *

import Dataframe as df


class LoadedSheets(QWidget):

    loadButton: QPushButton
    delButton: QPushButton
    newButton: QPushButton
    loadedSheets: QListWidget
    path: list

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.path = list()
        self.loadButton = QPushButton("Load")
        self.delButton = QPushButton("Del")
        self.loadedSheets = QListWidget(self)

        self.loadButton.clicked.connect(self.loadWorkBook)
        self.delButton.clicked.connect(self.removeItem)

        self.loadButton.setMinimumWidth(1)
        self.delButton.setMinimumWidth(1)
        self.setButtonWidth()

        layout.addWidget(self.loadButton, 0, 0)
        layout.addWidget(self.delButton, 0, 1)

        layout.addWidget(self.loadedSheets, 1, 0, 5, 2)


    def setButtonWidth(self):
        width = self.width()

        self.loadButton.setMaximumWidth(width // 2)
        self.delButton.setMaximumWidth(width // 2)


    def resizeEvent(self, event):
        self.setButtonWidth()

    def loadSheets(self, fileName : QListWidgetItem):
        pass

    def removeItem(self):
        selected = self.loadedSheets.selectedItems()

        remove = list()
        for item in selected:
            remove.append(self.loadedSheets.indexFromItem(item).row())
            self.loadedSheets.takeItem(self.loadedSheets.indexFromItem(item).row())

        for num in reversed(remove):
            self.path.pop(num)

    def getPath(self, listItem: QListWidgetItem) -> str:
        return self.path[self.loadedSheets.indexFromItem(listItem).row()]

    def loadWorkBook(self):
        fileDir = self.getOpenFilesAndDirs()

        if(fileDir != None):
            for file in fileDir:
                fileType = file[file.rindex('.'):]

                if(fileType == '.xlsx'):
                    self.path.append(file)
                    self.loadedSheets.addItem(QListWidgetItem(file[file.rindex('/') + 1:]))


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