import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem
from pyqtgraph import PlotWidget, ScatterPlotItem

class HighlightablePlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Scatter plot item to hold points
        self.scatter = ScatterPlotItem()
        self.addItem(self.scatter)

        # List to store highlighted points
        self.highlighted_points = []

        # Flag to track dragging state
        self.is_dragging = False

    def add_point(self, x, y):
        # Add a point to the scatter plot
        point = {'pos': (x, y), 'data': 1, 'brush': 'b', 'pen': {'color': 'w', 'width': 2}}
        self.scatter.addPoints([point])

    def mousePressEvent(self, event):
        # Convert the mouse position to the plot coordinates
        pos = self.plotItem.vb.mapSceneToView(event.pos())

        # Check if a scatter point is clicked
        clicked_point = self.scatter.pointsAt(pos)
        if clicked_point:
            # Highlight the clicked point
            for point in clicked_point:
                ellipse = QGraphicsEllipseItem(*point)
                ellipse.setBrush(QBrush(Qt.red))
                ellipse.setPen(QPen(Qt.red))
                self.highlighted_points.append(ellipse)
                self.addItem(ellipse)

            # Record the clicked point for dragging
            self.dragged_point = clicked_point[0]
            self.is_dragging = True
        else:
            # If no point is clicked, let the base class handle the event
            super().mousePressEvent(event)



    def mouseMoveEvent(self, event):
        if self.is_dragging:
            # Move the highlighted point with the cursor
            x, y = event.pos().x(), event.pos().y()
            self.dragged_point.setPos(x, y)

    def mouseReleaseEvent(self, event):
        if self.is_dragging:
            # Move the scatter point to the final position
            x, y = event.pos().x(), event.pos().y()
            self.scatter.scatter.points[self.dragged_point.data()['item']] = {'pos': (x, y), 'data': 1, 'brush': 'b', 'pen': {'color': 'w', 'width': 2}}
            # Clean up highlighted point
            for item in self.highlighted_points:
                self.removeItem(item)
            self.highlighted_points = []
            self.is_dragging = False
        else:
            # If not dragging, let the base class handle the event
            super().mouseReleaseEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.plot_widget = HighlightablePlotWidget(self.central_widget)
        self.plot_widget.add_point(1, 2)
        self.plot_widget.add_point(3, 4)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.plot_widget)

def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
