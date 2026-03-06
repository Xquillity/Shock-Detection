import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.interpolate import RBFInterpolator
import pandas as pd

# === FILE AND ANIMATION SETUP ===
file_to_read = "Data/center_hit.csv"  # Which file to read
num_samples = 15  # How many samples to animate through

# Read all samples from CSV
with open(file_to_read, 'r') as f:
    lines = f.readlines()

# Parse all samples
all_samples = []
for i in range(min(num_samples, len(lines))):
    line = lines[i].strip() 
    values = [float(val.strip()) for val in line.split(',') if val.strip()]
    if len(values) >= 6:
        all_samples.append(np.array(values[:6]))

print(f"Loaded {len(all_samples)} samples for animation")

# Define known data points (x, y) and their corresponding values (z)
x = np.array([0, -6, -2.5, 2.5, 6, 0])  # Chosen x-coordinates
y = np.array([0, 5.5, 11.5, 11.5, 5.5, 6])    # Chosen y-coordinates

# Create a meshgrid for interpolation
grid_x, grid_y = np.mgrid[-10:10:100j, 0:15:100j]

# Create a 3D plot 
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Animation function
def animate(frame):
    ax.clear()  # Clear the previous frame
    
    # Get sensor readings for this frame
    z = all_samples[frame % len(all_samples)]
    
    # Set gaussian kernel for this frame
    rbf = RBFInterpolator(np.column_stack((x, y)), z, kernel='gaussian', epsilon=0.1)
    
    # Perform interpolation on the grid
    points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    grid_z = rbf(points)
    grid_z = grid_z.reshape(grid_x.shape)
    
    # Plot the 3D surface
    surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', alpha=0.8, linewidth=0, antialiased=True)
    
    # Add sensor points
    ax.scatter(x, y, z, c='red', s=100, edgecolor='k')
    
    # Label sensor points
    for i in range(len(x)):
        ax.text(x[i], y[i], z[i] + np.max(z)*0.1, f'S{i}', fontsize=8, color='black')
    
    # Set consistent limits and labels
    ax.set_title(f'3D RBF Animation - Sample {frame + 1}/{len(all_samples)}')
    ax.set_xlabel('X (Inches)')
    ax.set_ylabel('Y (Inches)')
    ax.set_zlabel('Sensor Reading')
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 15)
    
    # Set consistent Z limits based on all data
    all_z_values = np.concatenate(all_samples)
    ax.set_zlim(np.min(all_z_values), np.max(all_z_values+100))
    
    return surf,

# Set up animation
print("Starting animation... Close the window to stop.")
anim = FuncAnimation(fig, animate, frames=len(all_samples), interval=200, blit=False, repeat=True)

# Show the plot
plt.show()