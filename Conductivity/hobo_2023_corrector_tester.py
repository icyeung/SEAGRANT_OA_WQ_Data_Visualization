import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as md
import datetime


'''
def find_midpoint_range(bbc_deep_df, bbc_index):
    output_list = []

    bbc_deep_df = pd.read_csv(bbc_deep_df)

    if bbc_index == -1:

        print("in find midpoint bbc-1")
        bbc_false_sample_date = dt(1900,5,17,14,6,18)
        bbc_next_sample_date = bbc_deep_df.loc[0, "Datetime_noyear"]
        bbc_next_sample_date = datetime.datetime.strptime(bbc_next_sample_date, "%Y-%m-%d %H:%M:%S")
        time_between = (bbc_next_sample_date-bbc_false_sample_date)
        time_between_days = time_between.days
        time_between_sec = time_between.seconds
            
        if time_between_days > 14 or (time_between_days == 14 and time_between_sec > 0): 
            bbc_first_end_date = bbc_false_sample_date+datetime.timedelta(days = 7)
            bbc_second_start_date = bbc_next_sample_date-datetime.timedelta(days = 7)
            output_list.append("2")
            output_list.append(bbc_false_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_first_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))

        if time_between_days < 14 or (time_between_days == 14 and time_between_sec == 0):
            time_between_allsec = time_between.total_seconds()
            midlength_time_between = time_between_allsec/2
            bbc_false_end_date = bbc_false_sample_date+datetime.timedelta(seconds=midlength_time_between)
            bbc_second_start_date = bbc_false_end_date+datetime.timedelta(seconds=1)
            output_list.append("1")
            output_list.append(bbc_false_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_false_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))

    if bbc_index == len(bbc_deep_df)-1:

        print("in find midpoint lenbbc-1")
        bbc_sample_date = bbc_deep_df.loc[bbc_index, "Datetime_noyear"]
        bbc_sample_date = datetime.datetime.strptime(bbc_sample_date, "%Y-%m-%d %H:%M:%S")
        bbc_end_date = bbc_deep_df.loc[bbc_index, "Datetime_noyear"]
        bbc_end_date = (datetime.datetime.strptime(bbc_end_date, "%Y-%m-%d %H:%M:%S")) +datetime.timedelta(days = 7)
        output_list.append("2")
        output_list.append(bbc_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
        output_list.append(bbc_end_date.strftime("%Y-%m-%d %H:%M:%S"))

    if bbc_index != -1 and bbc_index != len(bbc_deep_df)-1:
        
        print("in find midpoint !=-1")
        bbc_sample_date = bbc_deep_df.loc[bbc_index, "Datetime_noyear"]
        bbc_sample_date = datetime.datetime.strptime(bbc_sample_date, "%Y-%m-%d %H:%M:%S")
        bbc_next_sample_date = bbc_deep_df.loc[bbc_index+1, "Datetime_noyear"]
        bbc_next_sample_date = datetime.datetime.strptime(bbc_next_sample_date, "%Y-%m-%d %H:%M:%S")
        time_between = (bbc_next_sample_date-bbc_sample_date)
        time_between_days = time_between.days
        time_between_sec = time_between.seconds
        if time_between_days > 14 or (time_between_days == 14 and time_between_sec > 0): 
            bbc_first_end_date = bbc_sample_date+datetime.timedelta(days = 7)
            bbc_second_start_date = bbc_next_sample_date-datetime.timedelta(days = 7)
            output_list.append("2")
            output_list.append(bbc_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_first_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))

        if time_between_days < 14 or (time_between_days == 14 and time_between_sec == 0):
            time_between_allsec = time_between.total_seconds()
            midlength_time_between = time_between_allsec/2
            bbc_first_end_date = bbc_sample_date+datetime.timedelta(seconds=midlength_time_between)
            bbc_second_start_date = bbc_first_end_date+datetime.timedelta(seconds=1)
            output_list.append("1")
            output_list.append(bbc_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_first_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))   
    
    print(output_list)
    return(output_list)

find_midpoint_range("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\bbc_2023_deep.csv", 21)

'''

def find_closest_hobo(hobo_file, date, start_index):
        
        hobo_file = pd.read_csv(hobo_file)

        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        index = start_index
        isAfter = False
        while not(isAfter):
            print("in find closest hobo")

            if ((datetime.datetime.strptime(hobo_file.loc[index, "Datetime_noyear"], "%Y-%m-%d %H:%M:%S")) < date_dt) and not(isAfter):
                index +=1
                print(hobo_file.loc[index, "Datetime_noyear"])
                print(date_dt)
                print(index)
            else:
                isAfter = True
                print("another one done", index)
                break
        return index

#find_closest_hobo("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\hobo_2023.csv", "1900-09-29 13:00:00", 0)

find_closest_hobo("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\hobo_2023.csv", "1900-05-27 12:20:00", 0)

'''
def find_closest_hobo(hobo_file, date, start_index):
    hobo_data = pd.read_csv(hobo_file)
    
    print(hobo_data)

    # Ensure the Datetime_noyear column is parsed as datetime
    hobo_data['Datetime_noyear'] = pd.to_datetime(hobo_data['Datetime_noyear'], format="%Y-%m-%d %H:%M:%S")
    
    date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    closest_index = start_index
    min_diff = float('inf')
    
    for index in range(start_index, len(hobo_data)):
        current_date = hobo_data.loc[index, 'Datetime_noyear']
        diff = abs((current_date - date_dt).total_seconds())
        
        if diff < min_diff:
            min_diff = diff
            closest_index = index
        
        # If the current date is after the target date, we can stop searching
        if current_date > date_dt:
            break
    
    print(f"Closest index: {closest_index}, Date: {hobo_data.loc[closest_index, 'Datetime_noyear']}, Target Date: {date_dt}")
    return closest_index

# Test the function
find_closest_hobo("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\hobo_2023.csv", "1900-09-29 13:00:00", 0)
'''