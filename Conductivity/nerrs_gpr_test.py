import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel, ExpSineSquared
from sklearn.preprocessing import MinMaxScaler



print("hi0")

# Load data
orig_df = pd.read_csv("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ-master\\nerrs_2022_empty_sal_rows_test.csv")
orig_df['datetime'] = pd.to_datetime(orig_df['Salinity_Time'])
orig_df['time_numeric'] = (orig_df['datetime'] - orig_df['datetime'].min()).dt.total_seconds()

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(orig_df[['Salinity', 'Tide_Height']])
df = pd.DataFrame(scaled_data, columns=['Salinity', 'Tide_Height'])
df['datetime'] = orig_df['datetime']
df['time_numeric'] = orig_df['time_numeric']

# Separates data into observed and missing
observed = df[~df['Salinity'].isna()]
missing = df[df['Salinity'].isna()]

X_train = observed[['Tide_Height', 'time_numeric']].values
y_train = observed['Salinity'].values

X_missing = missing[['Tide_Height', 'time_numeric']].values

print("hi1")


# Kernel = trend + periodic component + noise
kernel = (
    ConstantKernel(1.0) * RBF(length_scale=[1.0, 1e5]) +  # length_scale tuned for [tidal, time]
    ExpSineSquared(length_scale=1.0, periodicity=43200) +  # 12-hour tidal cycle in seconds
    WhiteKernel(noise_level=0.1)
)

print("hi2")

gpr = GaussianProcessRegressor(kernel=kernel, normalize_y=True, optimizer='fmin_l_bfgs_b')
gpr.fit(X_train, y_train)

print("hi3")

# Predicts missing salinity
y_pred, sigma = gpr.predict(X_missing, return_std=True)

print("hi4")

# Fill in the missing salinity values
df.loc[df['Salinity'].isna(), 'Salinity'] = y_pred

print("hi5")

# Saves results to csv
df.to_csv("interpolated_gpr_2022_nerrs.csv")

# Plots results
plt.figure(figsize=(14, 6))
plt.plot(df['datetime'], df['Salinity'], label='Interpolated Salinity', color='blue')
plt.scatter(observed['datetime'], observed['Salinity'], label='Observed Salinity', color='black', s=10)
plt.fill_between(missing['datetime'], y_pred - 2 * sigma, y_pred + 2 * sigma,
                 color='blue', alpha=0.2, label='95% Confidence Interval')
plt.xlabel('Date')
plt.ylabel('Salinity')
plt.title('Salinity Interpolation using GPR with Tidal Height and Time')
plt.legend()
plt.grid(True)
plt.show()
