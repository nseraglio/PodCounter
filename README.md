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
   Detects and counts pods in the images, calculates their lengths using a white label as a size reference, and saves each individual length in a `.csv` file.

5. **Summary Generation**  
   Creates a summary table with the total number of pods and the average pod length for each processed image, and save in a `.txt` file.

## How to Use
### Setup
1. Organize the images into an input folder.
2. Set the arguments for the input and output directories in `main.py`:
   - `folder_path`: Path to the folder containing the input images.
   - `counting_path`: Path to save the processed images and summary.
   - `label_area_cm2`: Defines the area of the white label in square centimeters.
3. Run the main script `main.py`:
```bash 
python main.py
```

### Output
- **Background Cropped Images**: Saved in the `counting_path` directory.
- **Images with Pods Highlighted**: Saved in the `counting_path/counted` directory.
- **Individual Pods Size**: Saved in the `counting_path/counted/pods.csv`.
- **Summary**: Generated at `counting_path/counted/summary_table.txt`.

