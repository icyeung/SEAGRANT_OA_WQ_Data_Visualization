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

# NERRS Metoxit Point
nerrs_data = pd.read_csv(os.path.join(__location__, "Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2022_adjusted_UTC+1.csv"))

# Herring River
NOAA_tidal_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Tide_Data\\NOAA_Tide_Subordinate_Data\\Herring_River_MA\\NOAA_Tidal_HL_2022_HerringRiver_GMT.csv"))


# Need to cut out section of NOAA_tidal_data that fits with date range of pco2_section_data
# Program where you input time period to get overlay instead of having a manual overlay? probably

# Cuts out data that do not fit within desired date range
# Input: dataframe, start date in "mm-dd-yyyy", end date in "mm-dd-yyyy"
# Output: dataframe with only data that is within the start and end date
def commonDataRange_NOAA(data_df, start_date, end_date):
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


def commonDataRange_nerrs(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["Datetime_Adjusted_UTC+1"].tolist()
    for date in logger_dates_list:
        dateday = date.split(" ")[0]
        y1, m1, d1 = [int(date_part) for date_part in dateday.split("-")]
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

nerrs_fitted_data = commonDataRange_nerrs(nerrs_data, "10-7-2022", "10-11-2022")

NOAA_fitted_data = commonDataRange_NOAA(NOAA_tidal_data, "10-7-2022", "10-11-2022")
#print(commonDataRange(NOAA_tidal_data, "05-16-2023", "11-01-2020"))

print("yay, time is done?")


nerrs_sal = nerrs_fitted_data["Sal"]
nerrs_date_with_year = nerrs_fitted_data["Datetime_Adjusted_UTC+1"]
nerrs_date_dt = []
for date in nerrs_date_with_year:
    #date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    #date_no_year = str(date_no_year)
    nerrs_dt_date = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
    #dt_date_no_year_time_shift = dt_date_no_year - datetime.timedelta(hours=3)
    nerrs_date_dt.append(nerrs_dt_date)


# Need to decipher NOAA data
NOAA_date_with_year = NOAA_fitted_data["Subordinate DateTime (Adjusted)"]
NOAA_date_dt = []
for date in NOAA_date_with_year:
    #date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    #date_no_year = str(date_no_year)
    NOAA_dt_date = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
    NOAA_date_dt.append(NOAA_dt_date)


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
        NOAA_date_high.append(dt.strptime(NOAA_fitted_data.loc[index, "Subordinate DateTime (Adjusted)"], "%Y-%m-%d %H:%M:%S"))
        NOAA_data_high.append(NOAA_fitted_data.loc[index, "Pred(cm)"])
    if type == "L":
        NOAA_date_low.append(dt.strptime(NOAA_fitted_data.loc[index, "Subordinate DateTime (Adjusted)"], "%Y-%m-%d %H:%M:%S"))
        NOAA_data_low.append(NOAA_fitted_data.loc[index, "Pred(cm)"])


print(nerrs_fitted_data)

fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(nerrs_date_dt, nerrs_sal, color = "b", linestyle = 'solid', label = 'NERRS Metoxit Point 2022', linewidth=0.75)

# Sets x-axis as Dates

date_form = md.DateFormatter("%m-%d %H:%M")
ax1.xaxis.set_major_formatter(date_form)
ax1.set_xticks(NOAA_date_dt)
plt.xticks(rotation=90)
#ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_minor_locator(md.HourLocator(interval = 1))       # Indicates each day (without label) on x-axis


    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("Salinity (PSU)")
ax1.set_xlabel("Dates (MM-DD) UTC")
ax1.yaxis.label.set_color("k")  

# Graphs NOAA data
ax2 = ax1.twinx()
p2a = ax2.scatter(NOAA_date_high, NOAA_data_high, color = 'g', marker = "*", label = 'Herring River- 2022 High Tide')
p2b = ax2.scatter(NOAA_date_low, NOAA_data_low, color = 'r', marker = "^", label = 'Herring River- 2022 Low Tide')
ax2.set_ylabel("Tide Height (cm)")


# Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("NERRS Metoxit Point 2022 vs Herring River 2022 High/Low Tidal Markers", loc='center')
plt.grid(True)
plt.legend()

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\Conductivity_Graphs\\Comparison_Graphs\\nerrs_mp_2022_vs_2022_herringriver_tide_oct.png')

plt.show()