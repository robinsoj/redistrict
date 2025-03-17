import cv2
import numpy as np

# Load the PNG image
image_path = "arizona-county-map.png"  # Replace with your image path
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
