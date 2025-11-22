import numpy as np                      
import matplotlib.pyplot as plt          
from scipy.interpolate import Rbf        
from mpl_toolkits.mplot3d import Axes3D  

x = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])        # X coordinates of points
y = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])        # Y coordinates of points
z = np.array([1, 2, 3, 2, 5, 4, 3, 4, 5])        # Z values at those points

grid_x, grid_y = np.meshgrid(                     # Create a 2D grid for plotting
    np.linspace(x.min(), x.max(), 50),           # 50 points along X axis
    np.linspace(y.min(), y.max(), 50)            # 50 points along Y axis
)

rbf = Rbf(x, y, z)                               # Create a smooth interpolating function
grid_z = rbf(grid_x, grid_y)                     # Apply the function to the grid to get Z values

fig = plt.figure()                               # Create a figure window /the blank canvas for plotting
ax = fig.add_subplot(111, projection='3d')       # Add a 3D subplot/the area on that canvas where the 3D surface is drawn 

ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', edgecolor='none')  # Plot the smooth 3D surface

ax.set_xlabel('time')                               # Label X axis
ax.set_ylabel('position')                               # Label Y axis
ax.set_zlabel('peak value')                           # Label Z axis

plt.show()                                       # Display the 3D plot
