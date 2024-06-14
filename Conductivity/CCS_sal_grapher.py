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

NOAA_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\NOAA_Tidal_Data\\NOAA_Tidal_HL_2022_Boston_GMT.csv", delimiter=",")

CCS_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Center_for_Coastal_Studies_Salinity_Harwich_Data\\station_124.csv")

def CCS_time_converter(date_time):
    date = date_time.split("T")[0]
    time = date_time.split("T")[1]
    time = time[:-5]
    print(time)
    y1, m1, d1 = [int(date_part) for date_part in date.split("-")]
    date1 = dt(y1, m1, d1)
    converted_time = dt.strptime(time, "%H:%M:%S")
    return dt.combine(date1, converted_time.time())

ccs_datetime_list = []
for value in CCS_data["collected_at"]:
    ccs_datetime_list.append(CCS_time_converter(value))


CCS_data["Datetime"] = ccs_datetime_list


#print(CCS_data)


def commonDataRange_CCS(data_df, start_date, end_date):
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

CCS_fitted_data = commonDataRange_CCS(CCS_data, "01-01-2014", "12-31-2022")
CCS_fitted_data = CCS_fitted_data.reset_index()

'''
def commonDataRange_NOAA(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    #print(data_df)

    logger_dates_list = data_df["Date"].tolist()
    for date in logger_dates_list:
        date = str(date)
        date = date.split(" ")[0]
        #print(date)
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
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

NOAA_fitted_data = commonDataRange_NOAA(NOAA_data, "02-10-2022", "10-06-2022")

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
'''

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
#print(NOAA_fitted_data)
print("another part done?")
#print(NOAA_fitted_data)

NOAA_fitted_data["DateTime (Corrected)"] = np.nan



for index in range(0, len(NOAA_fitted_data)):
    tide_type = NOAA_fitted_data.loc[index, "High/Low"]
    if tide_type == "H":
        date = NOAA_fitted_data.loc[index, "DateTime"]
        time_change = datetime.timedelta(minutes = 68)
        date_corrected = date + time_change
        NOAA_fitted_data.loc[index, "DateTime (Corrected)"] = date_corrected
    if tide_type == "L":
        date = NOAA_fitted_data.loc[index, "DateTime"]
        time_change = datetime.timedelta(minutes = 45)
        date_corrected = date + time_change
        NOAA_fitted_data.loc[index, "DateTime (Corrected)"] = date_corrected

print(NOAA_fitted_data)
print(CCS_fitted_data)

'''

tide_type_list = []
tide_graphing_index = 0
tide_graphing_df = pd.DataFrame(columns=["Datetime", "Tide Heights"])
for date in CCS_fitted_data["Datetime"]:
    date = str(date)
    #print(date)
    
    date_num = date.split(" ")[0]
    '''
    print("num", date_num)
    y2, m2, d2 = [int(date) for date in date_num.split("-")]
    print(d2)
    date_num = dt(m2, d2, y2)

    date_num = date_num.replace("/", "-")
    

    date_num = '{:%m-%d-%Y}'.format(dt.strptime(date_num, '%Y-%m-%d'))
    date_num = str(date_num)
    #date_num = dt.strptime(date_num, "%m-%d-%Y")

    #print(date_num)

    #NOAA_tide_day_data_df = commonDataRange_NOAA(NOAA_fitted_data, date_num, date_num)
    time_num = date.split(" ")[1]
    #print('time num', time_num)
    NOAA_time_list = NOAA_tide_day_data_df["Time"]
    #print("NOAA time list", NOAA_time_list)
    index = 0

    NOAA_tide_day_data_df = NOAA_tide_day_data_df.drop(columns = "index")
    NOAA_tide_day_data_df = NOAA_tide_day_data_df.reset_index()

    #print("here", NOAA_tide_day_data_df)
    tide_type = ""
    
    while (index+1) < len(NOAA_time_list):
        #print("tide index", index)
        #print("hi")
        #print(time_num)
        if time_num > str(NOAA_tide_day_data_df.loc[index, "DateTime"]).split(" ")[1] and time_num < str(NOAA_tide_day_data_df.loc[index+1, "DateTime"]).split(" ")[1]:
            start_type = NOAA_tide_day_data_df.loc[index, "High/Low"]
            #print("start type", start_type)
            end_type = NOAA_tide_day_data_df.loc[index+1, "High/Low"]
            #print("end type", end_type)

            tide_graphing_df.loc[tide_graphing_index, "Datetime"] = NOAA_tide_day_data_df.loc[index, "DateTime"]
            tide_graphing_df.loc[tide_graphing_index, "Tide Heights"] = NOAA_tide_day_data_df.loc[index, "Pred(cm)"]
            tide_graphing_index += 1
            tide_graphing_df.loc[tide_graphing_index, "Datetime"] = NOAA_tide_day_data_df.loc[index+1, "DateTime"]
            tide_graphing_df.loc[tide_graphing_index, "Tide Heights"] = NOAA_tide_day_data_df.loc[index+1, "Pred(cm)"]
            tide_graphing_index += 1


            if start_type == "H" and end_type == "L":
                tide_type = "outgoing"
                tide_type_list.append(tide_type)
            if start_type == "L" and end_type == "H":
                tide_type = "incoming"
                tide_type_list.append(tide_type)
            break
        elif time_num == NOAA_tide_day_data_df.loc[index, "Time"]:
            tide_type = NOAA_tide_day_data_df.loc[index, "High/Low"]
            tide_type_list.append(tide_type)
            break
        elif time_num < str(NOAA_tide_day_data_df.loc[index, "DateTime"]).split(" ")[1]:
            if NOAA_tide_day_data_df.loc[index, "High/Low"] == "H":
                tide_type = "incoming"
                tide_type_list.append(tide_type)
                break
            if NOAA_tide_day_data_df.loc[index, "High/Low"] == "L":
                tide_type = "outgoing"
                tide_type_list.append(tide_type)
                break
        elif (index+2)==len(NOAA_time_list) and time_num > str(NOAA_tide_day_data_df.loc[index+1, "DateTime"]).split(" ")[1]:
            if NOAA_tide_day_data_df.loc[index+1, "High/Low"] == "H":
                tide_type = "outgoing"
                tide_type_list.append(tide_type)
                break
            if NOAA_tide_day_data_df.loc[index+1, "High/Low"] == "L":
                tide_type = "incoming"
                tide_type_list.append(tide_type)
                break
        else:
            index += 1
        #print("tide type", tide_type)
    

#print(tide_type_list)
print("list", CCS_fitted_data)
print("tide", tide_type_list)


incoming_time_list = []
incoming_list = []
outgoing_time_list = []
outgoing_list = []
high_time_list = []
high_list = []
low_time_list = []
low_list = []



for tidal_index in range(0, len(tide_type_list)):
    if tide_type_list[tidal_index] == "incoming":
        incoming_time_list.append(CCS_fitted_data.loc[tidal_index, "Datetime"])
        #print(MWRA_date_revised[index])
        incoming_list.append(0.05)
    elif tide_type_list[tidal_index] == "outgoing":
        outgoing_time_list.append(CCS_fitted_data.loc[tidal_index, "Datetime"])
        #print(MWRA_date_revised[index])
        outgoing_list.append(0.05)
    elif tide_type_list[tidal_index] == "H":
        high_time_list.append(CCS_fitted_data.loc[tidal_index, "Datetime"])
        high_list.append(0.05)
    elif tide_type_list[tidal_index] == "L":
        low_time_list.append(CCS_fitted_data.loc[tidal_index, "Datetime"])
        low_list.append(0.05)

#print("in", incoming_time_list)
#print("out", outgoing_time_list)


print("tide", tide_graphing_df)

'''

# Graphing
fig, ax1 = plt.subplots(figsize=(14,7))
#p1 = ax1.plot(NOAA_fitted_data["DateTime (Corrected)"], NOAA_fitted_data["Pred(cm)"], color = "y", linestyle = 'solid', label = 'NOAA Tide Height- Herring River', linewidth=0.75)
#p2 = ax1.plot(tide_graphing_df["Datetime"], tide_graphing_df["Tide Heights"], color = "b", linestyle = 'solid', label = "NOAA Tide Height- Herring River", linewidth = 0.75)

# Sets x-axis as Dates
date_form = DateFormatter("%m-%Y")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 16))     # Displays x-axis label every 14 days
plt.xticks(rotation=90)
#ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
# Sets axis labels and changes font color of "pco2" label for easy viewing
#ax1.set_ylabel("Tidal Height (cm)")
ax1.set_xlabel("Dates (MM-YYYY)")
ax1.yaxis.label.set_color("k")
#ax1.legend()  

#ax2 = ax1.twinx()
#p2 = ax2.scatter(bottom_date_GMT, bottom_TA_data, color = 'darkviolet', marker = "*", label = 'TA- Bottom Sample')
#p6 = ax2.scatter(top_date_GMT, top_TA_data, color = 'fuchsia', marker = "*", label = 'TA- Top Sample')
p13 = ax1.scatter(CCS_fitted_data["Datetime"], CCS_fitted_data["salinity"], color = 'red', marker = "*", label = 'CCS Salinity')
ax1.set_ylabel("Salinity (ppt)")
#ax2.legend(loc = 'lower center')


#ax4 = ax1.twinx()
#p8 = ax4.scatter(incoming_time_list, incoming_list, color = "k", marker = "+", label = "Incoming Tide- Herring River")
#p9 = ax4.scatter(outgoing_time_list, outgoing_list, color = "k", marker = "_", label = "Outgoing Tide- Herring River")
#p10 = ax4.scatter(high_time_list, high_list, color = "green", marker = 6, label = "High Tide")
#p11 = ax4.scatter(low_time_list, low_list, color = "green", marker = 7, label = "Low Tide")
#ax4.set_ylim([0, 5])
#ax4.yaxis.set_visible(False)

'''
handles, labels = ax1.get_legend_handles_labels()
plt.figlegend(handles, labels, loc='upper center')
'''

# Sets title, adds a grid, and shows legend
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("CCS Harwich (Herring River-Station 124) Salinity 2014-2022", loc='center')
fig.legend(loc = 'upper left', ncol = 2, borderaxespad=4)


my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\CCS_Salinity_2014_2022_Harwich.png')
plt.show()