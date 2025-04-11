import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

time_series = np.random.random(200)

fft_values = fft(time_series)
fft_magnitude = np.abs(fft_values)
frequencies = np.fft.fftfreq(len(time_series))

plt.plot(frequencies, fft_magnitude)
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum')
plt.show()

threshold = 7
fft_values_filtered = fft_values.copy()
fft_values_filtered[fft_magnitude < threshold] = 0

filtered_time_series = ifft(fft_values_filtered)

plt.plot(time_series, label='Original Time Series')
plt.plot(filtered_time_series.real, label='Filtered Time Series', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time Series Forecasting')
plt.legend()
plt.show()
