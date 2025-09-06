import pandas as pd
import matplotlib.pyplot as plt

# Load and reverse the file
df = pd.read_csv(r'D:\Github\Shock-Detection\Data\data_3.csv', header=None)
# df = df[::-1].reset_index(drop=True)

chunk_size = 90  # Number of samples per graph
plt.figure()

# Loop through data in chunks of 30
for start in range(0, len(df), chunk_size):
    end = start + chunk_size
    chunk = df[start:end]           # Extract the current chunk
    time = range(0, len(chunk))     # Time axis for this chunk
 
    # Sensor left = blue , Sensor right = orange 
    plt.plot(time, chunk[0])
    #plt.plot(time, chunk[1])
    plt.title(f'Samples {start} to {end})')
    plt.xlabel('Time')
    plt.ylabel('Vibration')

plt.show()
