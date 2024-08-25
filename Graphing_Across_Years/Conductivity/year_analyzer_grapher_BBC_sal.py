import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import statistics

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

def buzzard_bay_grapher(bbc_file_location, station, title, start_date, end_date, year, showSurface, showDeep):

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
    
    

    with open((bbc_file_location),'r') as csvfile:
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


    dataset_mean_surface_sal = statistics.mean(salinity_surface_list)

    mean_surface_list = []
    for index in range(0, len(BB_data_date_surface_converted_list)):
        mean_surface_list.append(dataset_mean_surface_sal)


    dataset_mean_deep_sal = statistics.mean(salinity_deep_list)

    mean_deep_list = []
    for index in range(0, len(BB_data_date_deep_converted_list)):
        mean_deep_list.append(dataset_mean_deep_sal)

    
    fig, ax1 = plt.subplots(figsize=(20,9))

    if showSurface == True:
        p1 = ax1.plot(BB_surface_df["DateTime (LST+4)"], BB_surface_df["Salinity"], "-o", color = "b", label = 'Salinity- Surface', linewidth = 0.85)
        p2 = ax1.plot(BB_surface_df["DateTime (LST+4)"], mean_surface_list, color = "r", label = "year " + station + " Surface Average", linewidth = 1.2)

    if showDeep == True:
        p3 = ax1.plot(BB_deep_df["DateTime (LST+4)"], BB_deep_df["Salinity"], "-o", color = "g", label = 'Salinity- Deep', linewidth = 0.85)
        p4 = ax1.plot(BB_deep_df["DateTime (LST+4)"], mean_deep_list, color = "purple", label = "year " + station + " Deep Average", linewidth = 1.2)
    
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%Y")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 4))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.MonthLocator(interval = 1))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=90)
    
    # Sets axis labels and changes font color of "Salinity" label for easy viewing
    ax1.set_ylabel("Salinity (%.)")
    ax1.set_xlabel("Dates (MM-YYYY)")
    ax1.yaxis.label.set_color("k")
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    #ax1.legend()  

    '''
    # Temperature
    ax2 = ax1.twinx()
    p13 = ax2.plot(BB_df["DateTime"], BB_df["Temperature"], "-o", color = 'g', label = 'Temperature')
    ax2.set_ylabel("Temperature (C)")
    '''
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper right')
    

    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves without outliers graph to specified name in folder
    plt.savefig(my_path + '\\Graphs\\BB_' + station + '_' + year + '_Sal_no_flags_depth_sep.png')
    plt.show()


#buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) 2021", "1/1/2021", "12/31/2021", "2021")

#buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2022", "1/1/2022", "12/31/2022", "2022")

#buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2023", "1/1/2023", "12/31/2023", "2023")

#buzzard_bay_grapher("\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "CI1", "Buzzard's Bay Salinity: CI1 2021", "1/1/2021", "12/31/2021", "2021")

#buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 1992-2023 (No Flags)", "1/1/1992", "12/31/2023", "1992-2023", True, True)

#buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) 1992-2023 (No Flags)", "1/1/1992", "12/31/2023", "1992-2023", True, True)

#buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2021-2023 (No Flags)", "1/1/2021", "12/31/2023", "2021-2023", True, True)

buzzard_bay_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) 2021-2023 (No Flags)", "1/1/2021", "12/31/2023", "2021-2023", True, True)
