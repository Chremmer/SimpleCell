from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtGui, QtCore
import PyQt5.QtWidgets

import subprocess


class LoadedSheets(QWidget):

    loadButton: QPushButton
    delButton: QPushButton
    newButton: QPushButton
    loadedSheets: QListWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.loadButton = QPushButton("Load")
        self.delButton = QPushButton("Del")
        self.newButton = QPushButton("New")

        self.loadButton.clicked.connect(self.loadSheet)

        self.setButtonWidth()
        self.loadButton.setMinimumWidth(1)
        self.delButton.setMinimumWidth(1)
        self.newButton.setMinimumWidth(1)

        layout.addWidget(self.loadButton, 0, 0)
        layout.addWidget(self.delButton, 0, 1)
        layout.addWidget(self.newButton, 0, 2)

        self.loadedSheets = QListWidget()

        layout.addWidget(self.loadedSheets, 1, 0, 5, 3)


    def setButtonWidth(self):
        width = self.width()

        self.loadButton.setMaximumWidth(width // 3)
        self.delButton.setMaximumWidth(width // 3)
        self.newButton.setMaximumWidth(width // 3)


    def resizeEvent(self, event):
        self.setButtonWidth()

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

    def loadSheet(self):
        fileDir = self.getOpenFilesAndDirs()

        if(fileDir != None):
            """
            TODO get call the functions for loading in the directories
            """