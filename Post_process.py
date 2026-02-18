#Initial code for reading multiple graphs from csv file
#obsolete after interpolation implementation

import pandas as pd
import matplotlib.pyplot as plt

# Load and reverse the file
df = pd.read_csv(r'D:\Github\Shock-Detection\Data\data_3.csv', header=None)
data_first_90 = df.iloc[:90]

chunk_size = 90  # Number of samples per graph
plt.figure()

# Loop through data in chunks of 30
for start in range(0, len(data_first_90), chunk_size):
    end = start + chunk_size
    chunk = df[start:end]           # Extract the current chunk
    time = range(0, len(chunk))     # Time axis for this chunk
 
    # Sensor left = blue , Sensor right = orange 
    plt.plot(time, chunk[0], label='Sensor 1 (Left)')
    plt.plot(time, chunk[1], label='Sensor 2 (Right)')
    plt.legend()
    plt.title(f'Samples {start} to {end})')
    plt.xlabel('Time')
    plt.ylabel('Vibration')

plt.show()
