# As compared with BBC Data for Pocasset (see IY's pCO2 Grapher slides for more info), HOBO #1 data 2022 will be offset by +15 PSU and used for 2022.
# For 2023, HOBO #1 offset by -3 hours and +15 PSU will be used for 2023.

import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import math
import datetime
import pytz
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression
from datetime import datetime as dt


# Used to find location of specified file within Python code folder
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


hobo_data = pd.read_csv(os.path.join(__location__, 'HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Pocasset_12-9-22_1_NO.csv'))

offset_sal_val_list = []
for sal_val in hobo_data["Salinity Value"]:
    offset_sal_val = sal_val + 15
    offset_sal_val_list.append(offset_sal_val)

hobo_data["Salinity Value (Offset +15)"] = offset_sal_val_list


# HOBO is stored as LST, added 4/5 hours to convert to UTC
def timeConvertertoUTC(datetime1):
    time_number_with_offset = datetime1.split(" ")[1]
    time_number = time_number_with_offset.split("-")[0]
    offset_value = time_number_with_offset.split("-")[1]
    converted_time_dt = dt.strptime(time_number, "%H:%M:%S")
    converted_date_dt = dt.strptime((date.split(" ")[0]), "%Y-%m-%d")
    combined_datetime_dt = dt.combine(converted_date_dt, converted_time_dt.time())
    if offset_value == "04:00":
        datetime_hobo_dt_utc = combined_datetime_dt + datetime.timedelta(hours=4)
    elif offset_value == "05:00":
        datetime_hobo_dt_utc = combined_datetime_dt + datetime.timedelta(hours=5)
    return datetime_hobo_dt_utc

'''
hobo_data_time_converted_list = []
for time in hobo_data["Date"]:
    hobo_data_time_converted_list.append(timeConverterto24(time))
   #print("time", NOAA_tidal_data_time_converted_list)

hobo_data_date_converted_list = []    
for date in hobo_data["Date"]:
    hobo_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%Y-%m-%d"))
    #print("date", NOAA_tidal_data_date_converted_list)

if len(hobo_data_date_converted_list) == len(hobo_data_time_converted_list):
    print("yayyyyy, everything works fine so far")
else:
    print("Oops", "date", len(hobo_data_date_converted_list), "time", len(hobo_data_time_converted_list))

#print(hobo_data_date_converted_list)
'''

hobo_data_datetime_combined_list = []
for date in hobo_data["Date"]:
    hobo_data_datetime_combined_list.append(timeConvertertoUTC(date))

hobo_data["Date (UTC)"] = hobo_data_datetime_combined_list

hobo_data_datetime_utc_offset_list = []
for date_utc in hobo_data["Date (UTC)"]:
    if date_utc.year == 2022:
        date_utc_offset = date_utc - datetime.timedelta(hours = 3)
        hobo_data_datetime_utc_offset_list.append(date_utc_offset)

hobo_data["Date (UTC) Offset -3 Hours"] = hobo_data_datetime_utc_offset_list


hobo_data = hobo_data.drop('Unnamed: 0', axis=1)

print(hobo_data)

hobo_data.to_csv(os.path.join(__location__, 'HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Pocasset_12-9-22_1_NO_offset_all.csv'), index=None)

print(len(hobo_data["Date (UTC)"]))
print(len(hobo_data["Salinity Value (Offset +15)"]))

#print(hobo_data_datetime_combined_list)

fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(hobo_data["Date (UTC)"], hobo_data["Salinity Value (Offset +15)"], color = 'b', label = 'Salinity (ppt)', linewidth = 0.75)

# Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    
# Sets axis labels and changes font color of "Salinity" label for easy viewing
ax1.set_ylabel("Salinity (ppt)")
ax1.set_xlabel("Dates (MM-DD) UTC")
   
#plt.subplots_adjust(top=0.95)
plt.title("HOBO 1 2022 Pocasset Salinity (Offset +15 PSU)", loc='center')
plt.grid(True)
plt.legend()

plt.savefig(__location__ + '\\Conductivity_Graphs\\HOBO_Graphs\\Conductivity_12-9-22_1_Graph_Without_Outliers_Offset_Sal.png')


plt.show()