import numpy as np
from scipy.signal import freqz


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
        self.UI.z_plane.plot(np.real(self.poles), np.imag(self.poles), symbol='x', symbolSize=10)
        self.UI.z_plane.plot(np.real(self.poles_conjugates), np.imag(self.poles_conjugates), symbol='x', symbolSize=10)
        self.UI.z_plane.plot(np.real(self.zeros), np.imag(self.zeros), symbol='o', symbolSize=10)
        self.UI.z_plane.plot(np.real(self.zeros_conjugates), np.imag(self.zeros_conjugates), symbol='o', symbolSize=10)
        self.UI.z_plane.setAspectLocked(True)
        self.plot_frequency_response()

    def add_zeros_poles(self):
        # TODO: taha change the mag and phase slider values to float, how? need to search then return this line complex(mag, phase)
        if self.UI.zeros_button.isChecked():
            mag = self.UI.mag_slider.value()
            phase = self.UI.phase_slider.value()
            self.zeros.append(0.5 + 0.5j)  # testing only do not delete
            self.plot_unit_circle()
        elif self.UI.pole_button.isChecked():
            mag = self.UI.mag_slider.value()
            phase = self.UI.phase_slider.value()
            self.poles.append(-0.5 - 0.5j)  # testing only do not delete
            self.plot_unit_circle()

    def add_conjugates(self):
        self.poles_conjugates = np.conjugate(self.poles)
        self.zeros_conjugates = np.conjugate(self.zeros)
        self.plot_unit_circle()

    def reset_sliders(self):
        self.UI.mag_slider.setValue(0)
        self.UI.phase_slider.setValue(0)
        self.UI.mag_LCD.display(0)
        self.UI.phase_LCD.display(0)

    def clear_placement(self):
        # Get the current text of the combo box
        current_text = self.UI.Clear_combobox.currentText()
        # dictionary mapping options to lists
        clear_options = {
            "all zeros": (self.zeros, self.zeros_conjugates),
            "all poles": (self.poles, self.poles_conjugates),
            "clear all": (self.zeros, self.zeros_conjugates, self.poles, self.poles_conjugates)}

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

