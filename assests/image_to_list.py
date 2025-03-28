import cv2
import numpy as np
import json
import os

class CountyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, County):
            return obj.__dict__
        return super().default(obj)

class County:
    def __init__(self, name, rep, dem, oth):
        self.county = name
        self.precincts = []
        self.rep = rep
        self.dem = dem
        self.oth = oth

def image_to_json(image_path):
    printit = image_path == './sliced images/greenlee.png'
    # Load the PNG image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to binary (necessary for contour detection)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to store points for each polygon
    polygons = []

    # Loop through the contours and extract polygon points
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.001 * cv2.arcLength(contour, True)  # Adjust epsilon for precision
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Convert points to a list of tuples
        polygon_points = [(point[0][0], point[0][1]) for point in approx]
        polygons.append(polygon_points)

    # Simplify points into plain integers
    simplified_polygons = [
        [(int(x), int(y)) for x, y in polygon] for polygon in polygons
    ]
    """
    # Define the canvas size (width and height) - Adjust to fit your polygons
    canvas_size = (1500, 1500)  # Example size, adjust based on your data

    # Loop through each polygon and create a separate file
    for idx, polygon in enumerate(polygons):
        # Create a blank canvas
        image = np.zeros(canvas_size, dtype=np.uint8)
        
        # Convert points to a NumPy array
        points = np.array(polygon, dtype=np.int32)
        points = points.reshape((-1, 1, 2))
        
        # Draw the polygon on the image (filled with white color)
        cv2.fillPoly(image, [points], 255)
        
        # Save the image as a separate file
        output_path = f"polygon_{idx + 1}.png"
        cv2.imwrite(output_path, image)
        print(f"Saved: {output_path}")
    """
    precincts = []
    flattened_polygons = [point for sublist in simplified_polygons for point in sublist]
    max_x = max(pt[0] for pt in flattened_polygons)
    max_y = max(pt[1] for pt in flattened_polygons)
    #print(image_path, max_x, max_y)
    for i, boundary in enumerate(simplified_polygons, start=1):
        if printit:
            print(i)
        # Call scale_points to adjust the boundary points
        scaled_boundary = scale_points(boundary, width=600, height=700, max_x=947, max_y=1240, min_x=53, min_y=174, printit=printit and i in (3,4,6,7))
        precinct = {
            "id": i,
            "boundary": [{"x": int(x), "y": int(y)} for x, y in scaled_boundary]
        }
        precincts.append(precinct)

    output = {"precincts": precincts}
    return output

def scale_points(points, width, height, max_x, max_y, min_x, min_y, printit):
    gap = 1.5
    expanded_points = []

    center_x = 0
    center_y = 0
    for x, y in points:
        center_x += x
        center_y += y
    center_x /= len(points)
    center_y /= len(points)
    
    for x, y in points:
        # Scale the points
        scaled_x = ((x - min_x) / max_x) * width
        scaled_y = ((y - min_y) / max_y) * height

        # Adjust for adjacency (expand flush with neighbors)
        adjustment_x = -gap if x < center_x else gap
        adjustment_y = -gap if y < center_y else gap
        adjusted_x = scaled_x + adjustment_x
        adjusted_y = scaled_y + adjustment_y

        expanded_points.append((adjusted_x, adjusted_y))
        if printit:
            print(x, y, int(center_x), int(center_y), int(scaled_x), int(scaled_y), adjustment_x, adjustment_y, int(adjusted_x), int(adjusted_y))

    return expanded_points

image_root = "./sliced images/"
voters = {
    "apache": {"rep": 5824, "dem": 18016, "oth": 8160},
    "cochise": {"rep": 37474, "dem": 23206, "oth": 21320},
    "coconino": {"rep": 24140, "dem": 35020, "oth": 25840},
    "gila": {"rep": 13188, "dem": 7252, "oth": 7560},
    "graham": {"rep": 9054, "dem": 3906, "oth": 5040},
    "greenlee": {"rep": 1910, "dem": 1605, "oth": 1485},
    "la_paz": {"rep": 4626, "dem": 1827, "oth": 2547},
    "maricopa": {"rep": 862500, "dem": 780000, "oth": 857500},
    "mojave": {"rep": 61380, "dem": 18920, "oth": 29700},
    "navajo": {"rep": 21285, "dem": 18205, "oth": 15510},
    "pima": {"rep": 176400, "dem": 238800, "oth": 184800},
    "pinal": {"rep": 85000, "dem": 55000, "oth": 60000},
    "santa_cruz": {"rep": 5075, "dem": 13175, "oth": 6750},
    "yavapai": {"rep": 71680, "dem": 30520, "oth": 37800},
    "yuma": {"rep": 34560, "dem": 30240, "oth": 25200}
}
counties = []
for filename in os.listdir(image_root):
    if filename.endswith(".png"):
        name_without_extension, extension = os.path.splitext(filename)
        fullname = os.path.join(image_root, filename)
        if os.path.isfile(fullname):
            county = County(name_without_extension,
                            voters[name_without_extension]["rep"],
                            voters[name_without_extension]["dem"],
                            voters[name_without_extension]["oth"])
            county.precincts = image_to_json(fullname)["precincts"]
            counties.append(county)
json_output = {
    "Name": "Arizona",
    "counties": counties,
    "districts": 8
}
print(json.dumps(json_output, cls=CountyEncoder, indent=4))
