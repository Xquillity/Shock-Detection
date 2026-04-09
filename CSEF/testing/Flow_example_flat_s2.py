import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import RBFInterpolator

# === SETUP ===
file_to_read = "Data/4_2_26_data/hit_3.csv"  
num_samples = 60  
ground_truth = (5, 10)  # SET THIS TO YOUR ACTUAL IMPACT LOCATION

# Read data
with open(file_to_read, 'r') as f:
    lines = f.readlines()

all_samples = []
for i in range(min(num_samples, len(lines))):
    line = lines[i].strip() 
    values = [float(val.strip()) for val in line.split(',') if val.strip()]
    if len(values) >= 6:
        values = values[0:6]  # Use S0-S5 for interpolation
        values[1] = values[1] * 1  # Scale S1 by 1
       # values[2] = values[2] * 0.3  # Scale S2 by 0.3
        all_samples.append(np.array(values[:6]))

      

print(f"Loaded {len(all_samples)} samples")

# Sensor locations
x = np.array([0, -6, -2.5, 2.5, 6, 0])  
y = np.array([0, 5.5, 11.5, 11.5, 5.5, 6])    
# Use all 6 sensors (S0-S5)
# Grid for interpolation
grid_x, grid_y = np.mgrid[-10:10:100j, 0:15:100j]

# Setup plot
fig, ax = plt.subplots(figsize=(10, 8))

def animate(frame):
    ax.clear()
    
    # Get sensor readings
    z = all_samples[frame % len(all_samples)]
    
    # Create RBF interpolator
    rbf = RBFInterpolator(np.column_stack((x, y)), z, kernel='gaussian', epsilon=0.25)
    
    # Interpolate over grid
    points = np.column_stack((grid_x.ravel(), grid_y.ravel()))
    grid_z = rbf(points).reshape(grid_x.shape)
    
    # Find max location (estimated impact)
    max_idx = np.unravel_index(np.argmax(grid_z), grid_z.shape)
    impact_x = grid_x[max_idx] 
    impact_y = grid_y[max_idx]
    
    # Calculate error
    error = np.sqrt((impact_x - ground_truth[0])**2 + (impact_y - ground_truth[1])**2)
    
    # Plot heatmap
    ax.imshow(grid_z.T, extent=(-10, 10, 0, 15), origin='lower', cmap='viridis', alpha=0.8)
    
    # Plot sensors
    ax.scatter(x, y, c=z, edgecolor='k', s=100, cmap='viridis')
    for i in range(len(x)):
        ax.annotate(f'S{i}', (x[i], y[i]), xytext=(5, 5), textcoords='offset points', 
                   fontsize=10, color='white')
    
    # Plot impact locations
    ax.scatter(impact_x, impact_y, c='red', s=200, marker='x', linewidths=4, label='RBF Estimate')
    ax.scatter(ground_truth[0], ground_truth[1], c='lime', s=200, marker='*', 
               edgecolor='black', linewidths=2, label='Ground Truth')
    
    # Labels and title
    ax.set_title(f'Sample {frame + 1}/{len(all_samples)} | Error: {error:.2f}"')
    ax.set_xlabel('X (inches)')
    ax.set_ylabel('Y (inches)')
    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 15)
    ax.legend()

# Run animation
anim = FuncAnimation(fig, animate, frames=len(all_samples), interval=400, repeat=True)
plt.show()