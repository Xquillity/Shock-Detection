import numpy as np
import matplotlib.pyplot as plt

# Parameters from image
d33 = 460e-12
epsilon_r = 1750
epsilon_0 = 8.854e-12
A = 0.000962  # m^2 (converted from mm^2)
t = 0.00053  # m (converted from mm)

# Formula: V = (d33 · F · t) / (εr · ε0 · A)
def force_to_voltage(F):
    return (d33 * F * t) / (epsilon_r * epsilon_0 * A)

def voltage_to_force(V):
    return (V * epsilon_r * epsilon_0 * A) / (d33 * t)

def analog_to_voltage(analog):
    return (analog / 1024) * 5.0

def analog_to_force(analog):
    V = analog_to_voltage(analog)
    return voltage_to_force(V)

# Data
analog_values = np.linspace(0, 1023, 100)
forces = analog_to_force(analog_values)

# Graph
plt.figure(figsize=(10, 6))
plt.plot(analog_values, forces, 'b-', linewidth=2)
plt.xlabel('Digital Reading (0-1023)')
plt.ylabel('Impact Force (N)')
plt.title('Impact Force vs Digital Reading')
plt.grid(True, alpha=0.3)
plt.xticks(np.arange(0, 1024, 100))
plt.show()

print(f"1023 analog = {analog_to_voltage(1023):.2f}V = {analog_to_force(1023):.1f}N")
