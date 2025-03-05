from graphic_primatives import *

class Precinct:
    def __init__(self, boundaries, rep, dem, oth, name):
        self.name = name
        self.rep = rep
        self.dem = dem
        self.oth = oth
        self.boundaries = boundaries
        self.district = -1

    def assign_color(self, color, district):
        self.boundaries.fill_color = color
        self.district = district
    
    def __eq__(self, value):
        return self.boundaries == value.boundaries