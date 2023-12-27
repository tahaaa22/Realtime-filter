import numpy as np
from scipy.signal import freqz
from PyQt5.QtCore import QTimer
class Signal:
    def __init__(self, real_signal_graph, filtered_signal_graph):
        self.y_coordinates = []
        self.x_coordinates = []
        self.graph1 = real_signal_graph
        self.graph2 = filtered_signal_graph
        self.X_Points_Plotted = 0

    def add_point(self, y):
        self.y_coordinates.append(y)
        self.x_coordinates = np.arange(len(self.y_coordinates))

    def plot_signal(self):
        self.X_Points_Plotted += 1
        self.graph1.setLimits(xMin = 0, xMax = float('inf'))
        self.graph1.plot(self.x_coordinates, self.y_coordinates)
        if self.X_Points_Plotted < 50:
            self.graph1.getViewBox().setXRange(self.x_coordinates[0], self.x_coordinates[-1])
        else:
            self.graph1.getViewBox().setXRange(self.x_coordinates[self.X_Points_Plotted - 50], self.x_coordinates[-1])


class Filter:
    def __init__(self, pole : complex = None):
        self.zeros = set()
        self.poles = set()
        if pole:
            chosen_pole = Pole(pole)
            calculated_zero = Zero(1 / pole.conjugate())
            self.poles.add(chosen_pole)
            self.zeros.add(calculated_zero)
        self.mag_response = None
        self.phase_response = None
        self.frequencies = None
        self.frequency_response = None

    def add_zero_pole(self, char : str, element):
        if char == 'z':
            self.zeros.add(element)
        else:
            self.poles.add(element)

    def add_conjugates(self):
        for pole in self.poles:
            if not pole.has_conjugate:
                pole.has_conjugate = True
                pole_conj = Pole(np.conjugate(pole), True)
                self.poles.add(pole_conj)
        for zero in self.zeros:
            if not zero.has_conjugate:
                zero.has_conjugate = True
                zer_conj = Zero(np.conjugate(zero), True)
                self.zeros.add(zer_conj)

    def calculate_frequency_response(self):
        if len(self.zeros) == 0 and len(self.poles) == 0:
            return
        self.frequencies, self.frequency_response = freqz(np.poly([zero.coordinates for zero in self.zeros]), np.poly([pole.coordinates for pole in self.poles]), worN=8000)
        self.mag_response = np.abs(self.frequency_response)
        self.phase_response = np.angle(self.frequency_response)

class Zero:
    def __init__(self, coordinates : complex, conj : bool = False):
        self.coordinates = coordinates
        self.has_conjugate= conj
    
class Pole:
    def __init__(self, coordinates : complex, conj : bool = False):
        self.coordinates = coordinates
        self.has_conjugate= conj
