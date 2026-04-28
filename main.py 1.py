import cv2
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

input_folder = os.path.join(base_dir, "inputs")
output_folder = os.path.join(base_dir, "output_images")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg")]

print("Images found:", image_files)

for file_name in image_files:

    img_path = os.path.join(input_folder, file_name)
    save_path = os.path.join(output_folder, "result_" + file_name)

    image = cv2.imread(img_path)

    if image is None:
        print("Error loading:", file_name)
        continue

    result = image.copy()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([5, 50, 50])
    upper = np.array([50, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 3000:
            continue

        peri = cv2.arcLength(cnt, True)
        if peri == 0:
            continue

        circ = (4 * np.pi * area) / (peri * peri)

        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        corners = len(approx)

        x, y, w, h = cv2.boundingRect(cnt)
        ratio = w / float(h)

        label = "Unknown"
        color = (255, 255, 0)

        if circ > 0.70 and corners > 5:
            if circ > 0.82:
                label = "Intact Biscuit (Circle)"
                color = (0, 255, 0)
            else:
                label = "Broken Biscuit (Circle)"
                color = (0, 0, 255)

        elif 3 <= corners <= 6:
            if 0.8 < ratio < 1.2:
                if corners == 4:
                    label = "Intact Biscuit (Square)"
                    color = (0, 255, 0)
                else:
                    label = "Broken Biscuit (Square)"
                    color = (0, 0, 255)
            else:
                label = "Broken Biscuit (Square)"
                color = (0, 0, 255)

        else:
            label = "Broken Biscuit"
            color = (0, 0, 255)

        cv2.drawContours(result, [cnt], -1, color, 2)
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)

        cv2.putText(result, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imwrite(save_path, result)

    print("Processed:", file_name)

print("Done processing all images")
