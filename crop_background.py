import cv2
import os
import glob
import numpy as np
from tqdm import tqdm

def run_crop_background(folder_path):
    # Find all images in the folder
    images = glob.glob(os.path.join(folder_path, '*.jpg'))

    for img_path in tqdm(images, desc="Cropping background"):
        img = cv2.imread(img_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define range for the blue color in HSV
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = np.int32(box)  # Corrected to int32

            # Apply perspective transformation
            width = int(rect[1][0])
            height = int(rect[1][1])
            src_pts = box.astype("float32")
            dst_pts = np.array([[0, height-1],
                                [0, 0],
                                [width-1, 0],
                                [width-1, height-1]], dtype="float32")
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(img, M, (width, height))

            # Ensure the image is in landscape mode
            if height > width:
                warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
                height, width = width, height

            # Remove 5% from each side
            crop_percent = 0.03
            top = int(height * crop_percent)
            bottom = int(height * (1 - crop_percent))
            left = int(width * crop_percent)
            right = int(width * (1 - crop_percent))
            cropped_img = warped[top:bottom, left:right]

            # Save cropped image, replacing the original
            cv2.imwrite(img_path, cropped_img)

# Example usage
#folder_path = 'yield_components'
#run_crop_background(folder_path)