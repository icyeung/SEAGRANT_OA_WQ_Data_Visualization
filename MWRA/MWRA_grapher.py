# STAT_ID = "HAR"; index = 2
# PROF_DATE_TIME_LOCAL column; index = 9 
# could have a time variable for sectioning what to graph
# SAL (PSU) column; index = 19

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


def commonDataRange(datetime, start_date, end_date):

    date = datetime.split(" ")[0]

    m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
    date1 = dt(y1, m1, d1)
    
    m2, d2, y2 = [int(date) for date in start_date.split("/")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("/")]
    date3 = dt(y3, m3, d3)       
      
    if (date1 <= date3) & (date1>= date2):
        return True
    else:
        return False

def mwra_grapher(file, station, title, start_date, end_date, year):

    numofLinesS = 0
    raw_datetime_list = []
    salinity_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, file),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:

            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[2] == "" and not row[9] == "" and not row[19] == "" and numofLinesS > 0:
                if row[2] == station:
                    if commonDataRange(row[9], start_date, end_date):
                        raw_datetime_list.append(row[9])
                        salinity_list.append(float(row[19]))
                        numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1
    
    #print(raw_datetime_list)

    def timeConverterto24(datetime):
        time_number = datetime.split(" ")[1]
        h1, m1 = [int(number) for number in time_number.split(":")]
        converted_time = str(h1) + ":" + str(m1)
        converted_time_dt = dt.strptime(converted_time, "%H:%M")
        return converted_time_dt

    MWRA_data_time_converted_list = []
    for time in raw_datetime_list:
        MWRA_data_time_converted_list.append(timeConverterto24(time))
    #print("time", NOAA_tidal_data_time_converted_list)

    MWRA_data_date_converted_list = []    
    for date in raw_datetime_list:
        MWRA_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%m/%d/%Y"))
    #print("date", NOAA_tidal_data_date_converted_list)

    if len(MWRA_data_date_converted_list) == len(MWRA_data_time_converted_list):
        print("yayyyyy, everything works fine so far")
    else:
        print("Oops", "date", len(MWRA_data_date_converted_list), "time", len(MWRA_data_time_converted_list))

    print(MWRA_data_date_converted_list)


    MWRA_data_datetime_combined_list = []
    for index in range(0, len(MWRA_data_date_converted_list)):
        MWRA_data_datetime_combined_list.append(dt.combine(MWRA_data_date_converted_list[index], MWRA_data_time_converted_list[index].time()))

    MWRA_df = pd.DataFrame({"DateTime": MWRA_data_datetime_combined_list, "Salinity": salinity_list})

    fig, ax1 = plt.subplots(figsize=(14,7))
    p1 = ax1.scatter(MWRA_df["DateTime"], MWRA_df["Salinity"], color = "b", label = 'Salinity', linewidth=0.75)
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d-%Y")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=90)

    # Sets axis labels
    ax1.set_ylabel("Salinity (%.)")
    ax1.set_xlabel("Dates (MM-DD-YYYY)")
    ax1.yaxis.label.set_color("k")
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper center', ncol = 3, borderaxespad=4)

    my_path = os.path.dirname(os.path.abspath(__file__))
    #plt.savefig(my_path + '\\MWRA_Graphs\\MWRA_' + station + '_' + year + '.png')

    # Used for graphing in NERRS vs bottle sal grapher (found in Conductivity folder)
    # Clean data formatting with only datetime and salinity
    MWRA_df.to_csv(my_path + '\\Formatted_MWRA_' + station + '_' + year + '_data.csv', index=False)

    plt.show()

# Graphs all Harwich water samples from 2021-2022
#mwra_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv", "HAR", "MWRA 2021-2022 Bottle Samples (Harwich)", "01/01/2021", "12/31/2022", "2021-2022")

# Graphs Harwich water samples from 2021
mwra_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv", "HAR", "MWRA 2021 Bottle Samples (Harwich)", "01/01/2021", "12/31/2021", "2021")

# Graphs Harwich water samples from 2022
mwra_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv", "HAR", "MWRA 2022 Bottle Samples (Harwich)", "01/01/2022", "12/31/2022", "2022")