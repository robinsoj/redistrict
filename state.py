from graphic_primatives import *
from enum import Enum
import random

class Color(Enum):
    BLUE = "#0000FF"
    BROWN = "#A52A2A"
    FOREST_GREEN = "#228B22"
    GOLD = "#FFD700"
    ORANGE = "#FFA500"
    PINK = "#FFC0CB"
    RED = "#FF0000"
    ALICE_BLUE = "#F0F8FF"
    ANTIQUE_WHITE = "#FAEBD7"
    AQUA = "#00FFFF"
    AQUAMARINE = "#7FFFD4"
    AZURE = "#F0FFFF"
    BEIGE = "#F5F5DC"
    BISQUE = "#FFE4C4"
    BLANCHED_ALMOND = "#FFEBCD"
    BLUE_VIOLET = "#8A2BE2"
    BURLY_WOOD = "#DEB887"
    CADET_BLUE = "#5F9EA0"
    CHARTREUSE = "#7FFF00"
    CHOCOLATE = "#D2691E"
    CORAL = "#FF7F50"
    CORNFLOWER_BLUE = "#6495ED"
    CORNSILK = "#FFF8DC"
    CRIMSON = "#DC143C"
    CYAN = "#00FFFF"
    DARK_BLUE = "#00008B"
    DARK_CYAN = "#008B8B"
    DARK_GOLDENROD = "#B8860B"
    DARK_GREEN = "#006400"
    DARK_KHAKI = "#BDB76B"
    DARK_MAGENTA = "#8B008B"
    DARK_OLIVE_GREEN = "#556B2F"
    DARK_ORANGE = "#FF8C00"
    DARK_ORCHID = "#9932CC"
    DARK_RED = "#8B0000"
    DARK_SALMON = "#E9967A"
    DARK_SEA_GREEN = "#8FBC8F"
    DARK_SLATE_BLUE = "#483D8B"
    DARK_TURQUOISE = "#00CED1"
    DARK_VIOLET = "#9400D3"
    DEEP_PINK = "#FF1493"
    DEEP_SKY_BLUE = "#00BFFF"
    DODGER_BLUE = "#1E90FF"
    FIREBRICK = "#B22222"
    FLORAL_WHITE = "#FFFAF0"
    FUCHSIA = "#FF00FF"
    GAINSBORO = "#DCDCDC"
    GHOST_WHITE = "#F8F8FF"
    GOLDENROD = "#DAA520"
    HONEYDEW = "#F0FFF0"
    HOT_PINK = "#FF69B4"
    INDIAN_RED = "#CD5C5C"
    INDIGO = "#4B0082"
    IVORY = "#FFFFF0"
    KHAKI = "#F0E68C"
    LAVENDER = "#E6E6FA"
    LAVENDER_BLUSH = "#FFF0F5"
    LAWN_GREEN = "#7CFC00"
    LEMON_CHIFFON = "#FFFACD"
    LIGHT_BLUE = "#ADD8E6"
    LIGHT_CORAL = "#F08080"
    LIGHT_CYAN = "#E0FFFF"
    LIGHT_GOLDENROD_YELLOW = "#FAFAD2"
    LIGHT_GREEN = "#90EE90"
    LIGHT_PINK = "#FFB6C1"
    LIGHT_SALMON = "#FFA07A"
    LIGHT_SEA_GREEN = "#20B2AA"
    LIGHT_SKY_BLUE = "#87CEFA"
    LIGHT_SLATE_BLUE = "#8470FF"
    LIGHT_STEEL_BLUE = "#B0C4DE"
    LIGHT_YELLOW = "#FFFFE0"
    LIME = "#00FF00"
    LIME_GREEN = "#32CD32"
    LINEN = "#FAF0E6"
    MAGENTA = "#FF00FF"
    MAROON = "#800000"
    MEDIUM_AQUAMARINE = "#66CDAA"
    MEDIUM_BLUE = "#0000CD"
    MEDIUM_ORCHID = "#BA55D3"
    MEDIUM_PURPLE = "#9370DB"
    MEDIUM_SEA_GREEN = "#3CB371"
    MEDIUM_SLATE_BLUE = "#7B68EE"
    MEDIUM_SPRING_GREEN = "#00FA9A"
    MEDIUM_TURQUOISE = "#48D1CC"
    MEDIUM_VIOLET_RED = "#C71585"
    MIDNIGHT_BLUE = "#191970"
    MINT_CREAM = "#F5FFFA"
    MISTY_ROSE = "#FFE4E1"
    MOCCASIN = "#FFE4B5"
    NAVAJO_WHITE = "#FFDEAD"
    NAVY = "#000080"
    OLD_LACE = "#FDF5E6"
    OLIVE = "#808000"
    OLIVE_DRAB = "#6B8E23"
    ORANGE_RED = "#FF4500"
    ORCHID = "#DA70D6"
    PALE_GOLDENROD = "#EEE8AA"
    PALE_GREEN = "#98FB98"
    PALE_TURQUOISE = "#AFEEEE"
    PALE_VIOLET_RED = "#DB7093"
    PAPAYA_WHIP = "#FFEFD5"
    PEACH_PUFF = "#FFDAB9"
    PERU = "#CD853F"
    PLUM = "#DDA0DD"
    POWDER_BLUE = "#B0E0E6"
    PURPLE = "#800080"
    ROSY_BROWN = "#BC8F8F"
    ROYAL_BLUE = "#4169E1"
    SADDLE_BROWN = "#8B4513"
    SALMON = "#FA8072"
    SANDY_BROWN = "#F4A460"

class State:
    def __init__(self, name, districts, presincts):
        self.name = name
        self.districts = []
        self.precints = presincts
        self.district_count = districts
        self.district_colors = []
        for i in range(self.district_count):
            print(i)
    
    def update_district(self, precinct, district_number):
        for pre in self.precincts:
            if precinct.boundaries == pre.boundaries:
                pre.assign_color(list(Color)[district_number].value, district_number)
                return

    def find_border_polygons(self, districtNum):
        def are_polygons_connected(polygon1, polygon2):
            return any(vertex in polygon2 for vertex in polygon1)

        def is_polygon_inside(polygon, other_polygons):
            for other in other_polygons:
                if all(vertex in other for vertex in polygon):
                    return True
            return False

        if districtNum > len(self.districts):
            return

        # Remove completely internal polygons from set1
        set1 = [polygon for polygon in self.districts[districtNum] if not is_polygon_inside(polygon, self.districts[districtNum])]

        border_polygons = []
        for polygon2 in self.precints:
            if polygon2 not in set1:
                for polygon1 in set1:
                    if are_polygons_connected(polygon1, polygon2.boundaries) and polygon2.district == -1:
                        border_polygons.append(polygon2.boundaries)
                        break
        return border_polygons
    
    def seed_initial_district(self):
        for i in range(self.district_count):
            dist_list = []
            while len(dist_list) == 0:
                random_precinct = random.choice(self.precints)
                if random_precinct.district == -1:
                    self.update_district(random_precinct, i)
                    dist_list.append(random_precinct)
                    self.districts.append(dist_list)

    def populate_districts(self):
        curr_district = 0
        total_precincts = 0
        for pre in self.precints:
            if pre.district == -1:
                total_precincts += 1
        
        while total_precincts > 0:


def main():
    print("In main")
    print(list(Color)[0].value)
    #for color in Color:
    #    print(color.value)

if __name__ == "__main__":
    main()