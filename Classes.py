class Signal:
    def __init__(self):
        pass


class Filter:
    def __init__(self):
        self.zeros = []
        self.poles = []


class Zero:
    def __init__(self,coordinates,  conj = False):
        self.coordinates = coordinates
        self.has_conjugate= conj
    
    
class Pole:
    def __init__(self,coordinates,  conj = False):
        self.coordinates = coordinates
        self.has_conjugate= conj