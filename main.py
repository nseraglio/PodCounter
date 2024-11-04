import shutil
from fisheye_correction import run_fisheye_correction
from crop_background import run_crop_background
from qr_renamer import run_rename_images
from pods_counting import run_count_pods
from grains_counting import detect_and_count_grains
from summary_table import generate_summary_table

def run_pods(folder_path, fisheye):
    pods_counting_path = 'pods_counting'
    shutil.copytree(folder_path, pods_counting_path, dirs_exist_ok=True)
    
    if fisheye:
        run_fisheye_correction(pods_counting_path)
    run_crop_background(pods_counting_path)
    run_rename_images(pods_counting_path)
    run_count_pods(pods_counting_path)
    generate_summary_table(pods_counting_path)

def run_grains(folder_path, fisheye):
    grain_counting_path = 'grain_counting'
    shutil.copytree(folder_path, grain_counting_path, dirs_exist_ok=True)
    
    if fisheye:
        run_fisheye_correction(grain_counting_path)
    run_rename_images(grain_counting_path)
    run_crop_background(grain_counting_path)
    detect_and_count_grains(grain_counting_path)
    #generate_summary_table(grain_counting_path)

folder_path = 'grains'
run_grains(folder_path, fisheye=True)
