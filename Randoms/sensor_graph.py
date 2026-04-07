import pandas as pd
import matplotlib.pyplot as plt

# Read data
data = pd.read_csv('Data/s1_3_data.csv', header=None)

# Create samples (x-axis)
samples = range(len(data))

# Plot
plt.figure(figsize=(10, 6))

# Loop through each sensor and plot normalized
for i in range(5):

    sensor_data = data[i]
    plt.plot(samples, sensor_data, label=f'Sensor {i+1}')

plt.xlabel('Samples')
plt.ylabel('Sensor Values')
plt.title('All Sensors')
plt.legend()
plt.grid(True)
plt.ylim(0, 110)
plt.yticks(range(0, 111, 20))
plt.tick_params(axis='y', labelsize=12)
plt.tight_layout()
plt.show()