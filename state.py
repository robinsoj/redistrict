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
        self.unassigned_precincts = []
        for name in precincts.keys():
            self.unassigned_precincts.append(name)
        self.neighbor_map = {}
        random.seed()
        for i in range(self.district_count):
            self.census.append(District_Census())
    
    def update_district(self, precinct, district_number, color_override = None):
        if color_override is None:
            color_override = list(Color)[district_number].value
        #for pre in self.precincts:
        #    if precinct.name == pre.name:
        #        pre.assign_color(color_override, district_number)
        #        self.census[district_number].add_precinct(pre)
        #        return
        self.precincts[precinct].assign_color(color_override, district_number)
        self.census[district_number].add_precinct(self.precincts[precinct])

    def normalize_point(self, pt):
        return Point(round(pt.x, 6), round(pt.y, 6))

    def two_true(self, a, b, c, d):
        return (a + b + c + d) == 2
    
    def are_polygons_connected(self, polygon1, polygon2, report = False):
        pg1_sides = polygon1.sides()
        pg2_sides = polygon2.sides()
        t = 1.1
        tolerance = Point(t, t)  # Define the fuzzy tolerance for gaps in pixels

        if report:
            print(pg1_sides)
            print(pg2_sides)
        for side1 in pg1_sides:
            side1 = (self.normalize_point(side1[0]), self.normalize_point(side1[1]))
            for side2 in pg2_sides:
                side2 = (self.normalize_point(side2[0]), self.normalize_point(side2[1]))

                # Find bounds of both line segments
                min_x1, max_x1 = min(side1[0].x, side1[1].x), max(side1[0].x, side1[1].x)
                min_x2, max_x2 = min(side2[0].x, side2[1].x), max(side2[0].x, side2[1].x)
                min_y1, max_y1 = min(side1[0].y, side1[1].y), max(side1[0].y, side1[1].y)
                min_y2, max_y2 = min(side2[0].y, side2[1].y), max(side2[0].y, side2[1].y)

                if report:
                    print(side1, 
                          side2,
                          side1[0] - side2[0],
                          side1[1] - side2[1],
                          side1[0] - side2[1],
                          side1[1] - side2[0],
                          side1[0] - side2[0] < tolerance,
                          side1[1] - side2[1] < tolerance,
                          side1[0] - side2[1] < tolerance,
                          side1[1] - side2[0] < tolerance,
                          self.two_true((side1[0] - side2[0] < tolerance),
                                        (side1[1] - side2[1] < tolerance),
                                        (side1[0] - side2[1] < tolerance),
                                        (side1[1] - side2[0] < tolerance)))
                if ((side1[0] - side2[0] < tolerance) ^ (side1[1] - side2[1] < tolerance) ^ (side1[0] - side2[1] < tolerance)
                    ^ (side1[1] - side2[0] < tolerance)):
                    continue  # Skip if they only share a corner

                # Ensure that the overlapping region has measurable length
                if self.two_true((side1[0] - side2[0] < tolerance), 
                                 (side1[1] - side2[1] < tolerance),
                                 (side1[0] - side2[1] < tolerance),
                                 (side1[1] - side2[0] < tolerance)):
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
        #refactor this to handle the maps
        if districtNum >= len(self.districts):
            return []

        district = []
        for name in self.districts[districtNum]:
            district.append(self.precincts[name])

        # Filter out internal precincts
        set1 = [precinct for precinct in district if not self.is_polygon_inside(precinct.boundaries, district)]
        if not set1:
            set1 = district

        border_precincts = []
        #for precinct in self.precincts:
        #    if precinct.district == -1:  # Unassigned precinct
        #        for polygon1 in set1:
        #            # Check for connections with tolerance
        #            if self.are_polygons_connected(polygon1.boundaries, precinct.boundaries):
        #               border_precincts.append(precinct)
        #                break
        for precinct in district:
            for neighbor in self.neighbor_map[precinct.name]:
                if self.precincts[neighbor].district == -1:
                    border_precincts.append(neighbor)
        return border_precincts
    
    def build_neighbor_map(self, precinct):
        ret_val = []
        for p2 in self.precincts:
            #if precinct.name == 'apache2':
            #    print(precinct.name, p2, self.are_polygons_connected(precinct.boundaries, self.precincts[p2].boundaries))
            if precinct.name != p2 and self.are_polygons_connected(precinct.boundaries, self.precincts[p2].boundaries,
                                                                   precinct.name== 'maricopa225' and p2 == 'maricopa247' and False):
                ret_val.append(p2)
        return ret_val

    def process_precincts(self):
        count = 0
        for precinct in self.precincts.values():
            if count % 100 == 0:
                print(f"Processed {count} precincts.")
            count += 1
            neighbors = self.build_neighbor_map(precinct)
            self.neighbor_map[precinct.name] = neighbors
        #print(self.neighbor_map)
        
    def seed_initial_district(self):
        for i in range(self.district_count):
            dist_list = []
            while len(dist_list) == 0:
                random_precinct = random.choice(list(self.precincts.values()))
                if random_precinct.district == -1:
                    self.update_district(random_precinct.name, i)
                    dist_list.append(random_precinct.name)
                    self.districts.append(dist_list)
                    self.unassigned_precincts.remove(random_precinct.name)
    
    def grab_neighboring_precinct(self, district):
        if district > len(self.districts):
            return
        border_polygons = self.find_border_precincts(district)
        if len(border_polygons) == 0:
            return
        random_precinct = random.choice(border_polygons)
        self.update_district(random_precinct, district)
        self.districts[district].append(random_precinct)
        self.unassigned_precincts.remove(random_precinct)

    def find_adjacent_precincts(self, district):
        adjacent_precincts = []

        for precinct in self.districts[district]:
            for other_precinct in self.neighbor_map[precinct]:
                if self.precincts[other_precinct].district != district:
                    adjacent_precincts.append(other_precinct)

        return adjacent_precincts

    def select_district(self):
        max_voters = 100000000
        min_dist = -1
        for i in range(len(self.census)):
            voters = self.census[i].total_voters()
            if voters < max_voters:
                max_voters = voters
                min_dist = i
        return min_dist
    
    def update(self):
        if len(self.unassigned_precincts) > 0:
            self.grab_neighboring_precinct(self.current_district)
            self.current_district += 1
            if self.current_district == self.district_count:
                self.current_district = 0
        else:
            return
            min_dist = self.select_district()
            print(min_dist, self.census[min_dist].total_voters())
            adjacent_precincts = self.find_adjacent_precincts(min_dist)
            choice = random.choice(adjacent_precincts)
            self.census[self.precincts[choice].district].remove_precinct(self.precincts[choice])
            self.update_district(choice, min_dist)

def main():
    print("In main")
    print(list(Color)[0].value)
    #for color in Color:
    #    print(color.value)

if __name__ == "__main__":
    main()