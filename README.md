# PodCounter

PodCounter is an automated image processing tool designed to count pods in captured photos, correct distortions, crop backgrounds, rename images based on QR codes, and generate a report with the total number and average length of pods. It is tailored for accurate and consistent analysis of agricultural research images.

## Requirements
To run this project, you need the following Python libraries:
- `opencv-python`
- `numpy`
- `tqdm`
- `matplotlib`

You can install all dependencies using the `requirements.txt` file:
```bash 
pip install -r requirements.txt
```

## Features
1. **Fisheye Distortion Correction**  
   Corrects distortion in images captured with GoPro Hero 4 cameras.

2. **Background Cropping**  
   Crops the background outside the board area in images. The code is adjusted to work with blue boards.

3. **Image Renaming**  
   Renames images based on detected QR codes.

4. **Pod Counting**  
   Identifies and counts pods in the images and calculates their lengths.

5. **Summary Generation**  
   Creates a summary table with the total number of pods and the average pod length for each processed image.

## How to Use
### Setup
1. Organize the images into an input folder.
2. Set the arguments for the input and output directories:
   - `folder_path`: Path to the folder containing the input images.
   - `counting_path`: Path to save the processed images and summary.

3. Run the main script `main.py`:
```bash 
python main.py
```

### Automated Steps
When running the main script, the following steps are performed:
1. **Fisheye Distortion Correction**: Corrects distortion for all images in the folder.
2. **Background Cropping**: Removes backgrounds and adjusts images to retain only the relevant areas.
3. **QR Code Renaming**: Detects QR codes in the images and renames them accordingly.
4. **Pod Counting**: Counts pods and measures their lengths and save in a `.csv` file.
5. **Summary**: Generates a detailed report in `.txt` format.

### Output
- **Background Cropped Images**: Saved in the `counting_path` directory.
- **Images with Pods Highlighted**: Saved in the `counting_path/counted` directory.
- **Individual Pods Size**: Saved in the `counting_path/counted/pods.csv`.
- **Summary**: Generated at `counting_path/counted/summary_table.txt`.

## Example Usage
```bash
from main import run_pods

folder_path = 'grains'  # Input folder with original images
counting_path = 'pods_counting'  # Output folder for processed results
run_pods(folder_path, counting_path)
```
