import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import numpy as np

class DraggablePlotWidget(pg.PlotWidget):
    def __init__(self):
        super(DraggablePlotWidget, self).__init__()

        # Store the points to be plotted
        self.points = []

        # Enable mouse tracking to capture mouse events
        self.setMouseTracking(True)

        # Connect mouse events to custom functions
        self.scene().sceneSigMouseMoved.connect(self.mouse_moved)
        self.scene().sceneSigMouseClicked.connect(self.mouse_clicked)

        # Store the index of the clicked point
        self.clicked_point_index = None

    def plot_points(self, points):
        self.clear()
        self.plot(*zip(*points), pen=None, symbol='o', symbolSize=10)

    def mouse_moved(self, ev):
        # Update the cursor position in the status bar or perform other actions
        pass

    def mouse_clicked(self, ev):
        # Check if a point is clicked
        pos = self.vb.mapSceneToView(ev.pos())
        clicked_point_index = self.get_clicked_point_index(pos)

        if clicked_point_index is not None:
            # Store the clicked point index for dragging
            self.clicked_point_index = clicked_point_index
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, ev):
        # Reset cursor and clicked point index when the mouse is released
        self.setCursor(Qt.ArrowCursor)
        self.clicked_point_index = None

    def mouseMoveEvent(self, ev):
        # Drag the point if it was clicked
        if self.clicked_point_index is not None:
            pos = self.vb.mapSceneToView(ev.pos())
            self.update_point_position(self.clicked_point_index, pos)

    def get_clicked_point_index(self, pos):
        # Check if the mouse click is close to any plotted point
        for i, point in enumerate(self.points):
            if np.linalg.norm(np.array(point) - np.array(pos)) < 0.1:
                return i
        return None

    def update_point_position(self, index, new_pos):
        # Update the position of a point in the list and redraw the plot
        self.points[index] = tuple(new_pos)
        self.plot_points(self.points)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        # Create a central widget to hold the draggable plot widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a draggable plot widget
        self.plot_widget = DraggablePlotWidget()
        layout.addWidget(self.plot_widget)

        # Add some example points
        self.plot_widget.points = [(1, 2), (3, 4), (-2, 1)]
        self.plot_widget.plot_points(self.plot_widget.points)

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
