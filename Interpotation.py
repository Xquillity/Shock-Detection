# Linear Interpolation beetween a single sample of 2 senors
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#Load CSV file
data = pd.read_csv(r'D:\Github\Shock-Detection\Data\data_3.csv', header=None, names=["sensor1", "sensor2"])

# find peak values
sensor1_peak_row = data["sensor1"].idxmax()
sensor2_peak_row = data["sensor2"].idxmax()

sensor1_peak_value = data.loc[sensor1_peak_row, "sensor1"]
sensor2_peak_value = data.loc[sensor2_peak_row, "sensor2"]

if sensor1_peak_value > sensor2_peak_value:
    max_value_index = sensor1_peak_row
else:
    max_value_index = sensor2_peak_row

sensor1_peak_value = data.loc[max_value_index, "sensor1"]
sensor2_peak_value = data.loc[max_value_index, "sensor2"]

print(sensor1_peak_value    )
print(sensor2_peak_value)

#ninterpolation setup 
sensor_locations = [0, 1]  # positions of the two sensors
sensor_peaks = [sensor1_peak_value, sensor2_peak_value]

linear_model = interp1d(sensor_locations, sensor_peaks, kind="linear")

evaluation_points = np.linspace(sensor_locations[0], sensor_locations[1], 50) 
estimated_values = linear_model(evaluation_points)

max_value_index = np.argmax(estimated_values)
predicted_impact_location = evaluation_points[max_value_index]


plt.plot(evaluation_points, estimated_values, "b-", label="Interpolated") 
#plt.axvline(predicted_impact_location, color="g", linestyle="--", label="Estimated impact") 
plt.xlabel("Position")
plt.ylabel("Peak value")
plt.legend()
plt.show()

