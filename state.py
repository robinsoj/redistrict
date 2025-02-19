from graphic_primatives import *
from enum import Enum
import random
from colors import *

class State:
    def __init__(self, name, districts, precincts):
        self.name = name
        self.districts = []
        self.precincts = precincts
        self.district_count = districts
        self.district_colors = []
        for i in range(self.district_count):
            print(i)
    
    def update_district(self, precinct, district_number):
        for pre in self.precincts:
            if precinct.boundaries == pre.boundaries:
                pre.assign_color(list(Color)[district_number].value, district_number)
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
        for other in other_precincts:
            for other_polygon in other.boundaries:
                if all(self.is_point_inside_polygon(vertex, other_polygon.points) for vertex in polygon.boundaries[0].points):
                    return True
        return False
        
    def find_border_polygons(self, districtNum):
        if districtNum > len(self.districts):
            return

        # Remove completely internal polygons from set1
        set1 = [polygon for polygon in self.districts[districtNum] if not self.is_polygon_inside(polygon, self.districts[districtNum])]
        if set1 == []:
            set1 = self.districts[districtNum]
        border_polygons = []
        for polygon2 in self.precincts:
            if polygon2 not in set1:
                for polygon1 in set1:
                    if self.are_polygons_connected(polygon1.boundaries, polygon2.boundaries) and polygon2.district == -1:
                        border_polygons.append(polygon2.boundaries)
                        break
        return border_polygons
    
    def seed_initial_district(self):
        for i in range(self.district_count):
            dist_list = []
            while len(dist_list) == 0:
                random_precinct = random.choice(self.precincts)
                if random_precinct.district == -1:
                    self.update_district(random_precinct, i)
                    dist_list.append(random_precinct)
                    self.districts.append(dist_list)
    """
    Rework this logic so that it actually works
    """
    def populate_districts(self):
        curr_district = 0
        total_precincts = 0
        for pre in self.precincts:
            if pre.district == -1:
                total_precincts += 1
        
        while total_precincts > 0:
            target_precints = 0
            target_precints = self.find_border_polygons(curr_district)
            if target_precints != []:
                random_precinct = random.choice(target_precints)
                if random_precinct == -1:
                    total_precincts -= 1
                    self.update_district(random_precinct, curr_district)
                    self.districts[curr_district].append(random_precinct)
            curr_district += 1
            if curr_district >= self.district_count:
                curr_district = 0


def main():
    print("In main")
    print(list(Color)[0].value)
    #for color in Color:
    #    print(color.value)

if __name__ == "__main__":
    main()