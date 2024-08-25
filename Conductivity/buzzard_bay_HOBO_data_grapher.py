import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
import datetime
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



def buzzard_bay_HOBO_grapher(bbc_file, station, title, start_date, end_date, year, HOBO_file1, HOBO_file2, HOBO_file3, HOBO_file4, showSurface, showDeep):

    numofLinesS = 0
    raw_date_surface_list = []
    raw_time_surface_list = []
    depth_surface_list = []
    temp_surface_list = []
    salinity_surface_list = []

    raw_date_deep_list = []
    raw_time_deep_list = []
    depth_deep_list = []
    temp_deep_list = []
    salinity_deep_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    file_BB = "Sourced_Data\\Buzzards_Bay_Coalition_Data\\" + bbc_file

    with open(os.path.join(__location__, file_BB),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            #print(row)
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[1] == "" and not row[3] == "" and not row[5] == "" and not row[10] == "" and not row[19] == "" and not row[21] == "" and row[30] == "" and numofLinesS > 0:
                if row[1] == station:
                    if commonDataRange(row[3], start_date, end_date):
                        if row[5].split("-")[6] == "S":
                            raw_date_surface_list.append(row[3])
                            raw_time_surface_list.append(row[10])
                            depth_surface_list.append(row[13])
                            temp_surface_list.append(float(row[19]))
                            salinity_surface_list.append(float(row[21])-4)
                            numofLinesS += 1
                        if row[5].split("-")[6] == "D":
                            raw_date_deep_list.append(row[3])
                            raw_time_deep_list.append(row[10])
                            depth_deep_list.append(row[13])
                            temp_deep_list.append(float(row[19]))
                            salinity_deep_list.append((float(row[21])))
            elif numofLinesS <= 0:
                numofLinesS += 1
    
    

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


    # Surface depth measurements
    BB_data_time_surface_converted_list = []
    for time in raw_time_surface_list:
        BB_data_time_surface_converted_list.append(timeConverterto24(time))

    BB_data_date_surface_converted_list = []    
    for date in raw_date_surface_list:
        BB_data_date_surface_converted_list.append(dt.strptime(date, "%m/%d/%Y"))

    '''
    if len(BB_data_date_surface_converted_list) == len(BB_data_time_surface_converted_list):
        print("surface- yayyyyy")
    else:
        print("surface- OOps", "date", len(BB_data_date_surface_converted_list), "time", len(BB_data_time_surface_converted_list))
    '''

    #print(BB_data_date_surface_converted_list)


    BB_data_datetime_surface_combined_list = []
    for index in range(0, len(BB_data_date_surface_converted_list)):
        datetime_surface_lst = dt.combine(BB_data_date_surface_converted_list[index], BB_data_time_surface_converted_list[index].time())
        datetime_surface_utc = datetime_surface_lst + datetime.timedelta(hours=6)
        BB_data_datetime_surface_combined_list.append(datetime_surface_utc)

    #Deep depth measurements
    BB_data_time_deep_converted_list = []
    for time in raw_time_deep_list:
        BB_data_time_deep_converted_list.append(timeConverterto24(time))


    BB_data_date_deep_converted_list = []    
    for date in raw_date_deep_list:
        BB_data_date_deep_converted_list.append(dt.strptime(date, "%m/%d/%Y"))

    '''
    if len(BB_data_date_deep_converted_list) == len(BB_data_time_deep_converted_list):
        print("deep- yayyyyy")
    else:
        print("deep- OOps", "date", len(BB_data_date_deep_converted_list), "time", len(BB_data_time_deep_converted_list))
    '''

    #print(BB_data_date_deep_converted_list)

    BB_data_datetime_deep_combined_list = []
    for index in range(0, len(BB_data_date_deep_converted_list)):
        datetime_deep_lst = dt.combine(BB_data_date_deep_converted_list[index], BB_data_time_deep_converted_list[index].time())
        datetime_deep_utc = datetime_deep_lst + datetime.timedelta(hours=6)
        BB_data_datetime_deep_combined_list.append(datetime_deep_utc)


    BB_surface_df = pd.DataFrame({"DateTime (LST+4)": BB_data_datetime_surface_combined_list, "Temperature": temp_surface_list, "Salinity": salinity_surface_list})
    
    BB_deep_df = pd.DataFrame({"DateTime (LST+4)": BB_data_datetime_deep_combined_list, "Temperature": temp_deep_list, "Salinity": salinity_deep_list})

    
    #NOAA Tide
    # To determine H/L:
    # Obtains list of dates and time
    # Separates date and time 
    # If date matches, creates list of times on that date
    # Uses searcher function on time list
    # Once time is determined, 
    # If "High/Low" is H for time before and L for time after, tide is outgoing (CARETDOWN)
    # If "High/Low" is L for time before and H for time after, tide is incoming (CARETUP)

    def commonDataRange_NOAA(data_loc, start_date, end_date):
        m2, d2, y2 = [int(date) for date in start_date.split("-")]
        date2 = dt(y2, m2, d2)

        m3, d3, y3 = [int(date) for date in end_date.split("-")]
        date3 = dt(y3, m3, d3)   

        invalid_date_list = []
        invalid_date_index_list = []
        logger_date_index = 0


        data_df = pd.read_csv(data_loc)

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
                break
            logger_date_index += 1
        
        #print("Index to drop:", invalid_date_index_list)
        
        data_df = data_df.reset_index()
        data_df = data_df.drop(invalid_date_index_list)
        
        data_df = data_df.drop(columns = "index")
        
        return data_df

    def tide_extractor(NOAA_file, list):
        incoming_time_list = []
        incoming_list = []
        outgoing_time_list = []
        outgoing_list = []
        high_time_list = []
        high_list = []
        low_time_list = []
        low_list = []
        tide_type_list = []
        for date in list:
            date = str(date)
            #print(date)
            
            date_num = date.split(" ")[0]
            
            print("num", date_num)
            y2, m2, d2 = [int(date) for date in date_num.split("-")]
            print(d2)
            date_num = dt(m2, d2, y2)

            date_num = date_num.replace("/", "-")
            

            date_num = '{:%m-%d-%Y}'.format(dt.strptime(date_num, '%Y-%m-%d'))
            date_num = str(date_num)
            #date_num = dt.strptime(date_num, "%m-%d-%Y")

            NOAA_tide_day_data_df = commonDataRange_NOAA(NOAA_file, date_num, date_num)
            time_num = date.split(" ")[1]
            NOAA_time_list = NOAA_tide_day_data_df["Time"]
            index = 0

            NOAA_tide_day_data_df = NOAA_tide_day_data_df.reset_index()
            while index+1 < len(NOAA_time_list):
                if time_num > NOAA_tide_day_data_df.loc[index, "Time"] and time_num < NOAA_tide_day_data_df.loc[index+1, "Time"]:
                    start_type = NOAA_tide_day_data_df.loc[index, "High/Low"]
                    end_type = NOAA_tide_day_data_df.loc[index+1, "High/Low"]
                    if start_type == "H" and end_type == "L":
                        tide_type = "outgoing"
                    if start_type == "L" and end_type == "H":
                        tide_type = "incoming"
                    break
                elif time_num == NOAA_tide_day_data_df.loc[index, "Time"]:
                    tide_type = NOAA_tide_day_data_df.loc[index, "High/Low"]
                    break
                else:
                    index += 1
            tide_type_list.append(tide_type)

            print("BBC Sample Time", date, "   |Previous Tide", NOAA_tide_day_data_df.loc[index, "Time"], "   |Next Tide", NOAA_tide_day_data_df.loc[index+1, "Time"], tide_type)

        #print(tide_type_list)
        #print("list", list)

        for tidal_index in range(0, len(tide_type_list)):
            if tide_type_list[tidal_index] == "incoming":
                incoming_time_list.append(list[tidal_index])
                #print(list[index])
                incoming_list.append(0.05)
            elif tide_type_list[tidal_index] == "outgoing":
                outgoing_time_list.append(list[tidal_index])
                #print(list[index])
                outgoing_list.append(0.05)
            elif tide_type_list[tidal_index] == "H":
                high_time_list.append(list[tidal_index])
                high_list.append(0.05)
            elif tide_type_list[tidal_index] == "L":
                low_time_list.append(list[tidal_index])
                low_list.append(0.05)

        tide_in_out_tuple = [incoming_time_list, incoming_list, outgoing_time_list, outgoing_list, high_time_list, high_list, low_time_list, low_list]
        return tide_in_out_tuple

    if station == "PR1":
        surface_tide_df = tide_extractor("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Comparisons_Different_Parameters\\DIC_TA_Grapher\\pCO2\\Tidal_Data\\NOAA_Tidal_HL_2022_Piney_Point_GMT_v2.csv", BB_data_datetime_surface_combined_list)
        deep_tide_df = tide_extractor("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Comparisons_Different_Parameters\\DIC_TA_Grapher\\pCO2\\Tidal_Data\\NOAA_Tidal_HL_2022_Piney_Point_GMT_v2.csv", BB_data_datetime_deep_combined_list)
    
    if station == "FC1X":
        surface_tide_df = tide_extractor()
        deep_tide_df = tide_extractor()


    # HOBO
    HOBO_1_part1 = pd.read_csv(os.path.join(__location__, "HOBO_Data\\Conductivity_Data_No_Outliers\\" + HOBO_file1), delimiter=",")

    HOBO_1_part2 = pd.read_csv(os.path.join(__location__, "HOBO_Data\\Conductivity_Data_No_Outliers\\" + HOBO_file2), delimiter=",")

    HOBO_2_part1 = pd.read_csv(os.path.join(__location__, "HOBO_Data\\Conductivity_Data_No_Outliers\\" + HOBO_file3), delimiter=",")

    HOBO_2_part2 = pd.read_csv(os.path.join(__location__, "HOBO_Data\\Conductivity_Data_No_Outliers\\" + HOBO_file4), delimiter=",")

    def convertTime(df):
        graphingTime = []
        for date in df["Date"]:
            dateNew = date[:-6]
            #print(dateNew)
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
        date_dt_edt = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_dt_utc = date_dt_edt + datetime.timedelta(hours=4) # Converts time to UTC
        HOBO1_data_time_converted_list.append(date_dt_utc)
    HOBO_1_part1_fx["Date (DT-UTC)"] = HOBO1_data_time_converted_list

    
    HOBO2_data_time_converted_list = []
    for date in HOBO_2_part1["Date (Corrected)"]:
        #print(HOBO_file1)
        #print("hi", date)
        date_dt_edt = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_dt_utc = date_dt_edt + datetime.timedelta(hours=4) # Converts time to UTC
        HOBO2_data_time_converted_list.append(date_dt_utc)
    HOBO_2_part1_fx["Date (DT-UTC)"] = HOBO2_data_time_converted_list

    HOBO1_data_time_converted_list_2 = []
    for date in HOBO_1_part2["Date (Corrected)"]:
        #print(HOBO_file1)
        #print("hi", date)
        date_dt_edt = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_dt_utc = date_dt_edt + datetime.timedelta(hours=4) # Converts time to UTC
        HOBO1_data_time_converted_list_2.append(date_dt_utc)
    HOBO_1_part2_fx["Date (DT-UTC)"] = HOBO1_data_time_converted_list_2

    HOBO2_data_time_converted_list_2 = []
    for date in HOBO_2_part2["Date (Corrected)"]:
        #print(HOBO_file1)
        #print("hi", date)
        date_dt_edt = dt.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_dt_utc = date_dt_edt + datetime.timedelta(hours=4) # Converts time to UTC
        HOBO2_data_time_converted_list_2.append(date_dt_utc)
    HOBO_2_part2_fx["Date (DT-UTC)"] = HOBO2_data_time_converted_list_2
    

    print(len(BB_surface_df))
    print(len(BB_deep_df))

    fig, ax1 = plt.subplots(figsize=(14,7))
    if showSurface == True:
        p1 = ax1.plot(BB_surface_df["DateTime (LST+4)"], BB_surface_df["Salinity"], marker = "o", color = "g", label = 'BBC Surface (Offset by -4PSU)', linewidth=0.75)
    if showDeep ==  True:
        p6 = ax1.plot(BB_deep_df["DateTime (LST+4)"], BB_deep_df["Salinity"], marker = "o", color = "k", label = 'BBC Deep', linewidth=0.75)

    
    if station == "PR1":
        p2 = ax1.plot(HOBO_1_part1_fx["Date (DT-UTC)"], HOBO_1_part1_fx["Salinity Value"], color = 'b', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
        p3 = ax1.plot(HOBO_2_part1_fx["Date (DT-UTC)"], HOBO_2_part1_fx["Salinity Value"], color = 'r', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
    if station == "FC1X":
        p2 = ax1.plot(HOBO_1_part1_fx["Date (DT-UTC)"], HOBO_1_part1_fx["Salinity Value"], color = 'b', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
        p3 = ax1.plot(HOBO_2_part1_fx["Date (DT-UTC)"], HOBO_2_part1_fx["Salinity Value"], color = 'r', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
        p4 = ax1.plot(HOBO_1_part2_fx["Date (DT-UTC)"], HOBO_1_part2_fx["Salinity Value"], color = 'cyan', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
        p5 = ax1.plot(HOBO_2_part2_fx["Date (DT-UTC)"], HOBO_2_part2_fx["Salinity Value"], color = 'orange', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
    
        
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
    #ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "pco2" label for easy viewing
    ax1.set_ylabel("Salinity (%.)")
    ax1.set_xlabel("Dates (MM-DD) UTC")
    ax1.yaxis.label.set_color("k")
    #ax1.legend()  

    #ax2 = ax1.twinx()
    #p13 = ax2.plot(BB_df["DateTime"], BB_df["Salinity"], color = 'g', linestyle = 'solid', label = 'Temperature')
    #ax2.set_ylabel("Temperature (C)")
    '''
    ax4 = ax1.twinx()
    p8 = ax4.scatter(surface_tide_df[0], surface_tide_df[1], color = "k", marker = "+", label = "Incoming Tide- Piney Point")
    p9 = ax4.scatter(deep_tide_df[0], deep_tide_df[1], color = "k", marker = "+", label = "Incoming Tide- Piney Point")
    p10 = ax4.scatter(surface_tide_df[2], surface_tide_df[3], color = "k", marker = "_", label = "Outgoing Tide- Piney Point")
    p11 = ax4.scatter(deep_tide_df[2], deep_tide_df[3], color = "k", marker = "_", label = "Outgoing Tide- Piney Point")
    #p12 = ax4.scatter(high_time_list, high_list, color = "green", marker = 6, label = "High Tide")
    #p13 = ax4.scatter(low_time_list, low_list, color = "green", marker = 7, label = "Low Tide")
    ax4.set_ylim([0, 5])
    ax4.yaxis.set_visible(False)
    '''

    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper right', ncol = 3, borderaxespad=4)
    plt.grid(True)


    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves without outliers graph to specified name in folder
    plt.savefig(my_path + '\\Conductivity_Graphs\\Comparison_Graphs\\BB_vs_HOBO_' + station + '_' + year + '_no_flags' + '_depth_sep_with_tide_BBC_offset' +'.png')
    plt.show()



buzzard_bay_HOBO_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) vs HOBO 2021", "1/1/2021", "12/31/2021", "2021", "Salinity_Carolina_FiddlersCove_9-28-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv", True, True)

#buzzard_bay_HOBO_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2022", "1/1/2022", "12/31/2022", "2022", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_Pocasset_6-2-22_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv", True, True)

#buzzard_bay_HOBO_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2023", "1/1/2023", "12/31/2023", "2023", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")

#buzzard_bay_HOBO_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2023", "1/1/2023", "12/31/2023", "2023", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_Pocasset_6-2-22_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv", True, True)

#buzzard_bay_HOBO_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2021-2023", "1/1/2021", "12/31/2023", "2023", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_Pocasset_6-2-22_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv", True, True)
