from Classes import *

# TODO: taha make the zeros and poles dragable (note: check your last research you reached a solid point)
# TODO: taha check for repetition after finishing all the todos
# TODO: taha check why function clear and reset together need two actions to work not only one action and also check if there is problem when switching
class AppManager:
    def __init__(self, ui):
        self.UI = ui
        self.Filters = [] # Filter at index 0 will always be the main filter
        self.designed_filter = Filter()
        self.Filters.append(self.designed_filter)
        

    def plot_unit_circle(self):
        self.UI.z_plane.clear()
        # Generate points on the unit circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)

        # Plot the unit circle
        self.UI.z_plane.plot(x, y)
        # Draw vertical and horizontal lines passing through the center
        self.UI.z_plane.plot([0, 0], [-1, 1])
        self.UI.z_plane.plot([-1, 1], [0, 0])
        # self.UI.z_plane.plot([zero.coordinates.real for zero in self.zeros], [zero.coordinates.imag for zero in self.zeros], pen=None, symbol='o', symbolSize=10)
        # self.UI.z_plane.plot([pole.coordinates.real for pole in self.poles], [pole.coordinates.imag for pole in self.poles], pen=None, symbol='x', symbolSize=10)

        self.UI.z_plane.setAspectLocked(True)

        self.UI.z_plane_2.plot(x, y)
        self.UI.z_plane_2.plot([0, 0], [-1, 1])
        self.UI.z_plane_2.plot([-1, 1], [0, 0])
        self.UI.z_plane_2.setAspectLocked(True)
        self.designed_filter.plot_mag_response()
        self.designed_filter.plot_phase_response()

    def add_zeros_poles(self):
        if self.UI.zeros_radioButton.isChecked():
            self.designed_filter.add_zero_pole('z', 0.5 + 0.5j)
        else:
            self.designed_filter.add_zero_pole('p', 0.5 + 0.5j)
        self.plot_unit_circle()

    def add_conjugates(self):
        self.designed_filter.add_conjugates()
        self.plot_unit_circle()

    # def clear_placement(self):
    #     # Get the current text of the combo box
    #     current_text = self.UI.Clear_combobox.currentText()
    #     # dictionary mapping options to lists
    #     clear_options = {
    #         "all zeros": (self.zeros),
    #         "all poles": (self.poles),
    #         "clear all": (self.zeros, self.poles)}
    #
    #     # Clear the selected lists based on the current option
    #     for clear_list in clear_options.get(current_text, []):
    #         clear_list.clear()
    #     # TODO: taha add current delete after finishing the highlighting functionality
    #     self.plot_unit_circle()

    def plot_response(self, tab : str, filter_obj : Filter):
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



