import pandas as pd
import numpy as np
from scipy.interpolate import RBFInterpolator
from scipy.stats import zscore 
import matplotlib.pyplot as plt

# Setup
file_to_read = "Data/4_2_26_data/hit_5.csv"
ground_truth = (5, 10.0)  # (x, y)
sensor_coords = np.array([[0, 0], [-6, 5.5], [-2.5, 11.5], [2.5, 11.5], [6, 5.5], [0, 6]])

# Read data and process each sample
df = pd.read_csv(file_to_read, header=None)
results = []

for i, row in df.iterrows():
    # Get first 6 sensor values
    sensors = pd.to_numeric(row[:6], errors='coerce').fillna(0).values
    
    if sensors.sum() == 0:  # Skip empty samples
        continue
    
    # RBF interpolation to find max point
    rbf = RBFInterpolator(sensor_coords, sensors, kernel='gaussian', epsilon=0.2)
    grid_x, grid_y = np.mgrid[-10:10:100j, 0:15:100j]
    grid_z = rbf(np.column_stack([grid_x.ravel(), grid_y.ravel()])).reshape(grid_x.shape)
    max_pos = np.unravel_index(grid_z.argmax(), grid_z.shape)
    max_x, max_y = grid_x[max_pos], grid_y[max_pos]
    
    # Calculate error manually
    error = np.sqrt((max_x - ground_truth[0])**2 + (max_y - ground_truth[1])**2)
    
    # Use library for box plot stats
    sensor_stats = pd.Series(sensors).describe()
    mean_val = sensor_stats['mean']
    median_val = sensor_stats['50%']
    iqr = sensor_stats['75%'] - sensor_stats['25%']
    outliers = np.where(np.abs(zscore(sensors)) > 2)[0].tolist()
    
    results.append({
        'sample': i,
        'avg_error': error,
        'sensor_mean': mean_val,
        'sensor_median': median_val,
        'sensor_iqr': iqr,
        'outliers': outliers
    })
    
    print(f"Sample {i:3d}: Error={error:.2f}, Mean={mean_val:.2f}, Median={median_val:.2f}, IQR={iqr:.2f}, Outliers={outliers}")

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('simple_results.csv', index=False)

# Create x,y plots
if len(results) > 0:
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Error vs Median
    errors = [r['avg_error'] for r in results]
    medians = [r['sensor_median'] for r in results]
    axes[0, 0].plot(medians, errors, 'bo')
    axes[0, 0].set_title('Sensor Median vs Error')
    axes[0, 0].set_xlabel('Sensor Median')
    axes[0, 0].set_ylabel('Error (inches)')
    axes[0, 0].grid(True)
    
    # Error vs Mean
    means = [r['sensor_mean'] for r in results]
    axes[0, 1].plot(means, errors, 'go')
    axes[0, 1].set_title('Sensor Mean vs Error')
    axes[0, 1].set_xlabel('Sensor Mean')
    axes[0, 1].set_ylabel('Error (inches)')
    axes[0, 1].grid(True)
    
    # IQR vs Error
    iqrs = [r['sensor_iqr'] for r in results]
    axes[1, 0].plot(iqrs, errors, 'ro')
    axes[1, 0].set_title('Sensor IQR vs Error')
    axes[1, 0].set_xlabel('Sensor IQR')
    axes[1, 0].set_ylabel('Error (inches)')
    axes[1, 0].grid(True)
    
    # Outlier values vs Error
    outlier_values = []
    outlier_errors = []
    for j, result in enumerate(results):
        if result['outliers']:  # If there are outliers
            # Get the sensor values for this sample
            sensors = pd.to_numeric(df.iloc[result['sample']][:6], errors='coerce').fillna(0).values
            for outlier_idx in result['outliers']:
                outlier_values.append(sensors[outlier_idx])
                outlier_errors.append(result['avg_error'])
    
    if outlier_values:  # Only plot if we have outlier data
        axes[1, 1].plot(outlier_values, outlier_errors, 'mo')
        axes[1, 1].set_title('Outlier Sensor Values vs Error')
        axes[1, 1].set_xlabel('Outlier Sensor Value')
        axes[1, 1].set_ylabel('Error (inches)')
    else:
        axes[1, 1].text(0.5, 0.5, 'No Outliers Found', ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Outlier Sensor Values vs Error')
        axes[1, 1].set_xlabel('Outlier Sensor Value')
        axes[1, 1].set_ylabel('Error (inches)')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.show()
    print("\nX,Y plots displayed!")
else:
    print("No data to plot")