import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as md
import datetime

# Input: Tidal Data, 1.2 Region of conductivity data
# Need to look for dates of nearest time and day comparisons of low tide and high tide daily
# Checks if times are same, if so, concats tidal time and day and conductivity value for nearest fitting time to list
# Plots list as dot plot

# For NOAA data, need to convert the time from 12H to 24H using self-created program
# Break up time string using .split(" ")[-1]
# If that string says "PM", add 12 hours to the hours
# If that string says "AM", and the hour is 12, change the hour to 0
# Piece string back together and convert string to datetime object using dt.strptime(sting, "%H:%M:%S")

# Convert date to datetime object using dt.strptime(string, "%m-%d-%Y")
# Combine date and time datetime objects using dt.combine(date, time)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# HOBO #1 2022 (Pocasset)
hobo_data = pd.read_csv(os.path.join(__location__, "HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Pocasset_12-9-22_1_NO_offset.csv"))

# Pocasset River Entrance 2023
NOAA_tidal_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Tide_Data\\NOAA_Tide_Subordinate_Data\\Pocasset_River_Entrance_MA\\NOAA_Tidal_HL_2023_PocassetRiverEntrance_GMT.csv"))


# Need to cut out section of NOAA_tidal_data that fits with date range of pco2_section_data
# Program where you input time period to get overlay instead of having a manual overlay? probably

# Cuts out data that do not fit within desired date range
# Input: dataframe, start date in "mm-dd-yyyy", end date in "mm-dd-yyyy"
# Output: dataframe with only data that is within the start and end date
def commonDataRange(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["Date"].tolist()
    for date in logger_dates_list:
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
        date1 = dt(y1, m1, d1)
      
        if not((date1 <= date3) & (date1>= date2)):
            invalid_date_list.append(date)
            invalid_date_index_list.append(logger_date_index)
        else:
            print("bruh it's working?", date)
        logger_date_index += 1
    
    data_df = data_df.drop(invalid_date_index_list)
    data_df = data_df.reset_index()
    data_df = data_df.drop(columns = "index")
    
    return data_df


NOAA_fitted_data = commonDataRange(NOAA_tidal_data, "05-16-2023", "12-02-2023")
print(commonDataRange(NOAA_tidal_data, "05-16-2023", "11-01-2023"))

print("yay, time is done?")

def timeConverterto24(time):
    ending = time.split(" ")[-1]
    time_number = time.split(" ")[0]
    h1, m1, s1 = [int(number) for number in time_number.split(":")]
    if ending == "PM" and h1 != 12:
        h1 += 12
    if ending == "AM" and h1 == 12:
        h1 = 0
    converted_time = str(h1) + ":" + str(m1) + ":" + str(s1)
    converted_time_dt = dt.strptime(converted_time, "%H:%M:%S")
    return converted_time_dt

NOAA_tidal_data_time_converted_list = []
for time in NOAA_fitted_data["Time"]:
    NOAA_tidal_data_time_converted_list.append(timeConverterto24(time))
#print("time", NOAA_tidal_data_time_converted_list)

NOAA_tidal_data_date_converted_list = []
for date in NOAA_fitted_data["Date"]:
    NOAA_tidal_data_date_converted_list.append(dt.strptime(date, "%m/%d/%Y"))
#print("date", NOAA_tidal_data_date_converted_list)


NOAA_tidal_data_datetime_combined_list = []
for index in range(0, len(NOAA_tidal_data_date_converted_list)):
    NOAA_tidal_data_datetime_combined_list.append(dt.combine(NOAA_tidal_data_date_converted_list[index], NOAA_tidal_data_time_converted_list[index].time()))

# Need to add NOAA_tidal_data_datetime_combined_list into NOAA dataframe as "DateTime"
NOAA_fitted_data["DateTime"] = NOAA_tidal_data_datetime_combined_list
print(NOAA_fitted_data)
print("another part done?")

# pCO2 2022 data section is good
hobo_sal = hobo_data["Salinity Value (Offset +15)"]
hobo_date_with_year = hobo_data["Date (UTC)"]
hobo_date_no_year = []
for date in hobo_date_with_year:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    dt_date_no_year_time_shift = dt_date_no_year - datetime.timedelta(hours=3)
    hobo_date_no_year.append(dt_date_no_year_time_shift)


# Need to decipher NOAA data
NOAA_date_with_year = NOAA_fitted_data["DateTime"]
NOAA_date_no_year = []
for date in NOAA_date_with_year:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_no_year.append(dt_date_no_year)


# Decipher NOAA high/low data
# If high, then puts in time to high_list
# If low, then puts in time to low_list
# High_list -> star points?
# Low_list -> triangle points?
    
NOAA_date_high = []
NOAA_date_low = []
NOAA_data_high = []
NOAA_data_low = []
for index in range(0, len(NOAA_date_with_year)):
    type = NOAA_fitted_data.loc[index, "High/Low"]
    if type == "H":
        NOAA_date_high.append(NOAA_fitted_data.loc[index, "DateTime"])
        NOAA_data_high.append(NOAA_fitted_data.loc[index, "Pred(cm)"])
    if type == "L":
        NOAA_date_low.append(NOAA_fitted_data.loc[index, "DateTime"])
        NOAA_data_low.append(NOAA_fitted_data.loc[index, "Pred(cm)"])


NOAA_date_high_revised = []
for date in NOAA_date_high:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_high_revised.append(dt_date_no_year)


NOAA_date_low_revised = []
for date in NOAA_date_low:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_low_revised.append(dt_date_no_year)

print(hobo_data)

fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(hobo_date_no_year, hobo_sal, color = "b", linestyle = 'solid', label = 'HOBO #1 2022 (+15 PSU)', linewidth=0.75)

# Sets x-axis as Dates

date_form = md.DateFormatter("%m-%d %H:%M")
ax1.xaxis.set_major_formatter(date_form)
ax1.set_xticks(NOAA_date_no_year)
plt.xticks(rotation=90)
#ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_minor_locator(md.HourLocator(interval = 1))       # Indicates each day (without label) on x-axis


    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("Salinity (PSU)")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")  

# Graphs NOAA data
ax2 = ax1.twinx()
p2a = ax2.scatter(NOAA_date_high_revised, NOAA_data_high, color = 'g', marker = "*", label = 'Pocasset River Entrance- 2023 High Tide')
p2b = ax2.scatter(NOAA_date_low_revised, NOAA_data_low, color = 'r', marker = "^", label = 'Pocasset River Entrance- 2023 Low Tide')
ax2.set_ylabel("Tide Height (cm)")


# Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("HOBO #1 2022 (-3 Hours) vs Pocasset River Entrance 2023 High/Low Tidal Markers", loc='center')
plt.grid(True)
plt.legend()

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
#plt.savefig(my_path + '\\Conductivity_Graphs\\Comparison_Graphs\\hobo_1_2022_vs_2023_pocasset_tide_offset_test2_time_shift3.png')

plt.show()
