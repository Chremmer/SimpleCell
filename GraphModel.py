from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# Widget for graph using matplotlib
class GraphModel(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=7, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(GraphModel, self).__init__(fig)
