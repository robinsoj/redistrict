import cv2
import numpy as np
import json
import os

def image_to_json(image_path):
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
    for i, boundary in enumerate(simplified_polygons, start=1):
        precinct = {
            "id": i,
            "boundary": [{"x": point[0], "y": point[1]} for point in boundary]
        }
        precincts.append(precinct)

    output = {"precincts": precincts}
    return output

def scale_points(points, width, height, max_x, max_y):
    scaled_points = []
    for x, y in points:
        scaled_x = (x/max_x) * canvas_width
        scaled_y = (y/max_y) * canvas_height
        scaled_points.append((scaled_x, scaled_y))
    return scaled_points

image_root = "./sliced images/"
for filename in os.listdir(image_root):
    if filename.endswith(".png"):
        fullname = os.path.join(image_root, filename)
        if os.path.isfile(fullname):
            print(fullname)
image_path = "./sliced images/greenlee.png"  # Replace with your image path
print(json.dumps(image_to_json(image_path), indent=4))
