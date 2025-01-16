import shutil
from fisheye_correction import run_fisheye_correction
from crop_background import run_crop_background
from qr_renamer import run_rename_images
from pods_counting import run_count_pods
from summary_table import generate_summary_table

def run_pods(folder_path, counting_path, label_area_cm2):
    # Copy the contents of the original folder to a new counting folder
    shutil.copytree(folder_path, counting_path, dirs_exist_ok=True)
    
    # Correct fisheye distortion in the images
    run_fisheye_correction(counting_path)
    
    # Crop the background from the images to focus on the pods
    run_crop_background(counting_path)
    
    # Rename the images based on the QR codes found
    run_rename_images(counting_path)
    
    # Count the pods in the images and save the results to a CSV file
    run_count_pods(counting_path, label_area_cm2)
    
    # Generate a summary table with the number of pods and the average pod length
    generate_summary_table(counting_path)

# Path to the original folder containing the pod images
folder_path = 'test/pods'

# Path to the folder where the processed images will be saved
counting_path = 'test/pods_counting'

# Area of the white label in cm² (passed as a string, will be converted to float in the function)
label_area_cm2 = '51.6'

# Execute the complete pod counting process
run_pods(folder_path, counting_path, label_area_cm2)