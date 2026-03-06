import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import RBFInterpolator
import pandas as pd

# === FILE AND ANIMATION SETUP ===
file_to_read = "Data/center_hit.csv"  # Which file to read
num_samples = 16  # How many samples to animate through

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

# Create a 2D plot 
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

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
    
    # Plot the 2D heatmap
    img = ax.imshow(grid_z.T, extent=(-10, 10, 0, 15), origin='lower', cmap='viridis', alpha=0.8)
    
    # Add sensor points
    ax.scatter(x, y, c=z, edgecolor='k', s=100, cmap='viridis')
    
    # Label sensor points
    for i in range(len(x)):
        ax.annotate(f'S{i}', (x[i], y[i]), xytext=(5, 5), textcoords='offset points', fontsize=10, color='white')
    
    # Set consistent limits and labels
    ax.set_title(f'2D RBF Animation - Sample {frame + 1}/{len(all_samples)}')
    ax.set_xlabel('X (Inches)')
    ax.set_ylabel('Y (Inches)')
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 15)
    
    return img,

# Set up animation
print("Starting animation... Close the window to stop.")
anim = FuncAnimation(fig, animate, frames=len(all_samples), interval=10, blit=False, repeat=True)

# Show the plot
plt.show()