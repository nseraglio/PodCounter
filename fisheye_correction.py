import cv2
import os
import glob
import numpy as np
from tqdm import tqdm

def run_fisheye_correction(folder_path):
    # GoPro Hero 4 Black fisheye distortion correction
    def remove_fisheye_effect(img):
        h, w, _ = img.shape
        focal_length = 0.5 * w
        optical_center = (w / 2, h / 2)
        k1, k2, k3, k4 = -0.15, 0.022, 0, 0
        new_K = np.array([[focal_length, 0, optical_center[0]],
                          [0, focal_length, optical_center[1]],
                          [0, 0, 1]])
        mapx, mapy = cv2.initUndistortRectifyMap(new_K, np.array([k1, k2, k3, k4]), None, new_K, (w, h), 5)
        return cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # Find all images in the folder
    images = glob.glob(os.path.join(folder_path, '*.jp*g'))

    for img_path in tqdm(images, desc="Correcting fisheye distortion"):
        img = cv2.imread(img_path)
        corrected_img = remove_fisheye_effect(img)
        
        # Replace original image with corrected image
        cv2.imwrite(img_path, corrected_img)

# Example usage
#folder_path = 'yield_components'
#run_fisheye_correction(folder_path)