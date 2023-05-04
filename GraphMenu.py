from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QComboBox, QLabel


# Create graph menu widget
class GraphMenu(QWidget):
    # Setup buttons and combo boxes
    label: QLabel
    graph_type: QComboBox
    column1: QComboBox
    column2: QComboBox
    create: QPushButton

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize GUI components
        layout = QGridLayout()
        self.setLayout(layout)

        self.label = QLabel("Graph Options\n")

        self.graph_type = QComboBox()
        self.graph_type.addItem("Select Graph Type")
        self.graph_type.addItem("Line")
        self.graph_type.addItem("Bar")

        self.column1 = QComboBox()
        self.column1.addItem("Select Column 1")
        self.column1.setEnabled(False)

        self.column2 = QComboBox()
        self.column2.addItem("Select Column 2")
        self.column2.setEnabled(False)

        self.create = QPushButton("Create")

        self.label.setMinimumWidth(1)
        self.graph_type.setMinimumWidth(1)
        self.column1.setMinimumWidth(1)
        self.column2.setMinimumWidth(1)
        self.create.setMinimumWidth(1)

        # Add widgets to grid layout
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.graph_type, 1, 0)
        layout.addWidget(self.column1, 1, 1)
        layout.addWidget(self.column2, 1, 2)
        layout.addWidget(self.create, 1, 3)

