from PyQt5.QtCore import QAbstractTableModel, Qt


# Class for dataframe table creation
class PandasModel(QAbstractTableModel):

    # Initialize table with data
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    # Getter method
    def rowCount(self, parent=None):
        return self._data.shape[0]

    # Getter method
    def columnCount(self, parnet=None):
        return self._data.shape[1]

    # Get location of selected item
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    # Set flags and make table editable
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        return super().flags(index) | Qt.ItemIsEditable  # add editable flag.

    # Set orientation to horizontal
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    # Called when table is edited
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            # Set the value into the frame.
            self._data.iloc[index.row(), index.column()] = value

            self.dataChanged.emit(index, index)
            return True

        return False
