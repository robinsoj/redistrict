from precinct import *

class District_Census:
    def __init__(self):
        self.rep = 0
        self.dem = 0
        self.other = 0
    
    def add_precinct(self, precinct):
        self.rep += precinct.rep
        self.dem += precinct.dem
        self.other += precinct.oth
    
    def remove_precinct(self, precinct):
        self.rep -= precinct.rep
        self.dem -= precinct.dem
        self.other -= precinct.oth
    
    def total_voters(self):
        return self.rep + self.dem + self.other
    
    def total_dem(self):
        return self.dem

    def total_other(self):
        return self.other

    def total_rep(self):
        return self.rep
    
    def district_party(self):
        maximum = max(self.dem, self.other, self.rep)
        if maximum == self.dem:
            return "Democrat"
        if maximum == self.other:
            return "Independent"
        return "Republican"

