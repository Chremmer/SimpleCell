from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox


class GraphMenu(QWidget):
    graph_type: QComboBox
    column: QComboBox
    create: QPushButton

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.graph_type = QComboBox()
        self.graph_type.addItem("Select Graph Type")
        self.graph_type.addItem("Line")
        self.graph_type.addItem("Bar")

        self.column = QComboBox()
        self.column.addItem("Select Column")

        self.create = QPushButton("Create")

        self.graph_type.setMinimumWidth(1)
        self.column.setMinimumWidth(1)
        self.create.setMinimumWidth(1)

        layout.addWidget(self.graph_type, 0, 0)
        layout.addWidget(self.column, 0, 1)
        layout.addWidget(self.create, 0, 2)

