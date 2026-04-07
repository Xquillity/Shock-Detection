# Interpolation for every time sample between 2 sensors and 3D plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Load CSV
data = pd.read_csv(r'D:\Github\Shock-Detection\Data\data_3.csv', header=None)  # sensor readings the z axis valus
data_first_90 = data.iloc[:90]

# Prepare grid for 3D plot
times = np.arange(len(data_first_90)) # times is basically the x axis
sensors = [0, 1] 
y_points = np.linspace(0, 1, 50) # setup y axsis
X, Y = np.meshgrid(times, y_points) # set up  x and y for the plot, times = x axis, y_points = y axis


# Interpolate sensor values for each time
Z = np.zeros_like(X) # setup Z axis
for i, t in enumerate(times):
    values = data.iloc[i].values #  changed so it picks the sensor readings for the current time 
    f = interp1d(sensors, values, kind='linear')  
    estimated_values = f(y_points)                 
    Z[:, i] = estimated_values                      
             

# Plot 3D surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none') # actually plot it now using 
ax.set_xlabel('Time')    
ax.set_ylabel('Sensor')  
ax.set_zlabel('Value')   
plt.show()
