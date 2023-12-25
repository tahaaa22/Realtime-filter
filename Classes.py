import numpy as np
from scipy.signal import freqz
class Signal:
    def __init__(self):
        pass


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
        self.complex_frequencies = None

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
        self.frequencies, self.complex_frequencies = freqz(np.poly(list(self.zeros)), np.poly(list(self.poles)), worN=8000)
        self.mag_response = np.abs(self.complex_frequencies)
        self.phase_response = np.angle(self.complex_frequencies)

class Zero:
    def __init__(self, coordinates : complex, conj : bool = False):
        self.coordinates = coordinates
        self.has_conjugate= conj
    
class Pole:
    def __init__(self, coordinates : complex, conj : bool = False):
        self.coordinates = coordinates
        self.has_conjugate= conj
