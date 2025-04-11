import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
def plot_correlation_coefficients(df, nerrs, title):
    """
    Plot the correlation coefficients between nerrs and other columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    nerrs (str): Column name for nerrs.
    title (str): Title for the plot.
    """
    # Calculate correlation coefficients
    corr = df.corr()[nerrs].drop(nerrs)

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    corr.plot(kind='bar', color='skyblue')
    plt.title(title)
    plt.xlabel('Features')
    plt.ylabel('Correlation Coefficient')
    plt.axhline(0, color='black', lw=1, ls='--')
    plt.grid(axis='y')
    plt.show()
'''

uncleaned_df = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\NERRS_MP_2022_Matched_Tide.csv", parse_dates=['Salinity_Time'])

# Drop rows with NaN in Salinity or Tide_Height
df = uncleaned_df[['Salinity', 'Tide_Height']].dropna()

# Extract the time series for Salinity and Tide_Height
salinity = df['Salinity'].values
tide_height = df['Tide_Height'].values

# Function to calculate cross-correlation with lags
def cross_correlation_with_lags(x, y, max_lag):
    lags = np.arange(-max_lag, max_lag + 1)
    corr = []
    
    '''
    # Loop over each lag to calculate the correlation coefficient
    for lag in lags:
        if lag < 0:
            corr_value = np.corrcoef(x[:lag], y[-lag:])[0, 1]
        elif lag > 0:
            corr_value = np.corrcoef(x[lag:], y[:-lag])[0, 1]
        else:
            corr_value = np.corrcoef(x, y)[0, 1]
        corr.append(corr_value)

        print(corr_value)
    
    return lags, corr

    '''

    for lag in lags:
        # Adjust the slices based on the lag value
        if lag < 0:
            # Shift y backward (i.e., x leads y)
            if len(x[:lag]) > 1 and len(y[-lag:]) > 1:  # Ensure slices are long enough
                corr_value = np.corrcoef(x[:lag], y[-lag:])[0, 1]
                print("hi1")
            else:
                corr_value = np.nan
        elif lag > 0:
            # Shift x forward (i.e., y leads x)
            if len(x[lag:]) > 1 and len(y[:-lag]) > 1:  # Ensure slices are long enough
                corr_value = np.corrcoef(x[lag:], y[:-lag])[0, 1]
                print("hi2")
            else:
                corr_value = np.nan
        else:
            # No lagn
            if len(x) > 1 and len(y) > 1:
                corr_value = np.corrcoef(x, y)[0, 1]
                print("hi3")
            else:
                corr_value = np.nan
        
        corr.append(corr_value)
    
    return lags, corr

# Set the maximum lag (e.g., 10 time steps)
max_lag = 48

# Calculate the cross-correlation
lags, corr = cross_correlation_with_lags(salinity, tide_height, max_lag)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(lags, corr, marker='o', linestyle='-', color='b')
plt.title('Cross-Correlation between NERRS Metoxit 2022 Salinity and Boston Tide Height')
plt.xlabel('Lag in Time Steps (1 Time Step = 15 Mins)')
plt.ylabel('Correlation Coefficient')
plt.grid(True)
plt.savefig('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\NERRS_MP_2022_Salinity_Tide_Cross_Correlation_Lag_Graph.png')
plt.show()