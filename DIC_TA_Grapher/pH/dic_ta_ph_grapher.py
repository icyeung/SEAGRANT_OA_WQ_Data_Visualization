import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import pytz

# Create graph overlay of water sampling date and pco2 or ph
# y-axis would be total alkalinity/DIC and calculated pco2/ph 
# maybe use 2020 as an example (not 2022 as it has the errors)
# will have to use 2021 as there is no water sample data for HAR besides 2021 


# use data from 2017-2022 mwra
# tco2=dic
# ta
# out vlues are calculated
#Stat_ID = HAR

# Separate DIC, TA, and calculated pH values by location of water sample
# Different colors for same symbol?
# red for top
# green for bottom

# Have small arrow denoting incoming or outgoing tide
# Pointing up for incoming
# Pointing down for outgoing


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

measured_pH_data_df = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Graphing_Across_Years\\pH\\pH_Data_2021_Compiled_Monthly.csv")

MWRA_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv")

MWRA_trunc_df = pd.DataFrame()
MWRA_trunc_df = pd.DataFrame(data=MWRA_trunc_df, columns=MWRA_data.columns)

for index in range(0, len(MWRA_data)):
#print("A:", indexA)
    if ((MWRA_data.loc[index, "STAT_ID"])) == "HAR":
        print("yay the date works")
        new_row = MWRA_data.loc[index].copy()
        MWRA_trunc_df.loc[index] = new_row
        print("yay")


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

    logger_dates_list = data_df["PROF_DATE_TIME_LOCAL"].tolist()
    for date in logger_dates_list:
        date = str(date)
        date = date.split(" ")[0]
        #print(date)
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
        date1 = dt(y1, m1, d1)
      
        if not((date1 <= date3) & (date1>= date2)):
            invalid_date_list.append(date)
            invalid_date_index_list.append(logger_date_index)
        else:
            print("bruh it's working?", date)
        logger_date_index += 1
    
    print("Index to drop:", invalid_date_index_list)
    
    data_df = data_df.reset_index()
    data_df = data_df.drop(invalid_date_index_list)
    
    data_df = data_df.drop(columns = "index")
    
    return data_df

print(MWRA_trunc_df)


MWRA_fitted_data = commonDataRange(MWRA_trunc_df, "01-01-2021", "12-31-2021")
print(MWRA_fitted_data)

print("yay, time is done?")

'''
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
for time in MWRA_fitted_data["Time"]:
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
'''


# pH 2022 data section is good
measured_pH_data = measured_pH_data_df["pH"]
pH_date = measured_pH_data_df["Date"]
pH_date_revised = []
for date in pH_date:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    pH_date_revised.append(dt_date_no_year)




# Need to decipher MWRA data
TA_data = MWRA_fitted_data["TA in (mmol/kgSW)"]
DIC_data = MWRA_fitted_data["TCO2 in (mmol/kgSW)"]
cal_pH_data = MWRA_fitted_data["pH out"]
MWRA_date = MWRA_fitted_data["PROF_DATE_TIME_LOCAL"]
sample_name = MWRA_fitted_data["Station_D"]
MWRA_date_revised = []


revised_MWRA_list = []
for date in MWRA_date:
    time = date.split(" ")[1]
    day = date.split(" ")[0]
    hour = time.split(":")[0]
    minute = time.split(":")[1]
    hour = str(hour)
    if len(hour) == 1:
        hour = "0" + hour
        new_time = hour + ":" + minute
        new_date = day + " " + new_time
        revised_MWRA_list.append(new_date)
    else:
        revised_MWRA_list.append(date)

revised_MWRA_list_GMT = []

utc = pytz.utc
eastern = pytz.timezone('US/Eastern')
fmt = '%m/%d/%Y %H:%M'
for date in revised_MWRA_list:
    date=dt.strptime(date,"%m/%d/%Y %H:%M")
    date_eastern=eastern.localize(date,is_dst=None)
    date_utc=date_eastern.astimezone(utc)
    date_utc = date_utc.replace(tzinfo=None)
    revised_MWRA_list_GMT.append(date_utc)
    
print(revised_MWRA_list_GMT)

for date in revised_MWRA_list_GMT:
    print(date)
    date_no_year = '{:%m-%d %H:%M}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M")
    MWRA_date_revised.append(dt_date_no_year)


fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(pH_date_revised, measured_pH_data, color = "b", linestyle = 'solid', label = 'Measured pH', linewidth=0.75)
p4 = ax1.scatter(MWRA_date_revised, cal_pH_data, color = 'c', marker = "D", label = "Calculated pH")
# Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
#ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("pH")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")
#ax1.legend()  

ax2 = ax1.twinx()
p2 = ax2.scatter(MWRA_date_revised, TA_data, color = 'g', marker = "*", label = 'TA')
ax2.set_ylabel("TA (mmol/kgSW)")
#ax2.legend(loc = 'lower center')

ax3 = ax1.twinx()
p3 = ax3.scatter(MWRA_date_revised, DIC_data, color = 'r', marker = "^", label = "TCO2")
ax3.set_ylabel("TOC2 (mmol/kgSW)")
ax3.spines["right"].set_position(("outward", 60))
#ax3.legend(loc = 'lower center')

'''
handles, labels = ax1.get_legend_handles_labels()
plt.figlegend(handles, labels, loc='upper center')
'''


# Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("pH: Calculated vs Measured (2021)", loc='center')
fig.legend(loc = 'upper center', ncol = 1, borderaxespad=4)
plt.grid(True)

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\ph_calculated_vs_measured_2021_Graph_No_Outliers.png')
plt.show()
