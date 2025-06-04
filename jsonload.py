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

def center_of_mass(points):
    """
    Calculate the center of mass for a list of points, ensuring the result lies within the convex hull.
    Points can be [(x, y)] or [(x, y, mass)].
    If no mass is provided, assumes equal mass for all points.
    
    Args:
        points: List of tuples, either (x, y) or (x, y, mass)
    
    Returns:
        Tuple (x_com, y_com) representing the center of mass coordinates
    """
    if not points:
        return None  # Handle empty list
    
    # Extract coordinates and masses
    total_mass = 0.0
    x_sum = 0.0
    y_sum = 0.0
    coords = []
    
    for point in points:
        if len(point) == 3:  # (x, y, mass)
            x, y, mass = point
        else:  # (x, y), assume mass = 1
            x, y = point
            mass = 1.0
            
        x_sum += x * mass
        y_sum += y * mass
        total_mass += mass
        coords.append([x, y])
    
    if total_mass == 0:
        return None  # Avoid division by zero
    
    x_com = x_sum / total_mass
    y_com = y_sum / total_mass
    
    # If fewer than 3 points, return original COM
    if len(points) < 3:
        return (x_com, y_com)
    
    # Simple convex hull (Graham scan)
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else -1  # Clockwise or counterclockwise
    
    def convex_hull(points):
        if len(points) < 3:
            return points
        
        # Find the bottom-most point
        points = sorted(points, key=lambda p: (p[1], p[0]))
        start = points[0]
        points = points[1:]
        
        # Sort by polar angle with respect to start
        points.sort(key=lambda p: (p[0] - start[0]) / (max(0.0001, ((p[0] - start[0])**2 + (p[1] - start[1])**2)**0.5)))
        
        # Graham scan
        hull = [start]
        for point in points:
            while len(hull) > 1 and orientation(hull[-2], hull[-1], point) <= 0:
                hull.pop()
            hull.append(point)
        return hull
    
    # Compute convex hull
    try:
        hull_points = convex_hull(coords)
    except:
        return (x_com, y_com)  # If hull fails (e.g., collinear points), return original COM
    
    # Check if point is inside convex hull using ray-casting
    def is_point_in_hull(point, hull_points):
        x, y = point
        intersections = 0
        for i in range(len(hull_points)):
            p1 = hull_points[i]
            p2 = hull_points[(i + 1) % len(hull_points)]
            if p1[1] == p2[1]:  # Skip horizontal edges
                continue
            if min(p1[1], p2[1]) < y <= max(p1[1], p2[1]):
                if x <= max(p1[0], p2[0]):
                    x_intersect = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1] + 0.0001)
                    if x <= x_intersect:
                        intersections += 1
        return intersections % 2 == 1
    
    # If center of mass is inside the convex hull, return it
    if is_point_in_hull((x_com, y_com), hull_points):
        return (x_com, y_com)
    
    # Find closest point on or within convex hull
    min_dist = float('inf')
    closest_point = (x_com, y_com)
    
    # Check each vertex of the convex hull
    for vertex in hull_points:
        dist = ((x_com - vertex[0])**2 + (y_com - vertex[1])**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest_point = (vertex[0], vertex[1])
    
    # Check points along edges of the convex hull
    for i in range(len(hull_points)):
        p1 = hull_points[i]
        p2 = hull_points[(i + 1) % len(hull_points)]
        # Parameterize the edge: p(t) = p1 + t*(p2 - p1), t in [0,1]
        for t in [i/100 for i in range(101)]:  # 100 samples
            x = p1[0] + t * (p2[0] - p1[0])
            y = p1[1] + t * (p2[1] - p1[1])
            dist = ((x_com - x)**2 + (y_com - y)**2)**0.5
            if dist < min_dist:
                min_dist = dist
                closest_point = (x, y)
    
    return closest_point