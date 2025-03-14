import pandas as pd

# Load the CSV file
file_path = "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\NERRS_Used\\MSTL_Filtered\\NERRS_2023_Metoxit_MSTL_Filtered_Data.csv"
df = pd.read_csv(file_path)


# Convert "Datetime_UTC" to datetime format
df["Datetime_UTC"] = pd.to_datetime(df["Datetime_UTC"])

# Sort by datetime to ensure proper time order
df = df.sort_values(by="Datetime_UTC").reset_index(drop=True)

# Set Datetime as index
df = df.set_index("Datetime_UTC")

# Compute time differences
df["Time_Diff"] = df["Datetime_UTC"].diff().dt.total_seconds() / (12 * 3600)  # Convert seconds to days

# Identify large gaps (greater than 1 day)
#gap_indices = df[df["Time_Diff"] > 0.5].index

gap_mask = df["Time_Diff"] > 0.5

# Interpolate only within the large gaps
for idx in df[gap_mask].index:
    # Find the previous and next valid values for interpolation
    prev_idx = df.loc[:idx - 1, "Sal"].last_valid_index()
    next_idx = df.loc[idx + 1:, "Sal"].first_valid_index()

    # Perform linear interpolation if valid indices exist
    if prev_idx is not None and next_idx is not None:
        df.loc[prev_idx:next_idx, "Sal"] = df.loc[prev_idx:next_idx, "Sal"].interpolate(method="linear")

# Interpolate "Sal" column only for gaps greater than 1 day
#df["Sal"] = df["Sal"].interpolate(method="linear")

# Drop the auxiliary "Time_Diff" column
#df = df.drop(columns=["Time_Diff"])

# Save the interpolated dataset
output_path = "testing_interpolation_v2.csv"
df.to_csv(output_path, index=False)
