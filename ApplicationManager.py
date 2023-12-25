from Classes import *

# TODO: taha make the zeros and poles dragable (note: check your last research you reached a solid point)
# TODO: taha check for repetition after finishing all the todos

class AppManager:
    def __init__(self, ui):
        self.UI = ui
        self.tabs_z_planes = [ui.z_plane, ui.z_plane_2]
        self.Filters = [Filter(), Filter(0.5 + 0.5j), Filter(-0.5 + 0.5j), Filter(0.5 - 0.5j), Filter(-0.5 - 0.5j)]
        self.designed_filter = self.Filters[0] # Filter at index 0 will always be the main filter

        
    def set_newCoordinates(self,new, x_old, y_old, new_placement_tuple):
        for zero in self.designed_filter.zeros:
                if zero.coordinates.real == x_old and zero.coordinates.imag == y_old:
                    self.designed_filter.zeros.remove(zero)
                    break  # Break the loop since you found and removed the point
            # Iterate through the list of poles
        for pole in self.designed_filter.poles:
            if pole.coordinates.real == x_old and pole.coordinates.imag == y_old:
                self.designed_filter.poles.remove(pole)
                break  # Break the loop since you found and removed the point
        x,y = new_placement_tuple
        self.add_zeros_poles(x, y)
        
    def plot_unit_circle(self, tab_num : int, filter_number : int = 0):
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        self.tabs_z_planes[tab_num].clear()
        self.tabs_z_planes[tab_num].plot(x, y)
        # Draw vertical and horizontal lines passing through the center
        self.tabs_z_planes[tab_num].plot([0, 0], [-1, 1])
        self.tabs_z_planes[tab_num].plot([-1, 1], [0, 0])
        self.tabs_z_planes[tab_num].setAspectLocked(True)
        self.plot_zeros_poles(tab_num, filter_number)
        #self.designed_filter.calculate_frequency_response()
        #self.plot_response('D', self.designed_filter)

    def plot_zeros_poles(self, tab_num : int, filter_number):
        self.tabs_z_planes[tab_num].plot([zero.coordinates.real for zero in self.Filters[filter_number].zeros],
                             [zero.coordinates.imag for zero in self.Filters[filter_number].zeros], pen=None, symbol='o',
                             symbolSize=10, pxMode=True)
        self.tabs_z_planes[tab_num].plot([pole.coordinates.real for pole in self.Filters[filter_number].poles],
                             [pole.coordinates.imag for pole in self.Filters[filter_number].poles], pen=None, symbol='x',
                             symbolSize=10)

    def add_zeros_poles(self, x, y):
        if self.UI.zeros_radioButton.isChecked():
            temp_zero = Zero(x + y * 1j)
            self.designed_filter.add_zero_pole('z', temp_zero)
        else:
            temp_pole = Pole(x + y * 1j)
            self.designed_filter.add_zero_pole('p', temp_pole)
            
        self.plot_unit_circle()

    def add_conjugates(self):
        self.designed_filter.add_conjugates()
        self.plot_unit_circle()

    def clear_placement(self, x = None, y = None, dragable = False):
        # Get the current text of the combo box
        current_text = self.UI.Clear_combobox.currentText()
        if current_text == "current" or dragable:
            # Iterate through the list of zeros
            for zero in self.designed_filter.zeros:
                if zero.coordinates.real == x and zero.coordinates.imag == y:
                    self.designed_filter.zeros.remove(zero)
                    break  # Break the loop since you found and removed the point
            # Iterate through the list of poles
            for pole in self.designed_filter.poles:
                if pole.coordinates.real == x and pole.coordinates.imag == y:
                    self.designed_filter.poles.remove(pole)
                    break  # Break the loop since you found and removed the point

        # dictionary mapping options to lists
        clear_options = {
            "all zeros": self.designed_filter.zeros,
            "all poles": self.designed_filter.poles,
            "all": (self.designed_filter.zeros, self.designed_filter.poles)}
    
        # Clear the selected lists based on the current option
        if current_text == "all":
            zeros_list, poles_list = clear_options.get(current_text, [])
            zeros_list.clear()
            poles_list.clear()
        else:
            clear_list = clear_options.get(current_text, [])
            clear_list.clear()
        # TODO: taha add current delete after finishing the highlighting functionality
        self.plot_unit_circle()

    def plot_response(self, tab : str, filter_obj : Filter):
        if filter_obj.frequencies is None:
            return
        if tab == 'D':
            self.UI.Magnitude_graph.clear()
            self.UI.Magnitude_graph.setLabel('bottom', 'Frequency', units='Hz')
            self.UI.Magnitude_graph.setLabel('left', 'Magnitude', units='dB')
            self.UI.Magnitude_graph.addLegend()
            self.UI.Phase_graph.clear()
            self.UI.Phase_graph.setLabel('bottom', 'Frequency', units='Hz')
            self.UI.Phase_graph.setLabel('left', 'Phase', units='degrees')
            self.UI.Phase_graph.addLegend()
            self.UI.Magnitude_graph.plot(filter_obj.frequencies, 20 * np.log10(filter_obj.mag_response))
            self.UI.Phase_graph.plot(filter_obj.frequencies, np.degrees(filter_obj.phase_response))

        else:
            self.UI.Phase_Response_Graph.clear()
            self.UI.Phase_Response_Graph.setLabel('bottom', 'Frequency', units='Hz')
            self.UI.Phase_Response_Graph.setLabel('left', 'Phase', units='degrees')
            self.UI.Phase_Response_Graph.addLegend()
            self.UI.corrected_phase.clear()
            self.UI.corrected_phase.setLabel('bottom', 'Frequency', units='Hz')
            self.UI.corrected_phase.setLabel('left', 'Phase', units='degrees')
            self.UI.corrected_phase.addLegend()
            self.UI.Phase_Response_Graph.plot(filter_obj.frequencies, np.degrees(filter_obj.phase_response))

    def display_allpass_filter(self, index : int):
        self.plot_unit_circle(1, index + 1)

    def display_tab(self, index : int):
        if index == 1:
            self.plot_unit_circle(1, self.UI.filter_combobox.currentIndex() + 1)

