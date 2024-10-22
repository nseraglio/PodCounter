from fisheye_correction import run_fisheye_correction
from crop_background import run_crop_background
from qr_renamer import run_rename_images
from pods_counting import run_count_pods
from summary_table import generate_summary_table

def run_all(folder_path, fisheye):
    if fisheye:
        run_fisheye_correction(folder_path)
    run_crop_background(folder_path)
    run_rename_images(folder_path)
    run_count_pods(folder_path)
    generate_summary_table(folder_path)

folder_path = 'yield_components'
run_all(folder_path, fisheye=True)