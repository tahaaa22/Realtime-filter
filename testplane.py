import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication

class MyPlotWidget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse_dragging = False
        self.last_mouse_pos = None
        self.selected_point = None

        # Plot some example data
        self.x = [1, 2, 3, 4, 5]
        self.y = [2, 4, 1, 7, 2]
        self.scatter = self.plot(self.x, self.y, symbol='o', symbolPen='b')

    def mousePressEvent(self, event):
        if event.button() == pg.QtCore.Qt.LeftButton:
            mouse_point = self.plotItem.vb.mapSceneToView(event.pos())

            # Check if the mouse is close to any plotted points
            for i in range(len(self.x)):
                if abs(mouse_point.x() - self.x[i]) < 0.2 and abs(mouse_point.y() - self.y[i]) < 0.2:
                    self.mouse_dragging = True
                    self.selected_point = i
                    self.last_mouse_pos = event.pos()
                    break

    def mouseMoveEvent(self, event):
        if self.mouse_dragging and self.selected_point is not None:
            delta = event.pos() - self.last_mouse_pos

            # Update the selected point's coordinates
            self.x[self.selected_point], self.y[self.selected_point] = self.plotItem.vb.mapSceneToView(event.pos()).x(), self.plotItem.vb.mapSceneToView(event.pos()).y()

            # Update the scatter plot with the new coordinates
            self.scatter.setData(x=self.x, y=self.y)

            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == pg.QtCore.Qt.LeftButton:
            self.mouse_dragging = False
            self.selected_point = None

if __name__ == '__main__':
    app = QApplication([])
    win = MyPlotWidget()
    win.show()
    app.exec_()
