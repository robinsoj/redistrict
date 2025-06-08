from graphic_primatives import *
from enum import Enum
import random
import math
from colors import *
from district_census import *
from datetime import datetime
import re

class State:
    def __init__(self, name, districts, precincts):
        self.name = name
        self.districts = []
        self.precincts = precincts
        self.district_count = districts
        #self.district_colors = []
        self.census = []
        self.centroids = []
        self.current_district = 0
        self.unassigned_precincts = []
        self.heuristic = None
        total_census = 0
        for name in precincts.keys():
            self.unassigned_precincts.append(name)
            total_census += precincts[name].rep + precincts[name].dem + precincts[name].oth
        self.neighbor_map = {}
        random.seed()
        for i in range(self.district_count):
            self.census.append(District_Census())
            self.centroids.append(Point(0, 0))
    
    def update_district(self, precinct, district_number, color_override = None):
        if color_override is None:
            color_override = list(Color)[district_number].value
        #for pre in self.precincts:
        #    if precinct.name == pre.name:
        #        pre.assign_color(color_override, district_number)
        #        self.census[district_number].add_precinct(pre)
        #        return
        old_district = self.precincts[precinct].district
        self.precincts[precinct].assign_color(color_override, district_number)
        self.census[district_number].add_precinct(self.precincts[precinct])
        pg = Polygon(None, [self.precincts[obj].boundaries.centroid for obj in self.precincts if self.precincts[obj].district == district_number])
        self.centroids[district_number] = pg.centroid
        if old_district != -1:
            pg = Polygon(None, [self.precincts[obj].boundaries.centroid for obj in self.precincts if self.precincts[obj].district == old_district])
            self.centroids[old_district] = pg.centroid

    def normalize_point(self, pt):
        return Point(round(pt.x, 6), round(pt.y, 6))

    def two_true(self, a, b, c, d):
        return (a + b + c + d) == 2
    
    def are_polygons_connected(self, polygon1, polygon2):
        pg1_sides = polygon1.sides()
        pg2_sides = polygon2.sides()
        t = 1.1
        tolerance = Point(t, t)  # Define the fuzzy tolerance for gaps in pixels

        for side1 in pg1_sides:
            side1 = (self.normalize_point(side1[0]), self.normalize_point(side1[1]))
            for side2 in pg2_sides:
                side2 = (self.normalize_point(side2[0]), self.normalize_point(side2[1]))

                # Find bounds of both line segments
                min_x1, max_x1 = min(side1[0].x, side1[1].x), max(side1[0].x, side1[1].x)
                min_x2, max_x2 = min(side2[0].x, side2[1].x), max(side2[0].x, side2[1].x)
                min_y1, max_y1 = min(side1[0].y, side1[1].y), max(side1[0].y, side1[1].y)
                min_y2, max_y2 = min(side2[0].y, side2[1].y), max(side2[0].y, side2[1].y)

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
            if precinct.name != p2 and self.are_polygons_connected(precinct.boundaries, self.precincts[p2].boundaries):
                ret_val.append(p2)
        return ret_val

    def process_precincts(self, cached_map = None):
        count = 0
        if cached_map is None:
            cached_map = {}
        for precinct in self.precincts.values():
            if count % 100 == 0:
                print(f"Processed {count} precincts: {datetime.now()}")
            count += 1
            if precinct.name not in cached_map:
                neighbors = self.build_neighbor_map(precinct)
            else:
                neighbors = cached_map[precinct.name]
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
        border_precincts = set()

        # Find precincts in the district that border another district
        for precinct in self.districts[district]:
            internal = True
            for neighbor in self.neighbor_map[precinct]:
                if self.precincts[neighbor].district != district:
                    internal = False
            if not internal:
                border_precincts.add(precinct)
        
        ret_val = set()
        
        for precinct in border_precincts:
            for neighbor in self.neighbor_map[precinct]:
                # Only consider neighbors not in the current district
                if self.precincts[neighbor].district != district:
                    # Check if removing neighbor from its district keeps it contiguous
                    # and if adding it to the target district keeps it contiguous
                    if (self._is_district_contiguous_after_removal(neighbor) and
                        self._is_district_contiguous_after_addition(neighbor, district)):
                        ret_val.add(neighbor)
        
        return list(ret_val)

    def _is_district_contiguous_after_removal(self, precinct):
        """
        Check if the district of the given precinct remains contiguous after removing it.
        Uses DFS to verify that all remaining precincts in the district are connected.
        """
        district = self.precincts[precinct].district
        district_precincts = set(self.districts[district]) - {precinct}
        
        if not district_precincts:
            return True  # Empty district is trivially contiguous
        
        # Start DFS from an arbitrary precinct in the district
        start_precinct = next(iter(district_precincts))
        visited = set()
        
        def dfs(current):
            visited.add(current)
            for neighbor in self.neighbor_map[current]:
                if neighbor in district_precincts and neighbor not in visited:
                    dfs(neighbor)
        
        dfs(start_precinct)
        
        # District is contiguous if all precincts were visited
        if len(visited) != len(district_precincts):
            return False
        return True

    def _is_district_contiguous_after_addition(self, precinct, target_district):
        """
        Check if adding the precinct to the target district keeps it contiguous.
        Simulates adding the precinct and checks connectivity.
        """
        # Simulate adding the precinct to the target district
        district_precincts = set(self.districts[target_district]) | {precinct}
        
        # Start DFS from an arbitrary precinct in the district
        start_precinct = next(iter(district_precincts))
        visited = set()
        
        def dfs(current):
            visited.add(current)
            for neighbor in self.neighbor_map[current]:
                if neighbor in district_precincts and neighbor not in visited:
                    dfs(neighbor)
        
        dfs(start_precinct)
        
        # District is contiguous if all precincts were visited
        if len(visited) != len(district_precincts):
            return False
        return True

    def cpvi_sort(self, district, party, str_split):
        pattern = r'(R|D)\+(\d{1,2})'
        cpvi = district[3]
        total_voters = district[4]
        match = re.search(pattern, cpvi)
        if not match:
            return (3, 0, total_voters)
        
        p, str = match.group(1), int(match.group(2))

        if p == party and str <= str_split:
            return (0, str, total_voters)
        elif p != party:
            return (1, str, total_voters)
        else:
            return (2, str, total_voters)

    def select_district(self):
        minimum = float('inf')
        min_dist = 0
        districts = []
        total_voters = 0

        for i in range(len(self.census)):
            rep = self.census[i].total_rep()
            dem = self.census[i].total_dem()
            total = self.census[i].total_voters()
            total_voters += total
            districts.append((i, rep, dem, self.generate_cpvi(rep, dem), total))
            if total < minimum:
                minimum = total
                min_dist = i

        average_voters = int (total_voters/len(self.census))

        if self.census[min_dist].total_voters() < (average_voters * .90):
            return min_dist

        match self.heuristic:
            case "Compact":
                return min_dist
            case "Republican":
                sorted_districts = sorted(districts, key=lambda x : self.cpvi_sort(x, 'D', 2))
                return sorted_districts[0][0]
            case "Democrat":
                sorted_districts = sorted(districts, key=lambda x : self.cpvi_sort(x, 'R', 2))
                return sorted_districts[0][0]

        return min_dist
    
    def update(self):
        if len(self.unassigned_precincts) > 0:
            self.grab_neighboring_precinct(self.current_district)
            self.current_district += 1
            if self.current_district == self.district_count:
                self.current_district = 0
        else:
            min_district = self.select_district()
            adjacent_precincts = self.find_adjacent_precincts(min_district)
            choice = self.choose_precinct(adjacent_precincts, min_district)

            self.districts[self.precincts[choice].district].remove(choice)
            self.districts[min_district].append(choice)
            self.census[self.precincts[choice].district].remove_precinct(self.precincts[choice])
            self.update_district(choice, min_district)
    
    def generate_district_counts(self):
        ret_val = ""
        for count in range(len(self.census)):
            rep = self.census[count].rep
            dem = self.census[count].dem
            ret_val += f"{count+1}:  {self.census[count].total_voters():,d} - {self.generate_cpvi(rep, dem)}\n"
        if len(self.unassigned_precincts) > 0:
            ret_val += f"{len(self.unassigned_precincts)} left\n"
        return ret_val
    
    def generate_cpvi(self, rep, dem):
        ret_val = ""
        tot = rep + dem
        perc = rep/tot - .5
        if perc < 0:
            ch = 'D'
            perc = abs(perc)
        else:
            ch = 'R'
        perc = int(perc * 100)
        ret_val = f"{ch}+{perc}"
        return ret_val
    
    def generate_district_controls(self):
        ret_val = ""
        counts = {}
        labels = ["Democrat", "Independent", "Republican"]
        for label in labels:
            counts[label] = 0
        
        for i in range(len(self.census)):
            counts[self.census[i].district_party()] += 1
        
        for label in labels:
            ret_val += f"{label}: {counts[label]}\n"
        
        return ret_val

    def sort_precincts(self, adjacent_precincts, district_centroid, func, mag1, mag2):
        precincts = [(obj, func(obj, self),
                        math.sqrt((district_centroid[0] - self.precincts[obj].boundaries.centroid[0])**2
                                + (district_centroid[1] - self.precincts[obj].boundaries.centroid[1])**2))
                                for obj in adjacent_precincts]
        precincts_sorted = sorted(precincts, key=lambda x: (mag1 * x[1], mag2 * x[2]))
        return precincts_sorted
    
    def choose_precinct(self, adjacent_precincts, district_number):
        district_centroid = self.centroids[district_number]

        def total_voters_weight(obj, self):
            return self.census[self.precincts[obj].district].total_voters()

        def republican_weight(obj, self):
            return self.census[self.precincts[obj].district].total_rep()

        def democrat_weight(obj, self):
            return self.census[self.precincts[obj].district].total_dem()

        def independent_weight(obj, self):
            return self.census[self.precincts[obj].district].total_other()

        rep = self.census[district_number].rep
        dem = self.census[district_number].dem
        tot = rep + dem
        perc = rep/tot - .5
        if perc < 0:
            ch = 'D'
            perc = abs(perc)
        else:
            ch = 'R'
        perc = int(perc * 100)

        match self.heuristic:
            case "Compact":
                precincts_sorted = self.sort_precincts(adjacent_precincts, district_centroid, total_voters_weight, -1, 1)

                #choice = random.choice(precincts[:5])
                choice = precincts_sorted[0]
                return choice[0]
            case "Republican":
                if (ch == 'D' and perc > 2) or (ch == 'R' and perc > 3):
                    func = democrat_weight
                else:
                    func = republican_weight
                precincts_sorted = self.sort_precincts(adjacent_precincts, district_centroid, func, -1, 1)
                choice = precincts_sorted[0]
                return choice[0]
            case "Competative":
                return random.choice(adjacent_precincts) #NYI
            case "Democrat":
                if (ch == 'R' and perc > 2) or (ch == 'D' and perc > 3):
                    func = republican_weight
                else:
                    func = democrat_weight
                precincts_sorted = self.sort_precincts(adjacent_precincts, district_centroid, func, -1, 1)
                choice = precincts_sorted[0]
                return choice[0]
        return random.choice(adjacent_precincts)
    
    def set_heuristic(self, value):
        self.heuristic = value

    def draw(self, canvas):
        for ct in self.centroids:
            cr = Circle(ct[0], ct[1], 5, "black")
            cr.draw(canvas)

def main():
    print("In main")
    print(list(Color)[0].value)
    #for color in Color:
    #    print(color.value)

if __name__ == "__main__":
    main()