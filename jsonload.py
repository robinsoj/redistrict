import json
import queue
import graphic_primatives as gp
from precinct import *

def openJson(stateFile):
    with open(stateFile, 'r') as file:
        data = json.load(file)
        #for county in data["counties"]:
        #    print(county["county"])
        #    for pt in county["boundary"]:
        #        print(" ", pt["x"], ", ", pt["y"])
        #print(data["districts"])
    return data

def createCountyPolygons(countyJson):
    print("Processing:", countyJson["county"])
    ret_map = {}
    precinctCount = len(countyJson["precincts"])
    rep = round(countyJson["rep"]/precinctCount)
    dem = round(countyJson["dem"]/precinctCount)
    oth = round(countyJson["oth"]/precinctCount)
    for precinct in countyJson["precincts"]:
        points = []
        for i in precinct["boundary"]:
            point = gp.Point(i["x"]+10, i["y"]+10)
            points.append(point)
        pg = gp.Polygon("grey", points)
        precinctItem = Precinct(pg, rep, dem, oth, countyJson["county"] + str(precinct["id"]))
        ret_map[precinctItem.name] = precinctItem
    return ret_map

def polygon_centroid(vertices):
    """
    Calculate the centroid of a polygon given a list of (x, y) coordinates.
    
    Args:
        vertices: List of tuples [(x1, y1), (x2, y2), ..., (xn, yn)] representing
                 the vertices of the polygon in order (clockwise or counterclockwise).
                 The first and last vertex should be the same to close the polygon.
    
    Returns:
        Tuple (cx, cy) representing the x, y coordinates of the centroid.
        Returns None if the area is zero (invalid polygon).
    """
    # Ensure the polygon is closed (first vertex = last vertex)
    if vertices[0] != vertices[-1]:
        vertices = vertices + [vertices[0]]
    
    n = len(vertices)
    if n < 3:  # Need at least 3 vertices to form a polygon
        return None
    
    # Initialize variables for area and centroid
    signed_area = 0.0
    cx = 0.0
    cy = 0.0
    
    # Shoelace formula to calculate area and centroid
    for i in range(n - 1):
        x0, y0 = vertices[i]
        x1, y1 = vertices[i + 1]
        
        # Calculate cross product for area
        cross = (x0 * y1) - (x1 * y0)
        signed_area += cross
        
        # Accumulate centroid contributions
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    
    # Finalize area (divide by 2)
    signed_area *= 0.5
    
    # Handle case where area is zero (degenerate polygon)
    if abs(signed_area) < 1e-10:
        return None
    
    # Finalize centroid coordinates (divide by 6 * area)
    cx = cx / (6.0 * signed_area)
    cy = cy / (6.0 * signed_area)
    
    return (cx, cy)

