import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
import pandas as pd

# === FILE AND SAMPLE SELECTION ===
file_to_read = "Data/s1_3_data.csv"  # Which file to read
sample_to_read = 1  # Which sample (line number) to read (0-based indexing)

# Read the selected sample from CSV
df = pd.read_csv(file_to_read, header=None)
sensor_values = df.iloc[sample_to_read].values  # Get the sensor readings S0-S4
z = np.array([float(str(val).strip()) for val in sensor_values])  # Convert to floats and strip whitespace

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
ax.scatter(max_x, max_y, c='red', marker='.', s=100, edgecolor='red', linewidth=1, label=f'Max Point')
ax.annotate(f'MAX\n({max_x:.2f}, {max_y:.2f})\nValue: {max_value:.3f}', 
           (max_x, max_y), 
           xytext=(10, 10), 
           textcoords='offset points', 
           fontsize=12, 
           color='red', 
           fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

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