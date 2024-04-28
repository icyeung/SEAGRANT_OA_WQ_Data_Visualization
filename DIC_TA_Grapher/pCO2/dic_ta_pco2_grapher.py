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

measured_pCO2_data_df = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Graphing_Across_Years\\pCO2\\pco2_2022_Total_Data_Compiled_Monthly.csv")

MWRA_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv")

NOAA_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\DIC_TA_Grapher\\pCO2\\Tidal_Data\\NOAA_Tidal_HL_2022_Monument_Beach_GMT.csv", delimiter=",")

MWRA_trunc_df = pd.DataFrame()
MWRA_trunc_df = pd.DataFrame(data=MWRA_trunc_df, columns=MWRA_data.columns)

# Obtains desired data for location
for index in range(0, len(MWRA_data)):
#print("A:", indexA)
    if ((MWRA_data.loc[index, "STAT_ID"])) == "POC":
        print("yay the date works")
        new_row = MWRA_data.loc[index].copy()
        MWRA_trunc_df.loc[index] = new_row
        print("yay")


# Cuts out data that do not fit within desired date range
# Input: dataframe, start date in "mm-dd-yyyy", end date in "mm-dd-yyyy"
# Output: dataframe with only data that is within the start and end date
def commonDataRange_MWRA(data_df, start_date, end_date):
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

# Obtains desired time frame from MWRA data
MWRA_fitted_data = commonDataRange_MWRA(MWRA_trunc_df, "01-01-2022", "12-31-2022")
print(MWRA_fitted_data)

def commonDataRange_NOAA(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    print(data_df)

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
        else:
            print("bruh it's working?", date)
        logger_date_index += 1
    
    #print("Index to drop:", invalid_date_index_list)
    
    data_df = data_df.reset_index()
    data_df = data_df.drop(invalid_date_index_list)
    
    data_df = data_df.drop(columns = "index")
    
    return data_df

NOAA_fitted_data = commonDataRange_NOAA(NOAA_data, "01-01-2022", "12-31-2022")

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

print(MWRA_fitted_data)

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



# pH 2021 data section is good
# converts pH date to mm/dd format by dropping year
measured_pCO2_data = measured_pCO2_data_df["CO2"]
pCO2_date = measured_pCO2_data_df["Date"]
pCO2_date_revised = []
for date in pCO2_date:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    pCO2_date_revised.append(dt_date_no_year)




# Need to decipher MWRA data
TA_data = MWRA_fitted_data["TA in (mmol/kgSW)"]
DIC_data = MWRA_fitted_data["TCO2 in (mmol/kgSW)"]
cal_pCO2_data = MWRA_fitted_data["pCO2 out (matm)"]
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


# Create new dataframe with the above lists
# Go through all bottle names using index for range(0, len(dataframe))
# If bottle name.split("-")[1][0] == "b" or "d", then adds that index to bottom_list
# If bottle name.split("-")[1][0] == "s", then adds that index to top_list

# Goes through dataframe for each list and the index is used to obtain the cells for the columns
# Graphs accordingly

processed_MWRA_fitted_df = pd.DataFrame({"PROF_DATE_TIME_LOCAL": MWRA_date, "GMT_Time": MWRA_date_revised, "Station_D": sample_name, "pCO2 out (matm)": cal_pCO2_data, "TA in (mmol/kgSW)": TA_data, "TCO2 in (mmol/kgSW)": DIC_data})

print(processed_MWRA_fitted_df)

bottom_list = []
top_list = []
mid_list = []
bottom_df = pd.DataFrame(columns = processed_MWRA_fitted_df.columns, dtype=str)
print("b", bottom_df)
top_df = pd.DataFrame(columns = processed_MWRA_fitted_df.columns, dtype=str)
print("t", top_df)
mid_df = pd.DataFrame(columns = processed_MWRA_fitted_df.columns, dtype=str)
print("m", mid_df)
bottom_index = 0
top_index = 0
mid_index = 0
for index in range(0, len(processed_MWRA_fitted_df["Station_D"])):
    bottle_name = processed_MWRA_fitted_df.loc[index, "Station_D"]
    if bottle_name.split("-")[1][0] == "b" or bottle_name.split("-")[1][0] == "d":
        bottom_list.append(index)
        new_row_bottom = processed_MWRA_fitted_df.loc[index].copy()
        bottom_df.loc[bottom_index] = new_row_bottom
        bottom_index += 1
    if bottle_name.split("-")[1][0] == 's':
        top_list.append(index)
        new_row_top = processed_MWRA_fitted_df.loc[index].copy()
        top_df.loc[top_index] = new_row_top
        top_index += 1
    else:
        mid_list.append(index)
        new_row_mid = processed_MWRA_fitted_df.loc[index].copy()
        mid_df.loc[mid_index] = new_row_mid
        mid_index += 1


# bottom_df = processed_MWRA_fitted_df.iloc[bottom_list, :]
# top_df = processed_MWRA_fitted_df.iloc[top_df, :]

print("bottom water samples", bottom_df)
print("top water samples", top_df)
print("mid water samples", mid_df)

bottom_date_GMT = bottom_df["GMT_Time"]
bottom_cal_pCO2_data = bottom_df["pCO2 out (matm)"]
bottom_TA_data = bottom_df["TA in (mmol/kgSW)"]
bottom_DIC_data = bottom_df["TCO2 in (mmol/kgSW)"]

top_date_GMT = top_df["GMT_Time"]
top_cal_pCO2_data = top_df["pCO2 out (matm)"]
top_TA_data = top_df["TA in (mmol/kgSW)"]
top_DIC_data = top_df["TCO2 in (mmol/kgSW)"]

mid_date_GMT = mid_df["GMT_Time"]
mid_cal_pCO2_data = mid_df["pCO2 out (matm)"]
mid_TA_data = mid_df["TA in (mmol/kgSW)"]
mid_DIC_data = mid_df["TCO2 in (mmol/kgSW)"]


# To determine H/L:
# Obtains list of dates and time
# Separates date and time 
# If date matches, creates list of times on that date
# Uses searcher function on time list
# Once time is determined, 
# If "High/Low" is H for time before and L for time after, tide is outgoing (CARETDOWN)
# If "High/Low" is L for time before and H for time after, tide is incoming (CARETUP)

incoming_time_list = []
incoming_list = []
outgoing_time_list = []
outgoing_list = []
high_time_list = []
high_list = []
low_time_list = []
low_list = []
tide_type_list = []

print("tide list", revised_MWRA_list_GMT)

for date in revised_MWRA_list_GMT:
    date = str(date)
    #print(date)
    
    date_num = date.split(" ")[0]
    '''
    print("num", date_num)
    y2, m2, d2 = [int(date) for date in date_num.split("-")]
    print(d2)
    date_num = dt(m2, d2, y2)

    date_num = date_num.replace("/", "-")
    '''

    date_num = '{:%m-%d-%Y}'.format(dt.strptime(date_num, '%Y-%m-%d'))
    date_num = str(date_num)
    #date_num = dt.strptime(date_num, "%m-%d-%Y")

    NOAA_tide_day_data_df = commonDataRange_NOAA(NOAA_fitted_data, date_num, date_num)
    time_num = date.split(" ")[1]
    print('time num', time_num)
    NOAA_time_list = NOAA_tide_day_data_df["Time"]
    print("NOAA time list", NOAA_time_list)
    index = 0

    NOAA_tide_day_data_df = NOAA_tide_day_data_df.reset_index()

    print(NOAA_tide_day_data_df)
    tide_type = ""
    while (index+1) < len(NOAA_time_list):
        print("tide index", index)
        print("hi")
        print(time_num)
        if time_num > str(NOAA_tide_day_data_df.loc[index, "DateTime"]).split(" ")[1] and time_num < str(NOAA_tide_day_data_df.loc[index+1, "DateTime"]).split(" ")[1]:
            start_type = NOAA_tide_day_data_df.loc[index, "High/Low"]
            print("start type", start_type)
            end_type = NOAA_tide_day_data_df.loc[index+1, "High/Low"]
            print("end type", end_type)
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
        print("tide type", tide_type)
    

print(tide_type_list)
print("list", MWRA_date_revised)

for tidal_index in range(0, len(tide_type_list)):
    if tide_type_list[tidal_index] == "incoming":
        incoming_time_list.append(MWRA_date_revised[tidal_index])
        print(MWRA_date_revised[index])
        incoming_list.append(0.05)
    elif tide_type_list[tidal_index] == "outgoing":
        outgoing_time_list.append(MWRA_date_revised[tidal_index])
        print(MWRA_date_revised[index])
        outgoing_list.append(0.05)
    elif tide_type_list[tidal_index] == "H":
        high_time_list.append(MWRA_date_revised[tidal_index])
        high_list.append(0.05)
    elif tide_type_list[tidal_index] == "L":
        low_time_list.append(MWRA_date_revised[tidal_index])
        low_list.append(0.05)

print("in", incoming_time_list)
print("out", outgoing_time_list)



# Graphing
fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(pCO2_date_revised, measured_pCO2_data, color = "b", linestyle = 'solid', label = 'Measured pCO2', linewidth=0.75)
#p4 = ax1.scatter(bottom_date_GMT, bottom_cal_pCO2_data, color = 'olivedrab', marker = "D", label = "Calculated pCO2- Bottom Sample", zorder=3)
#p5 = ax1.scatter(top_date_GMT, top_cal_pCO2_data, color = 'greenyellow', marker = "D", label = "Calculated pCO2- Top Sample", zorder=3)
p12 = ax1.scatter(mid_date_GMT, mid_cal_pCO2_data, color = 'teal', marker = "D", label = "Calculated pCO2- Middle Sample", zorder=3)
# Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
#ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("pCO2 (matm)")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")
#ax1.legend()  

ax2 = ax1.twinx()
#p2 = ax2.scatter(bottom_date_GMT, bottom_TA_data, color = 'darkviolet', marker = "*", label = 'TA- Bottom Sample')
#p6 = ax2.scatter(top_date_GMT, top_TA_data, color = 'fuchsia', marker = "*", label = 'TA- Top Sample')
p13 = ax2.scatter(mid_date_GMT, mid_TA_data, color = 'violet', marker = "*", label = 'TA- Middle Sample')
ax2.set_ylabel("TA (mmol/kgSW)")
#ax2.legend(loc = 'lower center')

ax3 = ax1.twinx()
#p3 = ax3.scatter(bottom_date_GMT, bottom_DIC_data, color = 'maroon', marker = "^", label = "TCO2- Bottom Sample")
#p7 = ax3.scatter(top_date_GMT, top_DIC_data, color = 'salmon', marker = "^", label = "TCO2- Top Sample")
p14 = ax3.scatter(mid_date_GMT, mid_DIC_data, color = 'orangered', marker = "^", label = "TCO2- Middle Sample")
ax3.set_ylabel("TOC2 (mmol/kgSW)")
ax3.spines["right"].set_position(("outward", 60))
#ax3.legend(loc = 'lower center')

ax4 = ax1.twinx()
p8 = ax4.scatter(incoming_time_list, incoming_list, color = "k", marker = "+", label = "Incoming Tide- Monument Beach")
p9 = ax4.scatter(outgoing_time_list, outgoing_list, color = "k", marker = "_", label = "Outgoing Tide- Monument Beach")
#p10 = ax4.scatter(high_time_list, high_list, color = "green", marker = 6, label = "High Tide")
#p11 = ax4.scatter(low_time_list, low_list, color = "green", marker = 7, label = "Low Tide")
ax4.set_ylim([0, 5])
ax4.yaxis.set_visible(False)

'''
handles, labels = ax1.get_legend_handles_labels()
plt.figlegend(handles, labels, loc='upper center')
'''


# Sets title, adds a grid, and shows legend
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("pCO2: Calculated vs Measured (2022)", loc='center')
fig.legend(loc = 'upper center', ncol = 3, borderaxespad=4)


my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\pco2_calculated_vs_measured_2022_Monument_Beach_Graph_No_Outliers.png')
plt.show()
