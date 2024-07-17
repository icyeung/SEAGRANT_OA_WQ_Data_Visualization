import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression
import math
import pytz
import datetime


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

NERACOOS_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERACOOS_Data\\NERACOOS_Waquoit_Bay_Data\\NERACOOS_Waquoit_Salinity_2023.csv")

def NERACOOS_time_converter(date_time):
    date = date_time.split(" ")[0]
    #print(date)
    time = date_time.split(" ")[1]
    #print(time)
    y1, m1, d1 = [int(date_part) for date_part in date.split("-")]
    date1 = dt(y1, m1, d1)
    converted_time = dt.strptime(time, "%H:%M:%S")
    return dt.combine(date1, converted_time.time())

neracoos_datetime_list = []
for value in NERACOOS_data["Time-UTC"]:
    neracoos_datetime_list.append(NERACOOS_time_converter(value))


NERACOOS_data["Datetime"] = neracoos_datetime_list


#print(NERACOOS_data)


def commonDataRange_NERACOOS(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    #print(data_df)

    logger_dates_list = data_df["Datetime"].tolist()
    for date in logger_dates_list:
        date = str(date)
        date = date.split(" ")[0]
        #print(date)
        y1, m1, d1 = [int(date_part) for date_part in date.split("-")]
        date1 = dt(y1, m1, d1)
      
        if not((date1 <= date3) & (date1>= date2)):
            invalid_date_list.append(date)
            invalid_date_index_list.append(logger_date_index)
        
        logger_date_index += 1
    
    #print("Index to drop:", invalid_date_index_list)
    
    data_df = data_df.reset_index()
    data_df = data_df.drop(invalid_date_index_list)
    
    data_df = data_df.drop(columns = "index")
    data_df = data_df.reset_index()
    
    return data_df

NERACOOS_fitted_data = commonDataRange_NERACOOS(NERACOOS_data, "01-01-2023", "12-31-2023")
NERACOOS_fitted_data = NERACOOS_fitted_data.reset_index()

print(NERACOOS_fitted_data)


# Graphing
fig, ax1 = plt.subplots(figsize=(14,7))

p1 = ax1.scatter(NERACOOS_fitted_data["Datetime"], NERACOOS_fitted_data["WAXM31m-Hourly-Salinity_psu"], color = 'blue', marker = "o", label = 'NERACOOS Salinity')

# Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 8))     # Displays x-axis label every 14 days
plt.xticks(rotation=90)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 7))       # Indicates each day (without label) on x-axis

ax1.set_xlim([datetime.date(2023, 1, 1), datetime.date(2023, 12, 31)])
ax1.set_ylim(26, 33)
    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_xlabel("Dates (MM-DD)")
ax1.set_ylabel("Salinity (ppt)")
ax1.yaxis.label.set_color("k")  


# Sets title, adds a grid, and shows legend
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("NERACOOS Waquoit Bay (WAXM3) 2023 Salinity Outliers Removed", loc='center')
fig.legend(loc = 'upper left', ncol = 2, borderaxespad=4)


my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\Conductivity_Graphs\\NERACOOS_Graphs\\NERACOOS_Salinity_2023_Waquoit_WAXM3_No_Outliers.png')
plt.show()