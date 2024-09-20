# Program is used to remove outliers from Eureka Salinity Data
# The conditons for classifying a point as an outlier is as follows:
# Any value of 0 or -999 or an extreme like those is an outlier
# For every point, the difference between two consecutive points must not be more than 5 PSU on both sides
# -If the difference on one side is greater than 5 PSU, but not the other, it will not be counted as an outlier
# -Stop in break of time frame must not be greater than 2 hours

import pandas as pd
import os
from datetime import datetime as dt
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import math

def timeWithinRange (time_a, time_b):
    delta = time_a-time_b
    print(delta.total_seconds())
    if delta.total_seconds() <= 7200:
        print("hi")
        return True
    else:
        return False

def NERRS_outlier_remover(file_name, location):
    #__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    #raw_data_folder = os.path.join(__location__, '')
    #raw_data_location_folder = os.path.join(raw_data_folder, location)

    #adjusted_data_folder = os.path.join(__location__, '')

    # Opens NERRS raw data file
    NERRS_data = pd.read_csv(location)
    
    # Goes through entire NERRS data file
    # For each point (index):
    
    
    print("before before", NERRS_data)

    # Removes first and last 5 data points
    initial_row_drop_list_p1 = [0,1,2,3,4,(len(NERRS_data)-5),(len(NERRS_data)-4),(len(NERRS_data)-3),(len(NERRS_data)-2),(len(NERRS_data)-1)]
    if len(NERRS_data) > 10:
        NERRS_data = NERRS_data.drop(initial_row_drop_list_p1)
    NERRS_data = NERRS_data.reset_index()


    # Removes all 0s and NaN values before points are compared
    initial_row_drop_list_p2 = []
    for index in range(1, len(NERRS_data)):
        salinity = NERRS_data.loc[index, "Sal"]
        if math.isnan(salinity):
            initial_row_drop_list_p2.append(index)
        if not(math.isnan(salinity)):
            if int(salinity) == 0.0:
                initial_row_drop_list_p2.append(index)
    NERRS_data = NERRS_data.drop(initial_row_drop_list_p2)
    #NERRS_data = NERRS_data.drop("level_0", axis=1)
    NERRS_data = NERRS_data.reset_index()
    
    print("what", NERRS_data)

    # Holds all row indices with outliers
    row_drop_list = []

    for index in range(1, len(NERRS_data)-1):
        print("--------------------------------")
        date_current = NERRS_data.loc[index, "Datetime_Adjusted_UTC+1"]
        date_current_dt = dt.strptime(date_current, '%Y-%m-%d %H:%M:%S')
        salinity_current = NERRS_data.loc[index, "Sal"]
    
        date_before = NERRS_data.loc[index-1, "Datetime_Adjusted_UTC+1"]
        date_before_dt = dt.strptime(date_before, '%Y-%m-%d %H:%M:%S')
        salinity_before = NERRS_data.loc[index-1, "Sal"]
        time_valid_left = timeWithinRange(date_current_dt, date_before_dt)
        print("lt", time_valid_left)
        salinity_diff_left = abs(salinity_current-salinity_before)
        print("left", salinity_diff_left)

        date_after = NERRS_data.loc[index+1, "Datetime_Adjusted_UTC+1"]
        date_after_dt = dt.strptime(date_after, '%Y-%m-%d %H:%M:%S')
        salinity_after = NERRS_data.loc[index+1, "Sal"]
        time_valid_right = timeWithinRange(date_after_dt, date_current_dt)
        print("rt", time_valid_right)
        salinity_diff_right = abs(salinity_after-salinity_current)
        print("right", salinity_diff_right)

        '''
        if math.isnan(salinity_current):
            row_drop_list.append(index)
        if math.isnan(salinity_before):
            row_drop_list.append(index)
        if math.isnan(salinity_after):
            row_drop_list.append(index)
        if not(math.isnan(salinity_current)):
            if int(salinity_current) == 0.0:
                row_drop_list.append(index)
        if not(math.isnan(salinity_before)):
            if int(salinity_before) == 0.0:
                row_drop_list.append(index-1)
        if not(math.isnan(salinity_after)):
            print(math.isnan(salinity_after))
            if int(salinity_after) == 0.0:
                row_drop_list.append(index+1)
        '''
        if time_valid_left and time_valid_right:
            if (salinity_diff_left > 5.0) and (salinity_diff_right > 5.0):
                print("here")
                row_drop_list.append(index)
        if not(time_valid_left):
            row_drop_list.append(index)
        if not(time_valid_right):
            row_drop_list.append(index)
    

    print("row index dropped:", row_drop_list)

    print("before", NERRS_data)

    NERRS_data_new = NERRS_data.drop(row_drop_list)
    #NERRS_data_new = NERRS_data_new.reset_index()

    print("after", NERRS_data_new)

    
    # Updates data file name to reflect the outliers haven been taken out
    file_name_adjusted = file_name + "_NO.csv"

    NERRS_data_new.to_csv(file_name_adjusted, index=None)

    
    
    time_list = []
    for i in NERRS_data_new["Datetime_Adjusted_UTC+1"]:
        datetime_obj = dt.strptime(i, '%Y-%m-%d %H:%M:%S')
        time_list.append(datetime_obj)

    # Graphing
    fig, ax1 = plt.subplots(figsize=(14,7))
    p1 = ax1.scatter(time_list, NERRS_data_new["Sal"], color = "brown", label = 'Salinity')
    
    # Sets axis labels
    ax1.set_ylabel("Salinity (PSU)")
    ax1.set_xlabel("Dates (MM-DD) UTC")
    #ax1.yaxis.label.set_color(p2[0].get_color())
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval = 1))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 7))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=45)
    
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title("NERRS: After Outliers Removed", loc='center')
    fig.legend(loc = 'upper center', ncol = 3, borderaxespad=4)
    plt.show()

    

# Metoxit Point 2020
#NERRS_outlier_remover("wqbmpwq2020.csv", "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2020_adjusted_UTC+1.csv")

# Metoxit Point 2021
#NERRS_outlier_remover("wqbmpwq2021.csv", "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2021_adjusted_UTC+1.csv")

# Metoxit Point 2022
#NERRS_outlier_remover("wqbmpwq2022.csv", "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2022_adjusted_UTC+1.csv")

# Metoxit Point 2023
NERRS_outlier_remover("wqbmpwq2023.csv", "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2023_adjusted_UTC+1.csv")




