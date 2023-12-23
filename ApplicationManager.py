import numpy as np
from scipy.signal import freqz
from Classes import *

# TODO: taha make the zeros and poles dragable (note: check your last research you reached a solid point)
# TODO: taha check for repetition after finishing all the todos
# TODO: taha check why function clear and reset together need two actions to work not only one action and also check if there is problem when switching
class AppManager:
    def __init__(self, ui):
        self.UI = ui
        self.Filters = set()
        # Create lists to store poles and zeros
        self.poles = []
        self.zeros = []
        

    def plot_unit_circle(self):
        self.UI.z_plane.clear()
        # Generate points on the unit circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)

        # Plot the unit circle
        self.UI.z_plane.plot(x, y)
        # Plot poles and zeros
        self.UI.z_plane.plot(np.real(self.poles), np.imag(self.poles), pen=None,symbol='x', symbolSize=10)
        self.UI.z_plane.plot(np.real(self.zeros), np.imag(self.zeros), pen=None,symbol='o', symbolSize=10)
        self.UI.z_plane.setAspectLocked(True)
        self.plot_frequency_response()

    def add_zeros_poles(self):
        # TODO: taha change the mag and phase slider values to float, how? need to search then return this line complex(mag, phase)
        if self.UI.zeros_radioButton.isChecked():
            zero = Zero(0.5 + 0.5j)
            self.zeros.append(zero.coordinates)  # testing only do not delete
            self.plot_unit_circle()
        elif self.UI.pole_radioButton.isChecked():
            zero = Zero(0.5 + 0.5j)
            self.poles.append(-0.5 - 0.5j)  # testing only do not delete
            self.plot_unit_circle()

    def add_conjugates(self):
        for pole in self.poles:
            if not pole.has_conjugate:
                pole.has_conjugate = True
                pole_conj = Pole(np.conjugate(pole), True)
                self.poles.append(pole_conj)
        for zero in self.zeros:
            if not zero.has_conjugate:
                zero.has_conjugate = True
                zer_conj = Zero(np.conjugate(zero), True)
                self.zeros.append(zer_conj)
        self.plot_unit_circle()

    def clear_placement(self):
        # Get the current text of the combo box
        current_text = self.UI.Clear_combobox.currentText()
        # dictionary mapping options to lists
        clear_options = {
            "all zeros": (self.zeros),
            "all poles": (self.poles),
            "clear all": (self.zeros, self.poles)}

        # Clear the selected lists based on the current option
        for clear_list in clear_options.get(current_text, []):
            clear_list.clear()
        # TODO: taha add current delete after finishing the highlighting functionality
        self.plot_unit_circle()

    def plot_frequency_response(self):
        # Calculate frequency response
        w, h = freqz(np.poly(self.zeros), np.poly(self.poles), worN=8000)
        # Extract magnitude and phase
        magnitude_response = np.abs(h)
        phase_response = np.angle(h)
        self.UI.Magnitude_graph.clear()
        self.UI.Magnitude_graph.setLabel('bottom', 'Frequency', units='Hz')
        self.UI.Magnitude_graph.setLabel('left', 'Magnitude', units='dB')
        self.UI.Magnitude_graph.addLegend()
        # Plot magnitude response
        self.UI.Magnitude_graph.plot(w, 20 * np.log10(magnitude_response))

        # Create a new PlotWidget for the phase response
        self.UI.Phase_graph.clear()
        self.UI.Phase_graph.setLabel('bottom', 'Frequency', units='Hz')
        self.UI.Phase_graph.setLabel('left', 'Phase', units='degrees')
        self.UI.Phase_graph.addLegend()
        # Plot phase response
        self.UI.Phase_graph.plot(w, np.degrees(phase_response))

