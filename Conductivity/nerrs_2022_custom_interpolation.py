# Adds in 12-hr variations of the ~week prior to the break on top of the week before and after mean to interpolate
# Obtain 

import pandas as pd
import numpy as np
from datetime import timedelta
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime


def nerrs_custom_interpolation(break_start_day, break_end_day, adjustment_start_day):
    nerrs_data = pd.read_csv("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\nerrs_2022_empty_sal_rows_test.csv")

    nerrs_data["Datetime"] = pd.to_datetime(nerrs_data["Datetime"])

 

    
    week_before = (break_start_day - timedelta(days=7), break_start_day)
    print("week_before", week_before)
    week_after = (break_end_day, break_end_day + timedelta(days=7))
    print("week_after", week_after)
        
    before_mean = (nerrs_data[(nerrs_data['Datetime'] > week_before[0]) & (nerrs_data['Datetime'] <= week_before[1])]['Salinity']).mean()
    after_mean = (nerrs_data[(nerrs_data['Datetime'] > week_after[0]) & (nerrs_data['Datetime'] <= week_after[1])]['Salinity']).mean()
        
    before_after_mean = (before_mean + after_mean) / 2
    print("before_after_mean", before_after_mean)
    

    missing_index_list = []
    for index in range(0, len(nerrs_data)):
        if nerrs_data.loc[index, 'Datetime'] >= break_start_day and nerrs_data.loc[index, 'Datetime'] <= break_end_day:
            nerrs_data.loc[index, 'Salinity'] = before_after_mean
            missing_index_list.append(index)

    print("Added mean", nerrs_data)
    nerrs_data.to_csv("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\nerrs_2022_empty_sal_rows_added_mean_week_test.csv", index=False)


    nerrs_data2 = nerrs_data.copy()

    seasonal_variation_part1 = pd.read_csv("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\NERRS_2022_Part1_Metoxit_MSTL_Seasonal_Component_Table.csv")
    #seasonal_variation_part2 = pd.read_csv("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\NERRS_2022_Part2_Metoxit_MSTL_Seasonal_Component_Table.csv")

    for index in range(0, len(seasonal_variation_part1)):
        if nerrs_data2.loc[index, 'Datetime'] == adjustment_start_day:
            adjustment_start_index = index
            print("Found adjustment start index", adjustment_start_index)

    indexb = 0
    for indexa in range(0, len(nerrs_data2)):
        if (nerrs_data2.loc[indexa, 'Datetime'] >= break_start_day) and (nerrs_data2.loc[indexa, 'Datetime'] <= break_end_day):
            print(nerrs_data2.loc[indexa, 'Datetime'])
            print(break_start_day)
            print(break_end_day)
            adjustment_index = adjustment_start_index + indexb
            print("hi I have the adjustment index")
            print(adjustment_index)
            print(len(seasonal_variation_part1)-1)
            if adjustment_index <= (len(seasonal_variation_part1)-1):
                print("hi I am in range")
                nerrs_data2.loc[indexa, 'Salinity'] = seasonal_variation_part1.loc[adjustment_index, 'seasonal'] + nerrs_data2.loc[indexa, 'Salinity'] 
                print("hi I should have adjusted something")
                print(seasonal_variation_part1.loc[adjustment_index, 'seasonal'] + nerrs_data2.loc[indexa, 'Salinity'])
                indexb += 1
            else:
                adjustment_index = adjustment_start_index
                ("hi I should be back in range")
                nerrs_data2.loc[indexa, 'Salinity'] = seasonal_variation_part1.loc[adjustment_index, 'seasonal'] + nerrs_data2.loc[indexa, 'Salinity']
                print("hi I should have adjusted something")
                print(seasonal_variation_part1.loc[adjustment_index, 'seasonal'] + nerrs_data2.loc[indexa, 'Salinity'])
                indexb = 0
                print(adjustment_index)
    
    print("Finished interpolation", nerrs_data2)
    nerrs_data2.to_csv("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\nerrs_2022_interpolation_with_daily_test_week_mean.csv", index=False)


    # Graphing
    fig, ax1 = plt.subplots(figsize=(14,7))

    p1 = ax1.plot(nerrs_data["Datetime"], nerrs_data["Salinity"], color = 'blue', marker = "o", markersize = 2, label = 'Original Salinity with Mean for Missing')
    p2 = ax1.scatter(nerrs_data2["Datetime"], nerrs_data2["Salinity"], color = 'red', marker = "x", label = 'Interpolated Salinity with Seasonal Variation')
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 8))     # Displays x-axis label every 14 days
    plt.xticks(rotation=90)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 7))       # Indicates each day (without label) on x-axis

        
    # Sets axis labels and changes font color of "pco2" label for easy viewing
    ax1.set_xlabel("Dates (MM-DD) UTC")
    ax1.set_ylabel("Salinity (ppt)")
    ax1.yaxis.label.set_color("k")  


    ax2 = ax1.twinx()
    p2 = ax2.plot(nerrs_data2["Datetime"], nerrs_data2["Tide_Height"], color = 'g', linestyle = 'solid', label = "Tide Height")
    ax2.set_ylabel("Tide Height (m)")
    ax2.yaxis.label.set_color(p2[0].get_color())
    ax2.set_ylim(-0.5, 15)  # Adjust y-axis limits for tide height


    # Sets title, adds a grid, and shows legend
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title("NERRS 2022 Interpolated Salinity", loc='center')
    fig.legend(loc = 'upper left', ncol = 2, borderaxespad=4)
    plt.savefig("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\nerrs_2022_custom_interpolated_salinity_test2_week_mean.png")

    plt.show()


nerrs_custom_interpolation(datetime.datetime(2022, 6, 25, 00, 45), datetime.datetime(2022, 7, 31, 17, 00), datetime.datetime(2022, 5, 12, 19, 30))
