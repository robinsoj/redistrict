from graphic_primatives import *
from enum import Enum
import random
from colors import *
from district_census import *

class State:
    def __init__(self, name, districts, precincts):
        self.name = name
        self.districts = []
        self.precincts = precincts
        self.district_count = districts
        #self.district_colors = []
        self.census = []
        self.current_district = 0
        for i in range(self.district_count):
            self.census.append(District_Census())
    
    def update_district(self, precinct, district_number):
        for pre in self.precincts:
            if precinct.boundaries == pre.boundaries:
                pre.assign_color(list(Color)[district_number].value, district_number)
                self.census[district_number].add_precinct(pre)
                return

    def is_point_on_line_segment(self, point, line_start, line_end):
        cross_product = (point.y - line_start.y) * (line_end.x - line_start.x) - (point.x - line_start.x) * (line_end.y - line_start.y)
        if abs(cross_product) > 1e-6:  # Use a small tolerance for floating-point comparison
            return False
        
        dot_product = (point.x - line_start.x) * (line_end.x - line_start.x) + (point.y - line_start.y) * (line_end.y - line_start.y)
        if dot_product < 0:
            return False

        squared_length = (line_end.x - line_start.x) ** 2 + (line_end.y - line_start.y) ** 2
        if dot_product > squared_length:
            return False

        return True

    def are_polygons_connected(self, polygon1, polygon2):
        pg1_sides = polygon1.sides()
        pg2_sides = polygon2.sides()

        for side1 in pg1_sides:
            for side2 in pg2_sides:
                if (
                    side1 == side2 
                    or side1 == side2[::-1]
                    or (self.is_point_on_line_segment(side1[0], *side2) and self.is_point_on_line_segment(side1[1], *side2))
                    or (self.is_point_on_line_segment(side2[0], *side1) and self.is_point_on_line_segment(side2[1], *side1))
                ):
                    return True
        return False

    def is_point_inside_polygon(self, point, polygon_points):
        x, y = point
        n = len(polygon_points)
        inside = False

        p1x, p1y = polygon_points[0]
        for i in range(n+1):
            p2x, p2y = polygon_points[i % n]
            if y == p1y == p2y and min(p1x, p2x) <= x <= max(p1x, p2x):
                return True
            
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def is_polygon_inside(self, polygon, other_precincts):
        
        if not polygon:
            return False
        for other in other_precincts:
            other_polygon = other.boundaries  # other.boundaries is a Polygon object
            # Check if all vertices of the polygon are inside the other_polygon
            if all(self.is_point_inside_polygon((vertex.x, vertex.y), [(p.x, p.y) for p in other_polygon.points]) for vertex in polygon.points):
                return True
        return False
        
    def find_border_precincts(self, districtNum):
        print(districtNum)
        #unable to find adjacent precincts.  I suspect that the borders are off by too much using float point comparisons.
        if districtNum >= len(self.districts):
            return []

        # Remove completely internal polygons from set1
        set1 = [precinct for precinct in self.districts[districtNum] if not self.is_polygon_inside(precinct.boundaries, self.districts[districtNum])]
        if not set1:
            set1 = self.districts[districtNum]
        
        border_precincts = []
        for precinct in self.precincts:
            #if precinct not in set1:
            if precinct.district == -1:
                for polygon1 in set1:
                    if self.are_polygons_connected(polygon1.boundaries, precinct.boundaries):
                        border_precincts.append(precinct)
                        break
        print(border_precincts)
        return border_precincts

    def seed_initial_district(self):
        for i in range(self.district_count):
            dist_list = []
            while len(dist_list) == 0:
                random_precinct = random.choice(self.precincts)
                if random_precinct.district == -1:
                    self.update_district(random_precinct, i)
                    dist_list.append(random_precinct)
                    self.districts.append(dist_list)
    
    def grab_neighboring_precinct(self, district):
        if district > len(self.districts):
            return
        border_polygons = self.find_border_precincts(district)
        if len(border_polygons) == 0:
            return
        random_precinct = random.choice(border_polygons)
        self.update_district(random_precinct, district)

    def find_adjacent_precincts(self, district):
        adjacent_precincts = []

        for precinct in self.precincts:
            if precinct.district == district:
                for other_precinct in self.precincts:
                    if precinct.district != other_precinct.district and self.are_polygons_connected(precinct.boundaries, other_precinct.boundaries):
                        adjacent_precincts.append(precinct)
                        break

        return adjacent_precincts
    
    def count_unassigned_precincts(self):
        count = 0
        for precinct in self.precincts:
            if precinct.district == -1:
                count += 1
        return count
    
    def update(self):
        if self.count_unassigned_precincts() > 0:
            self.grab_neighboring_precinct(self.current_district)
            self.current_district += 1
            if self.current_district == self.district_count:
                self.current_district = 0
        else:
            max = 100000000
            min_dist = -1
            for i in range(len(self.census)):
                voters = self.census[i].total_voters
                if voters < max:
                    max = voters
                    min_dist = i
            adjacent_precincts = self.find_adjacent_precincts(min_dist)
            choice = random.choice(adjacent_precincts)
            self.census[choice.district].remove_precinct(choice)
            self.update_district(choice, choice)

def main():
    print("In main")
    print(list(Color)[0].value)
    #for color in Color:
    #    print(color.value)

if __name__ == "__main__":
    main()