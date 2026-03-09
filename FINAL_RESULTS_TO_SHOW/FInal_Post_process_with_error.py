import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
import pandas as pd

# === FILE AND SAMPLE SELECTION ===-----------------------------------------------------------------------------------------------------------------
file_to_read = "Data/Test_hit_5,4.5"  # Which file to read
sample_to_read = 0  # Which sample (line number) to read (0-based indexing)

# Read the selected sample from CSV
df = pd.read_csv(file_to_read, header=None)
sensor_values = df.iloc[sample_to_read].values  # Get the sensor readings S0-S4

# Convert to floats, handling empty values and taking only first 5 sensors
z_list = []
for i, val in enumerate(sensor_values):
    if i >= 5:  # Only take first 5 sensors (S0-S4)
        break
    val_str = str(val).strip()
    if val_str and val_str != 'nan':  # Check if not empty and not NaN
        z_list.append(float(val_str))
    else:
        z_list.append(0.0)  # Default to 0 for empty values

z = np.array(z_list)  # Convert to numpy array

# === GROUND TRUTH COORDINATES (USER INPUT) ==========================================================================================================
# Enter your actual impact point coordinates here
actual_x = 5.0  # Actual X coordinate (inches)
actual_y = 10.0  # Actual Y coordinate (inches)
print(f"Ground Truth: ({actual_x}, {actual_y})")
#====================sensor setup===========================================================================================================================
# Define known data points (x, y) and their corresponding values (z)
x = np.array([0, -6, -2.5, 2.5, 6])  # Chosen x-coordinates
y = np.array([0, 5.5, 11.5, 11.5, 5.5])    # Chosen y-coordinates

# Create a meshgrid for interpolation
grid_x, grid_y = np.mgrid[-10:10:100j, 0:15:100j]

# Create a plot 
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Linear kernel only

# Set linear kernel
rbf = RBFInterpolator(np.column_stack((x, y)), z, kernel='linear')

# Perform interpolation on the grid (stacking grid_x and grid_y)
points = np.column_stack((grid_x.ravel(), grid_y.ravel()))  # Combine into (n_points, 2)
grid_z = rbf(points)  # Perform interpolation

# Reshape grid_z back to the original grid shape
grid_z = grid_z.reshape(grid_x.shape)

# Plot the result
img = ax.imshow(grid_z.T, extent=(-10, 10, 0, 15), origin='lower', cmap='viridis', alpha=0.8)
ax.scatter(x, y, c=z, edgecolor='k', s=100, label='Sensor Points')  # Increased size for visibility

# Find maximum point coordinates
max_value = np.max(grid_z)
max_idx = np.unravel_index(np.argmax(grid_z), grid_z.shape)
max_x = grid_x[max_idx]
max_y = grid_y[max_idx]

# Mark the maximum point on the graph
ax.scatter(max_x, max_y, c='red', marker='.', s=150, edgecolor='white', linewidth=1, label=f'Interpolated Max')
ax.annotate(f'MAX ({max_x:.1f}, {max_y:.1f})', 
           (max_x, max_y), 
           xytext=(8, 8), 
           textcoords='offset points', 
           fontsize=9, 
           color='red', 
           fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='red'))

# Mark the ground truth point on the graph
ax.scatter(actual_x, actual_y, c='blue', marker='X', s=150, edgecolor='white', linewidth=1, label=f'Ground Truth')
ax.annotate(f'GT ({actual_x:.1f}, {actual_y:.1f})', 
           (actual_x, actual_y), 
           xytext=(-8, -20), 
           textcoords='offset points', 
           fontsize=9, 
           color='blue', 
           fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='blue'))

# Calculate error using Pythagorean theorem
error_distance = np.sqrt((max_x - actual_x)**2 + (max_y - actual_y)**2)
print(f"\n=== ERROR ANALYSIS ===")
print(f"Interpolated Maximum: ({max_x:.3f}, {max_y:.3f})")
print(f"Ground Truth: ({actual_x:.3f}, {actual_y:.3f})")
print(f"Error Distance (Pythagorean): {error_distance:.3f} inches")
print(f"Error in X: {abs(max_x - actual_x):.3f} inches")
print(f"Error in Y: {abs(max_y - actual_y):.3f} inches")

# Draw line connecting ground truth and interpolated points
ax.plot([actual_x, max_x], [actual_y, max_y], 'k--', linewidth=1.5, alpha=0.6, label=f'Error: {error_distance:.2f}"')

# Label each sensor point
for i in range(len(x)):
    ax.annotate(f'S{i}', (x[i], y[i]), xytext=(5, 5), textcoords='offset points', fontsize=10, color='white')

ax.set_title('RBF Interpolation with Kernel: linear')
ax.set_xlabel('X ( Inches)')
ax.set_ylabel('Y ( Inches)')
ax.set_xlim(-10, 10)  # Explicitly set x limits
ax.set_ylim(0, 15)   # Explicitly set y limits
plt.colorbar(img, ax=ax, label='Interpolated Values')
ax.legend()  # Add legend to show data points and max point

# Show the plot
plt.show()