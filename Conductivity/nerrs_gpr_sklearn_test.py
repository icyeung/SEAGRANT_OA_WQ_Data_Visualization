import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel, ExpSineSquared
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV



print("hi0")

# Load data


true_df = pd.read_csv("gpr_test_true_values.csv")
true_df['datetime'] = pd.to_datetime(true_df['Salinity_Time'])

orig_df = pd.read_csv("gpr_test.csv")
orig_df['datetime'] = pd.to_datetime(orig_df['Salinity_Time'])
orig_df['time_numeric'] = (orig_df['datetime'] - orig_df['datetime'].min()).dt.total_seconds()


scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(orig_df[['Salinity', 'Tide_Height']])
df = pd.DataFrame(scaled_data, columns=['Salinity', 'Tide_Height'])
df['datetime'] = orig_df['datetime']
df['time_numeric'] = orig_df['time_numeric']
df['True_Salinity'] = true_df['Salinity']
scaled_true_data = scaler.fit_transform(true_df[['Salinity']])
df['True_Salinity_Scaled'] = scaled_true_data

# Separates data into observed and missing
observed = df[~df['Salinity'].isna()]
missing = df[df['Salinity'].isna()]

X_train = observed[['Tide_Height', 'time_numeric']].values
y_train = observed['Salinity'].values

X_missing = missing[['Tide_Height', 'time_numeric']].values

print("hi1")


#GPR Test Version 1
'''
# Kernel = trend + periodic component + noise
param_grid = {
    'kernel' : [
        (ConstantKernel(1.0) * RBF(length_scale=96) +  # length_scale tuned for [tidal, time]
        ExpSineSquared(length_scale=6, periodicity=100) +  # 12-hour tidal cycle in seconds
        WhiteKernel(noise_level=0.5))]
}

print("hi2")

gpr = GaussianProcessRegressor()


grid_search1 = GridSearchCV(gpr, param_grid, scoring='neg_mean_squared_error')
grid_search1.fit(X_train, y_train)

best_params = grid_search1.best_params_
print("Best parameters found: ", best_params)

best_score = grid_search1.best_score_
print("Best score (negative MSE): ", best_score)

print("hi3")


# Predicts missing salinity
y_pred = grid_search1.predict(X_missing)

# Fill in the missing salinity values in dataframe
df.loc[df['Salinity'].isna(), 'Salinity'] = y_pred
'''


# GPR Test Version 2
# Specify Gaussian Processes with fixed and optimized hyperparameters
gp_fix = GaussianProcessRegressor(kernel=(0.1 * RBF(35040) + # length_scale tuned for [tidal, time]
                                          2.0 * ExpSineSquared(length_scale=24, periodicity=2832) +  # 12-hour tidal cycle
                                          WhiteKernel(noise_level=0.5)),
                                  optimizer=None)
gp_fix.fit(X_train, y_train)

gp_opt = GaussianProcessRegressor(kernel=(0.1 * RBF(35040) + # length_scale tuned for [tidal, time]
                                          2.0 * ExpSineSquared(length_scale=24, periodicity=2832) +  # 12-hour tidal cycle
                                          WhiteKernel(noise_level=0.5)), n_restarts_optimizer=10)
gp_opt.fit(X_train, y_train)

y_fix_pred, sigma_fix = gp_fix.predict(X_missing, return_std=True)
y_opt_pred, sigma_opt = gp_opt.predict(X_missing, return_std=True)

print("hi4")

missing_salinity_rows = df[df['Salinity'].isna()]
datetimes_no_salinity = missing_salinity_rows['datetime'].to_list()


print("Fixed_Params:", gp_fix.get_params())
print("Fixed_Params_Kernel:", gp_fix.kernel_)
print("-----------------------------------------------------------")
print("Optimized_Params:", gp_opt.get_params())
print("Optimized_Params_Kernel:", gp_opt.kernel_)


# Fill in the missing salinity values

df['Salinity_with_Fixed_Pred'] = df['Salinity']
df["Salinity_with_Opt_Pred"] = df['Salinity']
df.loc[df['Salinity_with_Fixed_Pred'].isna(), 'Salinity_with_Fixed_Pred'] = y_fix_pred
df.loc[df['Salinity_with_Opt_Pred'].isna(), 'Salinity_with_Opt_Pred'] = y_opt_pred


print("hi5")

# Saves results to csv
df.to_csv("interpolated_gpr_fixed_and_opt_param_2022_nerrs.csv")

# Plots results
plt.figure(figsize=(14, 6))
#plt.plot(df['datetime'], df['Salinity'], label='Interpolated Salinity', color='blue')
plt.plot(df['datetime'], df['True_Salinity_Scaled'], label='True Salinity', color='green', linestyle='--')
plt.plot(df['datetime'], df['Salinity_with_Fixed_Pred'], label='Salinity with Fixed Hyper', color='blue')
plt.plot(df['datetime'], df['Salinity_with_Opt_Pred'], label='Salinity with Optimized Hyper', color='red')
plt.scatter(observed['datetime'], observed['Salinity'], label='Observed Salinity', color='black', s=10)
#plt.fill_between(missing['datetime'], y_pred - 2 * sigma, y_pred + 2 * sigma, color='blue', alpha=0.2, label='95% Confidence Interval')
plt.fill_between(datetimes_no_salinity, y_fix_pred - 2 * sigma_fix, 
                 y_fix_pred + 2 * sigma_fix, color='blue', alpha=0.2, label='95% CI Fixed Hyper')
plt.fill_between(datetimes_no_salinity, y_opt_pred - 2 * sigma_opt,
                 y_opt_pred + 2 * sigma_opt, color='red', alpha=0.2, label='95% CI Optimized Hyper')
plt.xlabel('Date')
plt.ylabel('Salinity')
plt.title('Salinity Interpolation using GPR with Tidal Height and Time')
plt.legend()
plt.grid(True)
plt.show()
