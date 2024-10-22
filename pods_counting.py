import cv2
import os
import glob
import numpy as np
import csv
from matplotlib import pyplot as plt
from tqdm import tqdm

def detect_white_label(image):
    # Convert the image from BGR to HSV (Hue, Saturation, Value) color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper limits for the white color in HSV
    lower_white = np.array([0, 0, 200])   # Low Hue, Low Saturation, High Value
    upper_white = np.array([180, 50, 255]) # Range to capture white

    # Create a mask to detect white areas (label)
    mask = cv2.inRange(hsv_image, lower_white, upper_white)

    # Apply morphological operations to remove small noise and fill small holes
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Assuming the largest white area is the label
        label_contour = max(contours, key=cv2.contourArea)
        return label_contour
    return None

def run_count_pods(folder_path):
    output_folder = os.path.join(folder_path, 'counted')
    csv_file = os.path.join(output_folder, 'pods.csv')
    # Create folder to save processed images
    os.makedirs(output_folder, exist_ok=True)

    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Photo Name', 'Pod Number', 'Pod Size (cm)'])

        # Find all images in the folder
        images = glob.glob(os.path.join(folder_path, '*.jp*g'))

        for img_path in tqdm(images, desc="Counting pods"):
            # Read the image
            image = cv2.imread(img_path)

            # Detect the white label
            label_contour = detect_white_label(image)
            if label_contour is not None:
                # Convert the label contour to a numpy array if it is not already
                label_contour = np.array(label_contour, dtype=np.float32)

                # Create a black mask the size of the image to apply dilation to the contour
                mask = np.zeros_like(image[:, :, 0])

                # Draw the label contour on the mask
                cv2.drawContours(mask, [label_contour.astype(int)], -1, 255, -1)

                # Create a 5-pixel buffer around the mask using dilation
                kernel = np.ones((3, 3), np.uint8)  # 3x3 kernel for dilation
                dilated_label_mask = cv2.dilate(mask, kernel, iterations=5)  # 5px buffer around

                # Exclude the dilated label area from the pod mask
                dilated_label_mask_inv = cv2.bitwise_not(dilated_label_mask)

                # Calculate the image scale (cm/pixel)
                x, y, w, h = cv2.boundingRect(label_contour)
                label_width_cm = 4 * 2.54  # 4 inches in cm
                label_height_cm = 2 * 2.54  # 2 inches in cm
                scale_x = label_width_cm / w
                scale_y = label_height_cm / h
                scale = (scale_x + scale_y) / 2  # Average of x and y scales

                # Define the minimum area in pixels (1 cm²)
                min_area_cm2 = 0.5
                min_area_pixels = min_area_cm2 / (scale ** 2)

                # Convert the image from BGR to HSV (Hue, Saturation, Value) color space
                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                # Define the lower and upper limits for the blue color in HSV
                lower_blue = np.array([100, 50, 50])
                upper_blue = np.array([140, 255, 255])

                # Create a mask to detect blue areas
                mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

                # Invert the mask to get the pods (non-blue areas)
                pods_mask = cv2.bitwise_not(mask)

                # Apply Gaussian smoothing to reduce noise
                pods_mask = cv2.GaussianBlur(pods_mask, (5, 5), 0)

                # Apply morphological operations to remove small noise and fill small holes
                kernel = np.ones((5, 5), np.uint8)
                pods_mask = cv2.morphologyEx(pods_mask, cv2.MORPH_OPEN, kernel)
                pods_mask = cv2.morphologyEx(pods_mask, cv2.MORPH_CLOSE, kernel)

                # Exclude the dilated label area (with buffer) from the pod mask
                pods_mask = cv2.bitwise_and(pods_mask, pods_mask, mask=dilated_label_mask_inv)

                # Find contours of the pods
                contours, _ = cv2.findContours(pods_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Draw contours and number the pods on the original image
                pod_count = 1
                for i, contour in enumerate(contours):
                    # Calculate the contour area
                    area = cv2.contourArea(contour)
                    if area < min_area_pixels:
                        continue  # Ignore pods smaller than the minimum area

                    # Draw contour in red
                    cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

                    # Find the center of the contour to place the number
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                    else:
                        cX, cY = 0, 0
                    # Place the pod number
                    cv2.putText(image, str(pod_count), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

                    # Calculate the pod length (largest dimension of the contour)
                    rect = cv2.minAreaRect(contour)
                    length = max(rect[1]) * scale  # Convert to cm

                    # Remove the file extension and the last suffix
                    photo_name = os.path.basename(img_path)
                    photo_name = os.path.splitext(photo_name)[0]
                    if '_' in photo_name:
                        photo_name = '_'.join(photo_name.split('_')[:-1])

                    # Write the data to the CSV file
                    writer.writerow([photo_name, pod_count, length])
                    pod_count += 1

                # Draw the label contour in green on the final image (do not use blue mask)
                cv2.drawContours(image, [label_contour.astype(int)], -1, (0, 255, 0), 2)  # Green contour

                # Save processed image
                output_path = os.path.join(output_folder, os.path.basename(img_path))
                cv2.imwrite(output_path, image)

# Example usage
#folder_path = 'yield_components'
#run_count_pods(folder_path)