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
import time

def NERRS_sal_grapher(nerrs_file_location, mwra_file, hobo_file, date_start, date_end, trunc_date_start, trunc_date_end, title, file_save_location):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    NERRS_data = pd.read_csv(nerrs_file_location)

    # Converts string time stamps from LST to GMT/UTC
    def NERRS_time_converter(date_time):
        
        date = date_time.split(" ")[0]
        #print(date)
        time = date_time.split(" ")[1]
        #print(time)
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
        date1 = dt(y1, m1, d1)
        converted_time = dt.strptime(time, "%H:%M")
        datetime_dt_est = dt.combine(date1, converted_time.time())

        datetime_dt_utc = datetime_dt_est + datetime.timedelta(hours=5)

        return datetime_dt_utc

    nerrs_datetime_list = []
    for value in NERRS_data["DateTimeStamp"]:
        nerrs_datetime_list.append(NERRS_time_converter(value))

    NERRS_data["Datetime"] = nerrs_datetime_list

    def commonDataRange_NERRS(data_df, start_date, end_date):
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
    #print(NERACOOS_data)

    NERRS_fitted_data = commonDataRange_NERRS(NERRS_data, date_start, date_end)
    NERRS_fitted_data = NERRS_fitted_data.reset_index()
    NERRS_fitted_data.to_csv("test_nerrs.csv")
    print(NERRS_fitted_data)

    mwra_raw_datetime_list = []
    mwra_salinity_list = []
    numofLinesS = 0
    with open(os.path.join(__location__, mwra_file),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:

            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[0] == "" and not row[1] == "" and numofLinesS > 0:
                mwra_raw_datetime_list.append(row[0])
                mwra_salinity_list.append(float(row[1]))
                numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1


    # MWRA is stored as LST, added 5 hours for now (but will need to account for daylight saving)
    def timeConverterto24(datetime1):
        time_number = datetime1.split(" ")[1]
        converted_time_dt = dt.strptime(time_number, "%H:%M:%S")
        datetime_mwra_dt_utc = converted_time_dt + datetime.timedelta(hours=5)
        return datetime_mwra_dt_utc

    MWRA_data_time_converted_list = []
    for time in mwra_raw_datetime_list:
        MWRA_data_time_converted_list.append(timeConverterto24(time))
    #print("time", NOAA_tidal_data_time_converted_list)

    MWRA_data_date_converted_list = []    
    for date in mwra_raw_datetime_list:
        MWRA_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%Y-%m-%d"))
    #print("date", NOAA_tidal_data_date_converted_list)

    if len(MWRA_data_date_converted_list) == len(MWRA_data_time_converted_list):
        print("yayyyyy, everything works fine so far")
    else:
        print("Oops", "date", len(MWRA_data_date_converted_list), "time", len(MWRA_data_time_converted_list))

    print(MWRA_data_date_converted_list)


    MWRA_data_datetime_combined_list = []
    for index in range(0, len(MWRA_data_date_converted_list)):
        MWRA_data_datetime_combined_list.append(dt.combine(MWRA_data_date_converted_list[index], MWRA_data_time_converted_list[index].time()))

    MWRA_df = pd.DataFrame({"DateTime": MWRA_data_datetime_combined_list, "Salinity": mwra_salinity_list})




    # Hobo
    def Hobo_df(file_name_hobo):

        hobo_raw_datetime_list = []
        hobo_salinity_list = []
        numofLinesS = 0
        with open(os.path.join(__location__, hobo_file),'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:

                # Checks if time entry has corresponding Time and Verified Measurement
                # If not, does not include data point in graph
                if not row[1] == "" and not row[2] == "" and numofLinesS > 0:
                    hobo_raw_datetime_list.append(row[1])
                    hobo_salinity_list.append(float(row[2]))
                    numofLinesS += 1
                elif numofLinesS <= 0:
                    numofLinesS += 1


        # MWRA is stored as LST, added 5 hours for now (but will need to account for daylight saving)
        def timeConverterto24(datetime1):
            time_number_with_offset = datetime1.split(" ")[1]
            time_number = time_number_with_offset.split("-")[0]
            converted_time_dt = dt.strptime(time_number, "%H:%M:%S")
            datetime_hobo_dt_utc = converted_time_dt + datetime.timedelta(hours=4)
            return datetime_hobo_dt_utc

        hobo_data_time_converted_list = []
        for time in hobo_raw_datetime_list:
            hobo_data_time_converted_list.append(timeConverterto24(time))
        #print("time", NOAA_tidal_data_time_converted_list)

        hobo_data_date_converted_list = []    
        for date in hobo_raw_datetime_list:
            hobo_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%Y-%m-%d"))
        #print("date", NOAA_tidal_data_date_converted_list)

        if len(hobo_data_date_converted_list) == len(hobo_data_time_converted_list):
            print("yayyyyy, everything works fine so far")
        else:
            print("Oops", "date", len(hobo_data_date_converted_list), "time", len(hobo_data_time_converted_list))

        print(hobo_data_date_converted_list)


        hobo_data_datetime_combined_list = []
        for index in range(0, len(hobo_data_date_converted_list)):
            hobo_data_datetime_combined_list.append(dt.combine(hobo_data_date_converted_list[index], hobo_data_time_converted_list[index].time()))

        hobo_df = pd.DataFrame({"DateTime": hobo_data_datetime_combined_list, "Salinity": hobo_salinity_list})
        
        return hobo_df

    hobo_sal_df = Hobo_df(hobo_file)
    print(hobo_sal_df)


    # Graphing
    fig, ax1 = plt.subplots(figsize=(14,7))

    p1 = ax1.scatter(NERRS_fitted_data["Datetime"], NERRS_fitted_data["Sal"], 5, color = 'blue', marker = "o", label = 'NERRS')
    
    #ax2 = ax1.twinx()
    p2 = ax1.scatter(MWRA_df["DateTime"], MWRA_df["Salinity"], color = "red", label = 'MWRA', linewidth=0.75, marker = "x")

    p3 = ax1.plot(hobo_sal_df["DateTime"], hobo_sal_df["Salinity"], 5, color = "green", label = 'HOBO')

    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 8))     # Displays x-axis label every 14 days
    plt.xticks(rotation=90)
    #ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 7))       # Indicates each day (without label) on x-axis

    ax1.set_xlim([trunc_date_start, trunc_date_end])
    # ax1.set_ylim(26, 33)
        
    # Sets axis labels 
    ax1.set_xlabel("Dates (MM-DD)")
    ax1.set_ylabel("Salinity (ppt)")
    ax1.yaxis.label.set_color("k")  


    # Sets title, adds a grid, and shows legend
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper left', ncol = 2, borderaxespad=4)


    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves without outliers graph to specified name in folder
    plt.savefig(my_path + file_save_location)
    plt.show()

'''
# Sage Lot 2021
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2021.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2021_data.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) vs MWRA Harwich Bottle 2021 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Sage_Lot_vs_MWRA_Harwich_Salinity_2021.png')

# Sage Lot 2022
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2022.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2022_data.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) vs MWRA Harwich Bottle 2022 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Sage_Lot_vs_MWRA_Harwich_Salinity_2022.png')
# Menauhant 2021
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2021.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2021_data.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) vs MWRA Harwich Bottle 2021 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Menauhant_vs_MWRA_Harwich_Salinity_2021.png')
'''

# Menauhant 2022
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2022.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2022_data.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Harwich_8-16-22_2_NO.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) vs MWRA Harwich Bottle vs HOBO 2022 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Menauhant_vs_MWRA_Harwich_Salinity_vs_HOBO_2022.png')
'''
# Metoxit Point 2021
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Metoxit_Point\\wqbmpwq2021.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2021_data.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) vs MWRA Harwich Bottle 2021 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Metoxit_Point_vs_MWRA_Harwich_Salinity_2021.png')
'''
# Metoxit Point 2022
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Metoxit_Point\\wqbmpwq2022.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2022_data.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Harwich_8-16-22_2_NO.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) vs MWRA Harwich Bottle vs HOBO 2022 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Metoxit_Point_vs_MWRA_Harwich_Salinity_vs_HOBO_2022.png')
'''
# Childs River 2021
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2021.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2021_data.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Childs River) vs MWRA Harwich Bottle 2021 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Childs_River_vs_MWRA_Harwich_Salinity_2021.png')

# Childs River 2022
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2022.csv",
                  "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\Formatted_MWRA_HAR_2022_data.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Childs River) vs MWRA Harwich Bottle 2022 Salinity',
                  '\\Conductivity_Graphs\\Comparison_Graphs\\NERRS_Childs_River_vs_MWRA_Harwich_Salinity_2022.png')
'''