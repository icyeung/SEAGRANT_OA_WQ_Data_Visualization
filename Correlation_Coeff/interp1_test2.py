import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#df = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\NERRS_Not_Used\\No_Flags\\wqbmpwq2022_NoFlagged.csv')
df_withtide_unsampled = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\NERRS_test_data_2022.csv')

df_withtide_unsampled["Datetime"] = pd.to_datetime(df_withtide_unsampled["Salinity_Time"])

df_withtide = df_withtide_unsampled.sample(frac=0.8, random_state=42)

# Convert Salinity_Time to datetime
df_withtide['Datetime'] = pd.to_datetime(df_withtide['Salinity_Time'])


# Set the datetime as the index
df_withtide.set_index('Datetime', inplace=True)

# Create the full range of timestamps at 15-minute intervals
full_range = pd.date_range(start="2022-08-15 03:30:00", end="2022-12-20 13:30:00", freq="15T")

# Reindex the dataframe to the full range
df_full = df_withtide.reindex(full_range)

# Perform spline interpolation (order=3 for cubic spline)
df_full['Salinity'] = df_full['Salinity'].interpolate(method='spline', order=3)

# Preview the interpolated result
df_full[['Salinity']].head(10)


# Create the plot
plt.figure(figsize=(12, 6))
plt.scatter(df_withtide_unsampled['Datetime'], df_withtide_unsampled['Salinity'], color='orange', s=10, alpha=0.5, label = "Original_Data")
plt.scatter(df_full.index, df_full['Salinity'], color='teal', linewidth=2, label='Interpolated', marker = "*")

plt.legend()
plt.title("Salinity Over Time", fontsize=16)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Salinity", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()


'''

df_notideduplicate = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\NERRS_MP_2022_Matched_Tide_NoTideDuplicates.csv')
missing_tide = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\Missing_Tide_withDate.csv')

# Convert Salinity_Time to datetime
df_notideduplicate['Datetime'] = pd.to_datetime(df_notideduplicate['Salinity_Time'])

df_notideduplicate = df_notideduplicate.sort_values(by='Tide_Height')

missingtide = missing_tide["Tide_Height"]

alltide = list(missingtide) + list(df_notideduplicate["Tide_Height"])

# Set the datetime as the index
df_notideduplicate.set_index('Tide_Height', inplace=True)

print(df_notideduplicate)

# Create the full range of timestamps at 15-minute intervals


alltide_list = []
for tides in alltide:
    print(tides)
    tides = float(tides)
    alltide_list.append(tides)

alltide_list = alltide_list.sort()

# Reindex the dataframe to the full range
df_alltide = df_notideduplicate.reindex(alltide_list)

print(alltide_list)

# Perform spline interpolation (order=3 for cubic spline)
df_alltide['Salinity'] = df_alltide['Salinity'].interpolate(method='spline', order=3)
df_alltide['Datetime'] = pd.to_datetime(df_alltide['Datetime'])
# Preview the interpolated result
df_alltide[['Salinity']].head(10)

print(df_alltide)
print(len(df_alltide))

df_alltide.to_csv('NERRS_MP_2022_Matched_Tide_InterpolatedByTide.csv', index=False)

# Create the plot
plt.figure(figsize=(12, 6))
plt.scatter(df_withtide["Datetime"], df_withtide['Salinity'], color='orange', s=10, alpha=0.5, label = "Original_Data")
#plt.scatter(df_notideduplicate.index, df_notideduplicate['Salinity'], color='teal', linewidth=2, label='No_Tide_Duplicates')
plt.scatter(df_alltide["Datetime"], df_alltide['Salinity'], color='red', s=10, alpha=0.5, label = "Interpolated")
plt.legend()
plt.title("Salinity Over Time", fontsize=16)
plt.xlabel("Time", fontsize=12)
plt.ylabel("Salinity", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
'''