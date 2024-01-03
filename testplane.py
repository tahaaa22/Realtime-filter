 def remove_current(self):
            self.clicked_points.remove((self.cursor_x_coordinates, self.cursor_y_coordinates))
            
    def mousePressEvent(self, event):
        if event.button() == pg.QtCore.Qt.LeftButton:
                mouse_point = self.plotItem.vb.mapSceneToView(event.pos())
                self.cursor_x_coordinates, self.cursor_y_coordinates = round(mouse_point.x(), 1), round(mouse_point.y(), 1)
                
        if not self.Maestro.isExist(self.cursor_x_coordinates, self.cursor_y_coordinates):
                # Check if the new point is within the area
                is_within_area = self.Maestro.currentPlacement(self.cursor_x_coordinates,self.cursor_y_coordinates)
                if is_within_area:
                        self.mouse_dragging = True
                        self.selected_point = True
                        self.last_mouse_pos = mouse_point
                
                if not is_within_area:
                    Maestro.highlightedX = self.cursor_x_coordinates
                    Maestro.highlightedY = self.cursor_y_coordinates
                    self.Maestro.add_zeros_poles(self.cursor_x_coordinates, self.cursor_y_coordinates)
                    # Create and add the new clicked point
                    self.addedPoint = ScatterPlotItem()
                    self.addedPoint.addPoints(x=[self.cursor_x_coordinates], y=[self.cursor_y_coordinates], brush='r')
                    self.addItem(self.addedPoint)
                                    
        else: # check dragging 
                self.mouse_dragging = True
                self.removeItem(self.addedPoint)
                if (self.Maestro.currentPlacement(self.cursor_x_coordinates,self.cursor_y_coordinates)):
                        self.addedPoint = ScatterPlotItem()
                        self.addedPoint.addPoints(x=[self.cursor_x_coordinates], y=[self.cursor_y_coordinates], brush='r')
                        self.addItem(self.addedPoint)
                        Maestro.highlightedX = self.cursor_x_coordinates
                        Maestro.highlightedY = self.cursor_y_coordinates
                        self.mouse_dragging = True
                        is_within_area = True
                        self.selected_point = True
                        self.last_mouse_pos = mouse_point
                
    def mouseMoveEvent(self, event):
        if self.mouse_dragging and self.selected_point:
            # Update the selected point's coordinates
            x_old = round(self.last_mouse_pos.x(), 1)
            y_old = round(self.last_mouse_pos.y(),1)
            current_position = self.plotItem.vb.mapSceneToView(event.pos())
            self.clicked_points = round(current_position.x(),1), round(current_position.y(),1)
            self.Maestro.set_newCoordinates(x_old, y_old, self.clicked_points)
            self.last_mouse_pos = current_position

    def mouseReleaseEvent(self, event):
        if event.button() == pg.QtCore.Qt.LeftButton:
            self.mouse_dragging = False
            self.selected_point = False
            
