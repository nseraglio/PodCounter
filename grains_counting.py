import cv2
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

def detect_and_count_grains(directory):
    # Initialize a list to store results
    results = []

    # Create output folder if it doesn't exist
    output_folder = os.path.join(directory, "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Convert to HSV and filter by the Hue channel
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hue_channel = hsv[:, :, 0]
            _, hue_mask = cv2.threshold(hue_channel, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            hue_filtered_grains = cv2.bitwise_and(image_rgb, image_rgb, mask=hue_mask)

            # Convert the result to grayscale
            hue_filtered_gray = cv2.cvtColor(hue_filtered_grains, cv2.COLOR_RGB2GRAY)

            # Apply CLAHE for contrast enhancement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            clahe_filtered = clahe.apply(hue_filtered_gray)

            # Use morphological operations to separate touching grains
            kernel = np.ones((3, 3), np.uint8)
            morphed_clahe = cv2.morphologyEx(clahe_filtered, cv2.MORPH_CLOSE, kernel, iterations=2)

            # Apply Hough Circle Transform to detect grains
            hough_circle_image = hue_filtered_grains.copy()
            circles = cv2.HoughCircles(
                morphed_clahe, 
                cv2.HOUGH_GRADIENT, 
                dp=1, 
                minDist=18,       # Minimum distance between detected circles
                param1=60,        # Edge detection sensitivity
                param2=10,        # Circle detection sensitivity
                minRadius=6,      # Minimum radius of grains
                maxRadius=12      # Maximum radius of grains
            )

            # Count detected grains and draw circles
            grain_count = 0
            if circles is not None:
                circles = np.uint16(np.around(circles))
                grain_count = len(circles[0, :])  # Count the grains
                for circle in circles[0, :]:
                    center = (circle[0], circle[1])
                    radius = circle[2]
                    cv2.circle(hough_circle_image, center, radius, (255, 0, 0), 2)  # Draw circle in red
                    cv2.circle(hough_circle_image, center, 2, (0, 255, 0), 3)       # Mark center in green

            # Save the output image with detected grains
            output_image_path = os.path.join(output_folder, f"detected_{filename}")
            output_image_bgr = cv2.cvtColor(hough_circle_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_image_path, output_image_bgr)

            # Append results for CSV
            results.append({"Image Name": filename, "Grain Count": grain_count})

    # Save results to CSV
    csv_path = os.path.join(directory, "grain_counts.csv")
    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {csv_path}")

# Example usage:
# detect_and_count_grains("path/to/your/folder")
