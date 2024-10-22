import csv
from collections import defaultdict
import os

def generate_summary_table(folder_path):
    # Construct the paths for the CSV file and the output text file
    csv_file = os.path.join(folder_path, 'counted', 'pods.csv')
    output_file = os.path.join(folder_path, 'counted', 'summary_table.txt')

    # Read the CSV file
    data = defaultdict(list)
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            photo_name = row['Photo Name']
            pod_size = float(row['Pod Size (cm)'])
            data[photo_name].append(pod_size)

    # Calculate the number of pods and average pod length for each plot
    summary = []
    for photo_name, pod_sizes in data.items():
        num_pods = len(pod_sizes)
        avg_pod_length = sum(pod_sizes) / num_pods
        summary.append((photo_name, num_pods, avg_pod_length))

    # Write the summary to a text file
    with open(output_file, mode='w') as file:
        file.write(f"{'Plot':<20} {'Number of Pods':<15} {'Average Pod Length (cm)':<25}\n")
        file.write("="*60 + "\n")
        for photo_name, num_pods, avg_pod_length in summary:
            file.write(f"{photo_name:<20} {num_pods:<15} {avg_pod_length:<25.2f}\n")

# Example usage
#folder_path = 'yield_components'
#generate_summary_table(folder_path)