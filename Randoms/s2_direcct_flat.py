import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
import pandas as pd

# === FILE AND SAMPLE SELECTION ===
file_to_read = "Data/center_hit.csv"  # Which file to read
sample_to_read = 1  # Which sample (line number) to read (0-based indexing)

# Read the selected sample from CSV
with open(file_to_read, 'r') as f:
    lines = f.readlines()

# Parse the line manually to handle inconsistent CSV format
line = lines[sample_to_read].strip()
# Split by comma and clean up each value, skip non-numeric entries
values = []
for val in line.split(','):
    val = val.strip()
    if val and not 'Sample index' in val:  # Skip sample index text
        try:
            values.append(float(val))
        except ValueError:
            continue  # Skip non-numeric values

# Take first 6 values (S0-S5) 
z = np.array(values[:6])

# Define known data points (x, y) and their corresponding values (z) - 6 sensors
x = np.array([0, -6, -2.5, 2.5, 6, 0])  # Chosen x-coordinates
y = np.array([0, 5.5, 11.5, 11.5, 5.5, 6])    # Chosen y-coordinates

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
ax.scatter(x, y, c=z, edgecolor='k', s=100, label='Data Points')  # Increased size for visibility

# Label each point
for i in range(len(x)):
    ax.annotate(f'S{i}', (x[i], y[i]), xytext=(5, 5), textcoords='offset points', fontsize=10, color='white')

ax.set_title('RBF Interpolation with Kernel: linear')
ax.set_xlabel('X ( Inches)')
ax.set_ylabel('Y ( Inches)')
ax.set_xlim(-10, 10)  # Explicitly set x limits
ax.set_ylim(0, 15)   # Explicitly set y limits
plt.colorbar(img, ax=ax, label='Interpolated Values')

# Show the plot
plt.show()