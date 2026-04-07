import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

# Create a 3D plot 
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Set linear kernel
rbf = RBFInterpolator(np.column_stack((x, y)), z, kernel='linear')

# Perform interpolation on the grid
points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
grid_z = rbf(points)
grid_z = grid_z.reshape(grid_x.shape)

# Plot the 3D surface
surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', alpha=0.8, linewidth=0, antialiased=True)

# Add sensor points as 3D scatter
ax.scatter(x, y, z, c='red', s=100, edgecolor='k', label='Sensor Locations')

# Label each sensor point
for i in range(len(x)):
    ax.text(x[i], y[i], z[i] + max(z)*0.1, f'S{i}', fontsize=10, color='black')

ax.set_title('3D RBF Interpolation with Linear Kernel')
ax.set_xlabel('X (Inches)')
ax.set_ylabel('Y (Inches)')
ax.set_zlabel('Sensor Reading')
ax.set_xlim(-10, 10)
ax.set_ylim(0, 15)
plt.colorbar(surf, ax=ax, label='Interpolated Values', shrink=0.8)

# Show the plot
plt.show()
plt.show()