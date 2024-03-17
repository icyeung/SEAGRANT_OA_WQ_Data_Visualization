import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

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

pco2_section_data = pd.read_csv(os.path.join(__location__, "pco2_2022_subsection_oct.csv"))

NOAA_tidal_data = pd.read_csv(os.path.join(__location__, "NOAA_Tidal_HL_2022_Monument_Beach.csv"))


# Need to cut out section of NOAA_tidal_data that fits with date range of pco2_section_data

def timeConverterto24(time):
    ending = time.split(" ")[-1]
    time_number = time.split(" ")[0]
    h1, m1, s1 = [int(number) for number in time_number.split(":")]
    if ending == "PM":
        h1 += 12
    if ending == "AM" and h1 == 12:
        h1 = 0
    converted_time = str(h1) + ":" + str(m1) + ":" + str(s1)
    converted_time_dt = dt.strptime(converted_time, "%H:%M:%S")
    return converted_time_dt

NOAA_tidal_data_time_converted_list = []
for time in NOAA_tidal_data["Time"]:
    NOAA_tidal_data_time_converted_list.append(timeConverterto24(time))

NOAA_tidal_data_date_converted_list = []
for date in NOAA_tidal_data["Date"]:
    NOAA_tidal_data_date_converted_list.append(dt.strptime(date, "%m-%d-%Y"))

NOAA_tidal_data_datetime_combined_list = []
for index in range(0, len(NOAA_tidal_data_date_converted_list)):
    NOAA_tidal_data_datetime_combined_list.append(dt.combine(NOAA_tidal_data_date_converted_list[index], NOAA_tidal_data_time_converted_list[index]))




m2, d2, y2 = [int(date) for date in start_date.split("-")]
date2 = datetime.datetime(y2, m2, d2)

m3, d3, y3 = [int(date) for date in end_date.split("-")]
date3 = datetime.datetime(y3, m3, d3)   

valid_date_list = []
valid_date_index_list = []
logger_date_index = 0

logger_dates_list = logger_df["Date"].tolist()
for date in logger_dates_list:
    m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
    date1 = datetime.datetime(y1, m1, d1)
      
    if ((date1 <= date3) & (date1>= date2)):
        valid_date_list.append(date)
        valid_date_index_list.append(logger_date_index)
    else:
        print("bruh is it working", date)
    logger_date_index += 1



pco2_data = pco2_section_data["CO2"]
pco2_date = pco2_section_data["Date"]
pco2_date_revised = []
for date in pco2_date:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    pco2_date_revised.append(dt_date_no_year)



NOAA_data = NOAA_tidal_data["High/Low"]
temp_2022 = pco2_2022_data["Temperature (C)"]
date_2022 = pco2_2022_data["Date"]
date_2022_revised = []
for date in date_2022:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2022_revised.append(dt_date_no_year)



    # Salinity plot
fig, ax1 = plt.subplots(figsize=(14,7))
p1a = ax1.plot(date_2021_revised, data_2021, color = 'b', linestyle = 'solid', label = '2021', linewidth=0.75)
p1b = ax1.plot(date_2022_revised, data_2022, color = "g", linestyle = 'solid', label = '2022', linewidth=0.75)


    # Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "Salinity" label for easy viewing
ax1.set_ylabel("pCO2")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")  
    
    # Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("pCO2 (2021-2023)", loc='center')
plt.grid(True)
plt.legend(handles=p1a+p1b+p1c)

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\pco2_2021_2023_Graph_No_Outliers.png')

plt.show()
