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
   Detects and counts pods in the images, calculates their lengths using a white label as a size reference (can be the QR code label), and saves each individual length in the `pods.csv` file.
   In the processed images, the pods are outlined in red, while the white labels are outlined in green to facilitate visual verification. Each pod is assigned a unique identifier (ID) at its centroid, enabling the individual identification of each pod in the `pods.csv` file.

6. **Summary Generation**  
   Creates a summary table with the total number of pods and the average pod length for each processed image, and save in the `summary_table.txt` file.

## How to Use

### Taking Pictures

To ensure accurate pod counting and measurement, please follow these guidelines when capturing images:

#### 1. **Use a Matte Blue Board**
- Use a flat, matte blue board as the background.
- This color provides optimal contrast for pod detection.

#### 2. **Include a White Reference Object**
- Place a white object with a known area beneath the blue board. This polygon should:
  - Be the largest white object in the image.
  - Optionally can be a label contain a QR code to help identify the sample.

#### 3. **Position the Pods Properly**
- Spread the pods with sufficient space between them.  
- **Important:** Pods that touch or are too close to each other will be detected and counted as a single pod.  
- Avoid stacking or overlapping the pods.

#### 4. **Keep the Board Clean**
- Do not place any objects on the blue board other than the pods and the white reference polygon.
- Remove any debris, shadows, or other obstructions that could interfere with image processing.

#### 5. **Reference Example Image**
- For guidance on proper setup, refer to the example image located at:  
  `example/pods_counting/counted/314_MB-DOP_1.jpg`.
- This example shows:
  - How the pods and the white reference object should be positioned.
  - What happens when pods touch (e.g., pods 4, 22, and 55 in the example are incorrectly counted as a single pod).

By following these guidelines, you ensure that the images are optimized for processing by **PodCounter**.

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


## Step-by-Step Guide for Beginners

If you're new to Python, follow these instructions to set up and use PodCounter:

### 1. Install Python
1. Download Python from the official website: [python.org](https://www.python.org).
2. During installation, make sure to:
   - Check the box that says "Add Python to PATH" before clicking "Install Now."
   - Complete the installation by following the prompts.

### 2. Install a Code Editor (Optional)
   - For a better experience, download and install a code editor like [Visual Studio Code](https://code.visualstudio.com).

### 3. Download PodCounter
1. Download the PodCounter project from the GitHub repository:
   - Click "Code" on the repository page and select "Download ZIP". Extract the ZIP file to a folder of your choice.

### 4. Install Required Python Libraries
1. Open a terminal or command prompt.
   - On Windows: Press Win + R, type cmd, and hit Enter.
   - On macOS/Linux: Open the Terminal application.
2. Navigate to the project folder where the requirements.txt file is located:
   ```bash
   cd path/to/PodCounter
3. Install the required libraries:
   ```bash 
   pip install -r requirements.txt

### 5. Prepare Your Images
1. Organize the images you want to process in a folder (e.g., input_images).
2. Ensure that the images follow the guidelines in the Taking Pictures section.

### 6. Configure the Script
1. Open the `main.py` file in a text editor or code editor.
2. Set the following variables:
   - folder_path: The path to your input folder containing the images.
   - counting_path: The path where processed images and reports will be saved.
   - label_area_cm2: The area (in square centimeters) of the white reference polygon beneath the blue board.

### 7. Run PodCounter
1. In the terminal or command prompt, navigate to the project folder:
   ```bash 
   cd path/to/PodCounter
3. Run the script:
   ```bash 
   python main.py

### 8. Check the Results
1. Processed images and reports will be saved in the counting_path directory:
   - Background Cropped Images: Found directly in the directory.
   - Images with Pods Highlighted: Saved in the counting_path/counted folder.
   - Pod Sizes: Saved in the pods.csv file.
   - Summary Report: Saved in the summary_table.txt file.
