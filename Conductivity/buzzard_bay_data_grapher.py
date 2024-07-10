import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

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

def buzzard_bay_grapher(file, station, title, start_date, end_date, year):

    numofLinesS = 0
    raw_date_list = []
    raw_time_list = []
    temp_list = []
    salinity_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, file),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            #print(row)
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[1] == "" and not row[3] == "" and not row[10] == "" and not row[19] == "" and not row[21] == "" and numofLinesS > 0:
                if row[1] == station:
                    print("hi")
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

    print(BB_data_date_converted_list)


    BB_data_datetime_combined_list = []
    for index in range(0, len(BB_data_date_converted_list)):
        BB_data_datetime_combined_list.append(dt.combine(BB_data_date_converted_list[index], BB_data_time_converted_list[index].time()))

    BB_df = pd.DataFrame({"DateTime": BB_data_datetime_combined_list, "Temperature": temp_list, "Salinity": salinity_list})

    fig, ax1 = plt.subplots(figsize=(14,7))
    p1 = ax1.plot(BB_df["DateTime"], BB_df["Salinity"], color = "b", linestyle = 'solid', label = 'Salinity', linewidth=0.75)
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

    ax2 = ax1.twinx()
    p13 = ax2.plot(BB_df["DateTime"], BB_df["Salinity"], color = 'g', linestyle = 'solid', label = 'Temperature')
    ax2.set_ylabel("Temperature (C)")
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper center', ncol = 3, borderaxespad=4)


    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves without outliers graph to specified name in folder
    plt.savefig(my_path + '\\BB_' + station + '_' + year + '.png')
    plt.show()


#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) 2021", "1/1/2021", "12/31/2021", "2021")

#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2022", "1/1/2022", "12/31/2022", "2022")

#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2023", "1/1/2023", "12/31/2023", "2023")

buzzard_bay_grapher("bbcdata1992to2020-ver07May2021.csv", "CI1", "Buzzard's Bay Salinity: CI1 2021", "1/1/2021", "12/31/2021", "2021")
