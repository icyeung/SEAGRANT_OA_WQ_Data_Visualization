import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# Create graph overlay of water sampling date and pco2 or ph
# y-axis would be total alkalinity/DIC and calculated pco2/ph 
# maybe use 2020 as an example (not 2022 as it has the errors)

# use data from 2017-2022 mwra
# tco2=dic
# ta
# out vlues are calculated


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

pco2_section_data = pd.read_csv(os.path.join(__location__, "pco2_2022_subsection_oct.csv"))

NOAA_tidal_data = pd.read_csv(os.path.join(__location__, "NOAA_Tidal_HL_2022_Monument_Beach.csv"))


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


NOAA_fitted_data = commonDataRange(NOAA_tidal_data, "09-30-2022", "11-01-2022")
print(commonDataRange(NOAA_tidal_data, "09-30-2022", "11-01-2022"))

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
pco2_data = pco2_section_data["CO2"]
pco2_date = pco2_section_data["Date"]
pco2_date_revised = []
for date in pco2_date:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    pco2_date_revised.append(dt_date_no_year)


# Need to decipher NOAA data
NOAA_date = NOAA_fitted_data["DateTime"]
NOAA_date_revised = []
for date in NOAA_date:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_revised.append(dt_date_no_year)


# Decipher NOAA high/low data
# If high, then puts in time to high_list
# If low, then puts in time to low_list
# High_list -> star points?
# Low_list -> triangle points?
    
NOAA_date_high = []
NOAA_date_low = []
NOAA_data_high = []
NOAA_data_low = []
for index in range(0, len(NOAA_date)):
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



fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(pco2_date_revised, pco2_data, color = "b", linestyle = 'solid', label = '2022', linewidth=0.75)

# Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
#ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("pCO2")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")  

# Graphs NOAA data
ax2 = ax1.twinx()
p2a = ax2.scatter(NOAA_date_high_revised, NOAA_data_high, color = 'g', marker = "*", label = 'Monument Beach- High Tide')
p2b = ax2.scatter(NOAA_date_low_revised, NOAA_data_low, color = 'r', marker = "^", label = 'Monument Beach- Low Tide')
ax2.set_ylabel("Tide Height (cm)")
 

# Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("pCO2 & High/Low Tidal Markers (2022)", loc='center')
plt.grid(True)
plt.legend()

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\pco2_tidal_overlay_oct_2022_Graph_No_Outliers.png')

plt.show()
