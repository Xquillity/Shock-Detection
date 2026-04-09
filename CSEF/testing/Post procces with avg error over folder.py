import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
import pandas as pd
import os
import re

# === FOLDER SETUP ===
data_folder = "Data/new_data/"  # Folder containing the CSV files
# === SENSOR SETUP ===
# Define known sensor coordinates (x, y) - with additional 5th sensor at (0,6)
x = np.array([0, -6, -2.5, 2.5, 6, 0])  # Sensor x-coordinates
y = np.array([0, 5.5, 11.5, 11.5, 5.5, 6])  # Sensor y-coordinates

def extract_ground_truth_from_filename(filename):
    """Extract ground truth coordinates from filename format x,y.csv"""
    try:
        # Remove .csv extension if present
        base_name = filename.replace('.csv', '')
        
        # Use regex to match x,y pattern with optional suffix (handles negative numbers and multiple files)
        pattern = r'^(-?\d*\.?\d+),(-?\d*\.?\d+)(_.*)?$'
        match = re.match(pattern, base_name)
        
        if match:
            actual_x = float(match.group(1))
            actual_y = float(match.group(2))
            return actual_x, actual_y
        else:
            return None
    except:
        return None

def process_single_file(file_path, actual_x, actual_y, sample_to_read=0):
    """Process a single CSV file and return the error"""
    try:
        # Read the selected sample from CSV
        df = pd.read_csv(file_path, header=None)
        sensor_values = df.iloc[sample_to_read].values  # Get the sensor readings S0-S5

        # Convert to floats, handling empty values and taking all 6 sensors
        z_list = []
        for i, val in enumerate(sensor_values):
            if i >= 6:  # Only take first 6 sensors (S0-S5)
                break
            val_str = str(val).strip()
            if val_str and val_str != 'nan':  # Check if not empty and not NaN
                z_list.append(float(val_str))
            else:
                z_list.append(0.0)  # Default to 0 for empty values

        z = np.array(z_list)  # Convert to numpy array

        # === RBF INTERPOLATION ===
        # Create a meshgrid for interpolation
        grid_x, grid_y = np.mgrid[-10:10:100j, 0:15:100j]

        # Set Gaussian kernel for RBF interpolation
        rbf = RBFInterpolator(np.column_stack((x, y)), z, kernel='gaussian', epsilon=0.2)

        # Perform interpolation on the grid
        points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
        grid_z = rbf(points)
        grid_z = grid_z.reshape(grid_x.shape)

        # Find maximum point coordinates
        max_value = np.max(grid_z)
        max_idx = np.unravel_index(np.argmax(grid_z), grid_z.shape)
        max_x = grid_x[max_idx]
        max_y = grid_y[max_idx]

        # Calculate error using Pythagorean theorem
        error_distance = np.sqrt((max_x - actual_x)**2 + (max_y - actual_y)**2)
        
        return {
            'filename': os.path.basename(file_path),
            'ground_truth': (actual_x, actual_y),
            'predicted': (max_x, max_y),
            'error': error_distance,
            'sensor_values': z
        }
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return None

def main():
    """Main function to process all files and calculate average error"""
    print("=== PROCESSING MULTIPLE DATA FILES FOR AVERAGE ERROR ===")
    print(f"Looking for CSV files in folder: {data_folder}")
    
    # Get all CSV files in the data folder
    all_files = os.listdir(data_folder)
    csv_files = [f for f in all_files if f.endswith('.csv')]
    
    valid_files = []
    results = []
    
    # Process each CSV file
    for filename in csv_files:
        # Extract ground truth from filename
        ground_truth = extract_ground_truth_from_filename(filename)
        
        if ground_truth is None:
            print(f"Skipping {filename} - cannot extract ground truth from filename")
            continue
            
        actual_x, actual_y = ground_truth
        file_path = os.path.join(data_folder, filename)
        
        print(f"\nProcessing: {filename}")
        print(f"Ground Truth: ({actual_x}, {actual_y})")
        
        # Process the file
        result = process_single_file(file_path, actual_x, actual_y)
        
        if result is not None:
            results.append(result)
            valid_files.append(filename)
            
            pred_x, pred_y = result['predicted']
            error = result['error']
            
            print(f"Predicted: ({pred_x:.3f}, {pred_y:.3f})")
            print(f"Error: {error:.3f} inches")
        else:
            print(f"Failed to process {filename}")
    
    # Calculate and display average error
    if results:
        errors = [r['error'] for r in results]
        avg_error = np.mean(errors)
        std_error = np.std(errors)
        min_error = np.min(errors)
        max_error = np.max(errors)
        
        print("\n" + "="*60)
        print("=== FINAL RESULTS ===")
        print(f"Total files processed: {len(results)}")
        print(f"Valid files: {', '.join(valid_files)}")
        print(f"\nERROR STATISTICS:")
        print(f"Average Error: {avg_error:.3f} inches")
        print(f"Standard Deviation: {std_error:.3f} inches")
        print(f"Minimum Error: {min_error:.3f} inches")
        print(f"Maximum Error: {max_error:.3f} inches")
        print("="*60)
        
        # Show detailed breakdown
        print("\nDETAILED BREAKDOWN:")
        for result in results:
            gt_x, gt_y = result['ground_truth']
            pred_x, pred_y = result['predicted']
            print(f"{result['filename']:<15} | GT: ({gt_x:>5.1f}, {gt_y:>5.1f}) | "
                  f"Pred: ({pred_x:>6.3f}, {pred_y:>6.3f}) | Error: {result['error']:>6.3f}")
        
    else:
        print("\nNo valid files were processed!")
        print("Make sure your CSV files follow the naming format: x,y.csv")
        print("Examples: -5,4.5.csv, 10,15.csv, 5,10.csv")

if __name__ == "__main__":
    main()