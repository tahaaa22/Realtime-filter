from Classes import *
from PyQt5.QtWidgets import QFileDialog
import wfdb
import warnings


class AppManager:
    def __init__(self, ui):
        self.UI = ui
        self.tabs_z_planes = [ui.z_plane, ui.z_plane_2]
        self.Filters = [Filter(), Filter(0.5 + 0.5j), Filter(-0.5 + 0.5j), Filter(0.5 - 0.5j), Filter(-0.5 - 0.5j)]
        self.designed_filter = self.Filters[0] # Filter at index 0 will always be the main filter
        self.custom_allpass_filters = 0
        self.mouse_signal = Signal(ui.real_signal, ui.filtered_signal, self.designed_filter)
        self.loaded_signal = Signal(ui.real_signal, ui.filtered_signal, self.designed_filter)
        self.corrected_phase = None
        self.corrected_freqs = None
        self.highlightedX = None
        self.highlightedY = None
    
    
    def currentPlacement(self, x,y):
        current_list = list(self.designed_filter.zeros.union(self.designed_filter.poles))
        for i in range(self.update_lists()):
            x_i, y_i = current_list[i].coordinates.real, current_list[i].coordinates.imag
            if abs(x - x_i) < 0.1 and abs(y- y_i) < 0.1:
                if current_list[i].has_conjugate:
                    self.UI.add_conjugates.setChecked(True)
                else:
                    self.UI.add_conjugates.setChecked(False)
                return True
        return False        
                    
    def update_lists(self):
        return len(self.designed_filter.zeros) + len(self.designed_filter.poles)
    
    def isExist(self, x, y):
        for element in self.designed_filter.zeros.union(self.designed_filter.poles):
            if element.coordinates.real == x and element.coordinates.imag == y:
                return True
        return False
    
            
    def set_newCoordinates(self, x_old, y_old, new_placement_tuple):
        current_placement = None
        for element in self.designed_filter.zeros.union(self.designed_filter.poles):
            if element.coordinates.real == x_old and element.coordinates.imag == y_old:
                if isinstance(element, Zero):
                    if element.has_conjugate:
                        self.designed_filter.zeros.remove(element.conj)
                    self.designed_filter.zeros.remove(element)
                    Hasconj = element.has_conjugate
                    current_placement = "z"
                elif isinstance(element, Pole):
                    if element.has_conjugate:
                        self.designed_filter.poles.remove(element.conj)
                    self.designed_filter.poles.remove(element)
                    Hasconj = element.has_conjugate
                    current_placement = "p"
                break  # Break the loop since you found and removed the point
        x,y = new_placement_tuple
        self.add_zeros_poles(x, y, current_placement, Hasconj)

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
        if tab_num == 0 and len(self.designed_filter.zeros) > 0:
            self.designed_filter.calculate_frequency_response()
            self.plot_response('D', self.designed_filter)

    def plot_zeros_poles(self, tab_num : int, filter_number):
        self.tabs_z_planes[tab_num].plot([zero.coordinates.real for zero in self.Filters[filter_number].zeros],
                             [zero.coordinates.imag for zero in self.Filters[filter_number].zeros], pen=None, symbol='o',
                             symbolSize=10, pxMode=True)
        self.tabs_z_planes[tab_num].plot([pole.coordinates.real for pole in self.Filters[filter_number].poles],
                             [pole.coordinates.imag for pole in self.Filters[filter_number].poles], pen=None, symbol='x',
                             symbolSize=10)

    def add_zeros_poles(self, x, y, selector = None, hasConj = None):
        if self.UI.zeros_radioButton.isChecked() or selector == "z":
            temp_zero = Zero(x + y * 1j)
            if hasConj:
                conjugate = Zero(x - y* 1j)
                conjugate.has_conjugate = True
                temp_zero.conj = conjugate
                conjugate.conj = temp_zero
                self.designed_filter.add_zero_pole('z', conjugate)
                #self.Control_Conj(x, y , selector) # there is a better and professional way for this, which is by applying deep copying
                temp_zero.has_conjugate = True
            self.designed_filter.add_zero_pole('z', temp_zero)
        else:
            temp_pole = Pole(x + y * 1j)
            self.designed_filter.add_zero_pole('p', temp_pole)
            if hasConj:
                conjugate = Pole(x - y* 1j)
                conjugate.has_conjugate = True
                temp_pole.conj = conjugate
                conjugate.conj = temp_pole
                self.designed_filter.add_zero_pole('p', conjugate)
                #self.Control_Conj(x, y , selector) # there is a better and professional way for this, which is by applying deep copying
                temp_pole.has_conjugate = True
       
        self.plot_unit_circle(0) # added 0 for testing remove it if it is wrong

    def add_conjugates(self):
        if self.UI.add_conjugates.isChecked():
            self.designed_filter.add_conjugates(self.highlightedX, self.highlightedY)
            self.plot_unit_circle(0)

    def clear_placement(self, x = None, y = None, draggable = False):
        # Get the current text of the combo box
        current_text = self.UI.Clear_combobox.currentText()
        if current_text == "current":
            # Iterate through the list of zeros
            for zero in self.designed_filter.zeros:
                if zero.coordinates.real == self.highlightedX and zero.coordinates.imag == self.highlightedY:
                    self.designed_filter.zeros.remove(zero)
                    self.designed_filter.zeros.remove(zero.conj) #comment lw tele3 kalamk sa7 w doctor 3awezha keda
                    break  # Break the loop since you found and removed the point
            # Iterate through the list of poles
            for pole in self.designed_filter.poles:
                if pole.coordinates.real == self.highlightedX and pole.coordinates.imag == self.highlightedY:
                    self.designed_filter.poles.remove(pole)
                    self.designed_filter.poles.remove(pole.conj)  #comment lw tele3 kalamk sa7 w doctor 3awezha keda
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
        self.plot_unit_circle(0) # added 0 for testing remove it if it is wrong

    # noinspection PyBroadException
    def plot_response(self, tab : str, filter_obj : Filter):
        filter_obj.calculate_frequency_response()
        self.calculate_corrected_phase()
        try:
            if tab == 'D':
                self.adjust_graphs(self.UI.Magnitude_graph, 'Magnitude', 'dB')
                self.adjust_graphs(self.UI.Phase_graph, 'Phase', 'radian')
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    self.UI.Magnitude_graph.plot(filter_obj.frequencies, 20 * np.log10(filter_obj.mag_response))
                self.UI.Phase_graph.plot(filter_obj.frequencies, filter_obj.phase_response)
            else:
                self.adjust_graphs(self.UI.Phase_Response_Graph, 'Phase', 'radian')
                self.adjust_graphs(self.UI.corrected_phase, 'Phase', 'radian')
                self.UI.Phase_Response_Graph.plot(filter_obj.frequencies, filter_obj.phase_response)
                self.UI.corrected_phase.plot(self.corrected_freqs, self.corrected_phase)
        except Exception:
            return

    @staticmethod
    def adjust_graphs(graph, title : str, units : str):
        graph.clear()
        graph.setLabel('bottom', 'Frequency', units='Hz')
        graph.setLabel('left', title, units=units)
        graph.addLegend()

    def display_allpass_filter(self, index : int):
        self.plot_unit_circle(1, index + 1)
        self.plot_response('C', self.Filters[index + 1])

    def display_tab(self, index : int):
        if index == 1:
            self.plot_unit_circle(1, self.UI.filter_combobox.currentIndex() + 1)
            self.plot_response('C', self.Filters[self.UI.filter_combobox.currentIndex() + 1])
        else:
            self.plot_unit_circle(0)
            self.plot_response('D', self.designed_filter)

    def add_filter(self):
        # Please be advised that | is the symbol for set intersection in python
        self.designed_filter.zeros |= self.Filters[self.UI.filter_combobox.currentIndex() + 1].zeros
        self.designed_filter.poles |= self.Filters[self.UI.filter_combobox.currentIndex() + 1].poles

    def delete_filter(self):
        # Please be advised that - is the symbol for set difference in python
        self.designed_filter.zeros -= self.Filters[self.UI.filter_combobox.currentIndex() + 1].zeros
        self.designed_filter.poles -= self.Filters[self.UI.filter_combobox.currentIndex() + 1].poles

    def track_cursor(self, event):
        if not self.UI.touch_pad_radioButton.isChecked():
            return
        # Get the cursor position in view coordinates
        cursor_position = event.pos()
        cursor_y = cursor_position.y()
        self.mouse_signal.add_point(cursor_y)
        self.mouse_signal.plot_signal()

    def load_signal(self):
        self.clear_graphs()
        self.loaded_signal.timer = None
        self.loaded_signal.X_Points_Plotted = 0
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "", "All Files (*)")
        if File_Path:
            Coordinates_List = ["x", "y", "f"]
            loaded_data = pd.read_csv(File_Path, usecols=Coordinates_List)
            self.loaded_signal.x_coordinates = loaded_data["x"]
            self.loaded_signal.y_coordinates = loaded_data["y"]
            max_frequency = loaded_data["f"]
            self.loaded_signal.max_freq = max_frequency[0]
            self.loaded_signal.plot_ECG()

    def touchpad_toggled(self):
        if self.UI.touch_pad_radioButton.isChecked():
            self.clear_graphs()
            self.loaded_signal.timer = None

    def clear_graphs(self):
        self.UI.real_signal.clear()
        self.UI.filtered_signal.clear()

    def calculate_corrected_phase(self):
        self.corrected_freqs , frequency_response = freqz(np.poly([zero.coordinates for zero in self.designed_filter.zeros
        | self.Filters[self.UI.filter_combobox.currentIndex() + 1].zeros]),
                                                          np.poly([pole.coordinates for pole in self.designed_filter.poles
                                                                   | self.Filters[self.UI.filter_combobox.currentIndex() + 1].poles]), worN=8000)
        self.corrected_phase = np.angle(frequency_response)

    def insert_custom_allpass(self):
        try:
            # First we obtain the value of the custom pole coordinates and append it in the combobox
            chosen_a = complex(self.UI.custom_filter_text.text())
            self.custom_allpass_filters += 1
            self.UI.filter_combobox.addItem(str(chosen_a))
            # Secondly we create the filter and append it to Filters list
            self.Filters.append(Filter(complex(self.UI.custom_filter_text.text())))
            self.UI.filter_combobox.setCurrentIndex(3 + self.custom_allpass_filters)
            self.UI.custom_filter_text.setText("")
        except ValueError:
            print(f"Invalid input {self.UI.custom_filter_text.text()}")

    def update_temporal_resolution(self, value: int):
        target_signal = self.mouse_signal if self.UI.touch_pad_radioButton.isChecked() else self.loaded_signal
        target_signal.temporal_resolution = value
