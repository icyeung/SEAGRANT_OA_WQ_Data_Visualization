import pandas as pd

# Load the salinity and tidal data
salinity_df = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\NERRS_Not_Used\\No_Flags\\wqbmpwq2022_NoFlagged.csv', parse_dates=['DateTimeStamp'])
tidal_df = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\NOAA_Tidal_1MIN_May-Dec_2022_DeadNeck_GMT.csv', parse_dates=['DateTime (UTC)'])

# Convert time columns to datetime format if not already
salinity_df['time_column'] = pd.to_datetime(salinity_df['Datetime'])
tidal_df['time_column'] = pd.to_datetime(tidal_df['DateTime (UTC)'])

# Ensure that the tidal data is sorted by time for efficient matching
tidal_df = tidal_df.sort_values('time_column')

# Create an empty list to store the matched data
matched_data = []

# For each salinity record, find the exact corresponding tidal record
for _, salinity_row in salinity_df.iterrows():
    # Find the closest time in the tidal data for the exact timestamp
    tidal_row = tidal_df[tidal_df['time_column'] == salinity_row['time_column']]
    
    # If an exact match is found, add it to the matched data
    if not tidal_row.empty:
        matched_data.append({
            'Salinity_Time': salinity_row['time_column'],
            'Salinity': salinity_row['Sal'],
            'Tide_Height': tidal_row.iloc[0]['Pred']
        })

# Convert the matched data to a DataFrame
matched_df = pd.DataFrame(matched_data)

matched_df.to_csv('NERRS_MP_2022_Matched_Tide_Updated.csv', index=False)

# View the combined data
print(matched_df)