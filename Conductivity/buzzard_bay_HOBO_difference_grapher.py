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

# saves csv as dataframe
# sorts by station
# checks start date & end date
# if there is no valid start or end date, uses entire time frame
# 

def commonDataRange(date, start_date, end_date):
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

def buzzard_bay_grapher(file, station, title, start_date, end_date, year, HOBO_file1, HOBO_file2, HOBO_file3, HOBO_file4):

    numofLinesS = 0
    raw_date_list = []
    raw_time_list = []
    temp_list = []
    salinity_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    file_BB = "Buzzards_Bay_Data\\" + file

    with open(os.path.join(__location__, file_BB),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            #print(row)
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[1] == "" and not row[3] == "" and not row[10] == "" and not row[19] == "" and not row[21] == "" and numofLinesS > 0:
                if row[1] == station:
                    #print("hi")
                    if commonDataRange(row[3], start_date, end_date):
                        raw_date_list.append(row[3])
                        raw_time_list.append(row[10])
                        temp_list.append(float(row[19]))
                        salinity_list.append(float(row[21]))
                        numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1
    
    print(raw_date_list)

    def timeConverterto24(time):
        ending = time.split(" ")[-1]
        time_number = time.split(" ")[0]
        h1, m1 = [int(number) for number in time_number.split(":")]
        if ending == "PM" and h1 != 12:
            h1 += 12
        if ending == "AM" and h1 == 12:
            h1 = 0
        converted_time = str(h1) + ":" + str(m1)
        converted_time_dt = dt.strptime(converted_time, "%H:%M")
        return converted_time_dt

    BB_data_time_converted_list = []
    for time in raw_time_list:
        BB_data_time_converted_list.append(timeConverterto24(time))
    #print("time", NOAA_tidal_data_time_converted_list)

    BB_data_date_converted_list = []    
    for date in raw_date_list:
        BB_data_date_converted_list.append(dt.strptime(date, "%m/%d/%Y"))
    #print("date", NOAA_tidal_data_date_converted_list)

    if len(BB_data_date_converted_list) == len(BB_data_time_converted_list):
        print("yayyyyy")
    else:
        print("OOps", "date", len(BB_data_date_converted_list), "time", len(BB_data_time_converted_list))

    #print(BB_data_date_converted_list)


    BB_data_datetime_combined_list = []
    for index in range(0, len(BB_data_date_converted_list)):
        BB_data_datetime_combined_list.append(dt.combine(BB_data_date_converted_list[index], BB_data_time_converted_list[index].time()))

    BB_df = pd.DataFrame({"DateTime": BB_data_datetime_combined_list, "Temperature": temp_list, "Salinity": salinity_list})
    
    HOBO_1_part1 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file1), delimiter=",")

    HOBO_1_part2 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file2), delimiter=",")

    HOBO_2_part1 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file3), delimiter=",")

    HOBO_2_part2 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file4), delimiter=",")

    def convertTime(df):
        graphingTime = []
        for date in df["Date"]:
            dateNew = date[:-6]
            print(dateNew)
            graphingTime.append(dateNew)
        df["Date (Corrected)"] = graphingTime
        return(df)

    HOBO_1_part1_fx = convertTime(HOBO_1_part1)
    #print(HOBO_1_part1_fx)
    HOBO_1_part2_fx = convertTime(HOBO_1_part2)
    HOBO_2_part1_fx = convertTime(HOBO_2_part1)
    HOBO_2_part2_fx = convertTime(HOBO_2_part2)
    
    HOBO1_data_time_converted_list = []
    for date in HOBO_1_part1["Date (Corrected)"]:
        #print(HOBO_file1)
        #print("hi", date)
        HOBO1_data_time_converted_list.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_1_part1_fx["Date (DT)"] = HOBO1_data_time_converted_list

    '''
    HOBO2_data_time_converted_list = []
    for date in HOBO_2_part1["Date (Corrected)"]:
        #print(HOBO_file1)
        print("hi", date)
        HOBO2_data_time_converted_list.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_2_part1_fx["Date (DT)"] = HOBO2_data_time_converted_list

    HOBO1_data_time_converted_list_2 = []
    for date in HOBO_1_part2["Date (Corrected)"]:
        #print(HOBO_file1)
        print("hi", date)
        HOBO1_data_time_converted_list_2.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_1_part2_fx["Date (DT)"] = HOBO1_data_time_converted_list_2

    HOBO2_data_time_converted_list_2 = []
    for date in HOBO_2_part2["Date (Corrected)"]:
        #print(HOBO_file1)
        print("hi", date)
        HOBO2_data_time_converted_list_2.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_2_part2_fx["Date (DT)"] = HOBO2_data_time_converted_list_2
    '''

    print(BB_df)

    
    chosen_datetimes = []
    BB_datetimes = []
    for indexA in range(0, len(BB_df)):
        possible_times = []
        possible_times_index = []
        BB_date = (BB_df.loc[indexA, "DateTime"]).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]
        BB_time = (BB_df.loc[indexA, "DateTime"]).strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]

        for indexB in range(0, len(HOBO_1_part1_fx)):
            HOBO_date = (HOBO_1_part1_fx.loc[indexB, "Date (DT)"]).strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]
            HOBO_time = (HOBO_1_part1_fx.loc[indexB, "Date (DT)"]).strftime("%Y-%m-%d %H:%M:%S").split(" ")[1]

            #print(HOBO_time)

            if BB_date == HOBO_date:
                possible_times.append(HOBO_date + " " + HOBO_time)
                possible_times_index.append(indexB)

        if possible_times != []:
            BB_time_hour = int(BB_time.split(":")[0])
            BB_time_minute = int(BB_time.split(":")[1])
            BB_time_min_percent = round(BB_time_minute/60, 4)
            BB_time_conv = float(BB_time_hour + BB_time_min_percent)
            difference_list = []
            
            for HOBO_time_date in possible_times:
                HOBO_time_time = HOBO_time_date.split(" ")[1]
                HOBO_time_hour = int(HOBO_time_time.split(":")[0])
                HOBO_time_minute = int(HOBO_time_time.split(":")[1])
                HOBO_time_min_percent = round(HOBO_time_minute/60, 4)
                HOBO_time_conv = float(HOBO_time_hour + HOBO_time_min_percent)
                
                difference = abs(float(BB_time_conv-HOBO_time_conv))         
                difference_list.append(difference)

            # Chooses file with minimum time difference
            min_time_diff = min(difference_list)
            min_time_diff_index = difference_list.index(min_time_diff)
            opt_time = possible_times[min_time_diff_index]
            chosen_date = str(opt_time)
            chosen_datetimes.append(chosen_date)
            BB_datetimes.append(BB_date + " " + BB_time)

        print("HOBO list", chosen_datetimes)
        print(len(chosen_datetimes))
        print("BB list", BB_datetimes)
        print(len(BB_datetimes))

    HOBO_common_date_index_list = []
    for date1 in chosen_datetimes:
        HOBO_common_date_index = HOBO_1_part1_fx.loc[HOBO_1_part1_fx["Date (DT)"] == date1].index[0]
        HOBO_common_date_index_list.append(HOBO_common_date_index)
    
    print(HOBO_common_date_index_list)

    BB_common_date_index_list = []
    for date2 in BB_datetimes:
        BB_common_date_index = BB_df.loc[BB_df["DateTime"] == date2].index[0]
        BB_common_date_index_list.append(BB_common_date_index)

    print(BB_common_date_index_list)

    sal_diff_list = []
    for indexCommon in range(0, len(BB_common_date_index_list)):
        HOBO_salinity = HOBO_1_part1_fx.loc[HOBO_common_date_index_list[indexCommon], "Salinity Value"]
        BB_salinity = BB_df.loc[BB_common_date_index_list[indexCommon], "Salinity"]
        sal_diff = HOBO_salinity - BB_salinity
        sal_diff_list.append(sal_diff)

    chosen_datetime_time_converted_list = []
    for date in chosen_datetimes:
        #print(HOBO_file1)
        #print("hi", date)
        chosen_datetime_time_converted_list.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))

    fig, ax1 = plt.subplots(figsize=(14,7))
    #p1 = ax1.plot(BB_df["DateTime"], BB_df["Salinity"], color = "g", linestyle = 'solid', label = 'BB', linewidth=0.75)
    #p2 = ax1.plot(HOBO_1_part1_fx["Date (DT)"], HOBO_1_part1_fx["Salinity Value"], color = 'b', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
    p3 = ax1.plot(chosen_datetime_time_converted_list, sal_diff_list, color = 'b', linestyle = '-', label = "Difference Between HOBO #1 and BB", linewidth = 0.75)
    #p3 = ax1.plot(HOBO_2_part1_fx["Date (DT)"], HOBO_2_part1_fx["Salinity Value"], color = 'r', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
    #p4 = ax1.plot(HOBO_1_part2_fx["Date (DT)"], HOBO_1_part2_fx["Salinity Value"], color = 'cyan', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
    #p5 = ax1.plot(HOBO_2_part2_fx["Date (DT)"], HOBO_2_part2_fx["Salinity Value"], color = 'orange', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
    #ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "pco2" label for easy viewing
    ax1.set_ylabel("Salinity (%.)")
    ax1.set_xlabel("Dates (MM-DD)")
    ax1.yaxis.label.set_color("k")
    #ax1.legend()  

    #ax2 = ax1.twinx()
    #p13 = ax2.plot(BB_df["DateTime"], BB_df["Salinity"], color = 'g', linestyle = 'solid', label = 'Temperature')
    #ax2.set_ylabel("Temperature (C)")
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper right', ncol = 3, borderaxespad=4)


    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves without outliers graph to specified name in folder
    #plt.savefig(my_path + '\\BB_vs_HOBO_' + station + '_' + year + '.png')
    plt.show()



buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) vs HOBO 2021", "1/1/2021", "12/31/2021", "2021", "Salinity_Carolina_FiddlersCove_9-28-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")

#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2022", "1/1/2022", "12/31/2022", "2022", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")

#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2023", "1/1/2023", "12/31/2023", "2023", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")


