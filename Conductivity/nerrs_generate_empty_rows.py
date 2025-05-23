import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Example lists of times (replace with your actual data)
sal_data = pd.read_csv('/Users/isabellayeung/Downloads/MITSG_OA_WQ-master/Correlation_Coeff/NERRS_MP_2022_Matched_Tide_Updated.csv')
tide_data = pd.read_csv('/Users/isabellayeung/Downloads/MITSG_OA_WQ-master/Correlation_Coeff/NOAA_Tidal_1MIN_May-Dec_2022_DeadNeck_GMT.csv')

# Convert time strings to datetime objects
sal_data["Datetime"] = pd.to_datetime(sal_data["Salinity_Time"])
tide_data["Datetime"] = pd.to_datetime(tide_data["DateTime (UTC)"])

# Find the time range (start and end times)
start_time = min(list(sal_data["Datetime"]))
end_time = max(list(sal_data["Datetime"]))

# Generate all times that are multiples of 15 minutes between start_time and end_time
time_range = pd.date_range(start=start_time, end=end_time, freq='15T')

# Convert the list of times to sets for easier comparison
list1_set = set(sal_data["Datetime"])
#list2_set = set(tide_data["Datetime"])

# Find the times in list1 that are not in list2
missing_times = [time for time in time_range if time not in list1_set]

# Print the missing times
missing_time_list = []
for time in missing_times:
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    missing_time_list.append(time.strftime('%Y-%m-%d %H:%M:%S'))

tide_list = []
for time in missing_time_list:
    tide_height = tide_data.loc[tide_data["Datetime"] == time]["Pred"].values[0]
    print(f"Missing time: {time}, Tide Height: {tide_height}")
    tide_list.append(tide_height)

missing_sal_df = pd.DataFrame({'Salinity_Time': missing_time_list, 'Salinity': [np.nan]*len(missing_time_list), 'Tide_Height': tide_list, "Datetime": missing_time_list})

df_with_missing_sal_rows = pd.concat([sal_data, missing_sal_df], ignore_index=True)

df_with_missing_sal_rows_sorted = df_with_missing_sal_rows.sort_values('Salinity_Time')

#missing_tide_df = pd.DataFrame({"Datetime": missing_time_list, "Tide_Height": tide_list})
print(df_with_missing_sal_rows_sorted)
df_with_missing_sal_rows_sorted.to_csv('nerrs_2022_empty_sal_rows_test.csv', index=False)