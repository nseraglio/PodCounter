import cv2
import os
import glob
from tqdm import tqdm

def decode_qr_code(img):
    # Initialize the QR code detector
    detector = cv2.QRCodeDetector()
    
    # Try to detect and decode the QR code
    data, _, _ = detector.detectAndDecode(img)
    if data:
        return data
    
    # Try to decode the QR code at different scales
    for scale in [0.5, 1.5, 2.5]:
        resized_img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        data, _, _ = detector.detectAndDecode(resized_img)
        if data:
            return data
    
    # Try to decode the QR code with contrast and brightness adjustments
    for contrast in [0.5, 1.0, 1.5]:
        for brightness in [-50, 0, 50]:
            adjusted_img = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
            data, _, _ = detector.detectAndDecode(adjusted_img)
            if data:
                return data
    
    # Try to decode the QR code at different angles
    for angle in [0, 90, 180, 270]:
        rotated_img = cv2.rotate(img, angle)
        data, _, _ = detector.detectAndDecode(rotated_img)
        if data:
            return data
    
    return None

def run_rename_images(folder_path):
    # Create a dictionary to store QR code counts
    qr_code_counts = {}

    # Find all images in the folder
    images = glob.glob(os.path.join(folder_path, '*.jp*g'))

    for img_path in tqdm(images, desc="Renaming images"):
        img = cv2.imread(img_path)
        qr_code = decode_qr_code(img)
        
        if qr_code:
            # Increment the count for this QR code
            if qr_code in qr_code_counts:
                qr_code_counts[qr_code] += 1
            else:
                qr_code_counts[qr_code] = 1
            
            # Create new file name
            new_file_name = f"{qr_code}_{qr_code_counts[qr_code]}.jpg"
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # Rename the file
            os.rename(img_path, new_file_path)

# Example usage
#folder_path = 'yield_components'
#run_rename_images(folder_path)