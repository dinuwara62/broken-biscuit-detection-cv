import cv2
import numpy as np
import os

# Get current folder path
base_dir = os.path.dirname(os.path.abspath(__file__))

# Input and output folders
input_folder = os.path.join(base_dir, "inputs")
output_folder = os.path.join(base_dir, "output_images")

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get all image files
image_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]

print("Images found:", image_files)

# Process each image
for file_name in image_files:

    image_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, "result_" + file_name)

    image = cv2.imread(image_path)

    # Check if image is loaded
    if image is None:
        print("Could not read:", file_name)
        continue

    output = image.copy()

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color range for biscuit
    lower = np.array([5, 50, 50])
    upper = np.array([50, 255, 255])

    # Create mask
    mask = cv2.inRange(hsv, lower, upper)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Further cleaning
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    for cnt in contours:

        area = cv2.contourArea(cnt)

        # Ignore small noise
        if area < 3000:
            continue

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue

        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter * perimeter)

        # Approximate shape
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
        vertices = len(approx)

        # Bounding box
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h

        # Classification
        label = "Unknown"
        color = (255, 255, 0)

        # Circle detection
        if circularity > 0.70 and vertices > 5:
            if circularity > 0.82:
                label = "Intact Biscuit (Circle)"
                color = (0, 255, 0)
            else:
                label = "Broken Biscuit (Circle)"
                color = (0, 0, 255)

        # Square detection
        elif 3 <= vertices <= 6:
            if 0.8 < aspect_ratio < 1.2:
                if vertices == 4:
                    label = "Intact Biscuit (Square)"
                    color = (0, 255, 0)
                else:
                    label = "Broken Biscuit (Square)"
                    color = (0, 0, 255)
            else:
                label = "Broken Biscuit (Square)"
                color = (0, 0, 255)

        # Other shapes
        else:
            label = "Broken Biscuit"
            color = (0, 0, 255)

        # Draw contour and box
        cv2.drawContours(output, [cnt], -1, color, 2)
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)

        # Add label
        cv2.putText(output, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Save result
    cv2.imwrite(output_path, output)
    print("Processed:", file_name)

print("All images processed.")