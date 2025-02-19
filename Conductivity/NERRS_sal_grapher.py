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

def NERRS_sal_grapher(file_location, date_start, date_end, trunc_date_start, trunc_date_end, data_save_name, title, file_save_location):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    NERRS_data = pd.read_csv(file_location)



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
        

        '''
        # Uses pytz package, ambiguous times (change in est/edt) result in error message
        utc=pytz.utc
        eastern = pytz.timezone('US/Eastern')

        timeObj = datetime.datetime.strptime(date_time, '%m/%d/%Y %H:%M')
        time_eastern = eastern.localize(timeObj, is_dst=None)
        timeObj_utc = time_eastern.astimezone(utc)
        '''

        '''
        utc=pytz.utc
        eastern=pytz.timezone('US/Eastern')

        timeObj=datetime.datetime.strptime(date_time,"%m/%d/%Y %H:%M")
        date_est=eastern.localize(timeObj,is_dst=None)
        date_utc=date_est.astimezone(utc)
        date_utc2=datetime.datetime.utcfromtimestamp(time.mktime(timeObj.timetuple()))
        '''

        return datetime_dt_utc

    nerrs_datetime_list = []
    for value in NERRS_data["DateTimeStamp"]:
        nerrs_datetime_list.append(NERRS_time_converter(value))


    NERRS_data["Datetime"] = nerrs_datetime_list


    #print(NERACOOS_data)


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
        data_df = data_df.reset_index(drop=True)
        
        return data_df

    NERRS_fitted_data = commonDataRange_NERRS(NERRS_data, date_start, date_end)
    NERRS_fitted_data = NERRS_fitted_data.reset_index(drop=True)

    print(NERRS_fitted_data)

    not_flagged_data = NERRS_fitted_data.apply(lambda row: row[(NERRS_fitted_data["F_Sal"] == "<0> ") | (NERRS_fitted_data["F_Sal"] == "<0> (CRE)")])
    not_flagged_data = not_flagged_data.reset_index(drop=True)
    not_flagged_data.to_csv(data_save_name, index = False)


    # Graphing
    fig, ax1 = plt.subplots(figsize=(14,7))

    p1 = ax1.scatter(NERRS_fitted_data["Datetime"], NERRS_fitted_data["Sal"], 5, color = 'blue', marker = "o", label = 'NERRS Salinity')

    p2 = ax1.scatter(not_flagged_data["Datetime"], not_flagged_data["Sal"], 5, color = 'red', marker = "o", label = 'QAQC Passed')

    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 8))     # Displays x-axis label every 14 days
    plt.xticks(rotation=90)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 7))       # Indicates each day (without label) on x-axis

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


# Sage Lot 2020
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Sage_Lot.png')
'''

# Sage Lot 2020 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Sage_Lot_zoomed_in.png')
'''

# Sage Lot 2021
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Sage_Lot.png')
'''

# Sage Lot 2021 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Sage_Lot_zoomed_in.png')
'''

# Sage Lot 2022
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2022 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Sage_Lot.png')
'''

# Sage Lot 2022 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2022 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Sage_Lot_zoomed_in.png')
'''

# Sage Lot 2023
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Sage_Lot.png')
'''

# Sage Lot 2023 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Sage_Lot\\wqbslwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Sage Lot) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Sage_Lot_zoomed_in.png')
'''



# Metoxit Point 2020

NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2020_adjusted_UTC+1.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  "wqbmpwq2020_NoFlagged.csv",
                  'NERRS Waquoit Bay (Metoxit Point) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Metoxit_Point_NoFlagged.png')


# Metoxit Point 2020 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Metoxit_Point\\wqbmpwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Metoxit_Point_zoomed_in.png')
'''

# Metoxit Point 2021

NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2021_adjusted_UTC+1.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  "wqbmpwq2021_NoFlagged.csv",
                  'NERRS Waquoit Bay (Metoxit Point) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Metoxit_Point_NoFlagged.png')


# Metoxit Point 2021 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Metoxit_Point\\wqbmpwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Metoxit_Point_zoomed_in.png')
'''

# Metoxit Point 2022

NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2022_adjusted_UTC+1.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  "wqbmpwq2022_NoFlagged.csv",
                  'NERRS Waquoit Bay (Metoxit Point) 2022 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Metoxit_Point_NoFlagged.png')


# Metoxit Point (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Metoxit_Point\\wqbmpwq2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) 2022 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Metoxit_Point_zoomed_in.png')
'''


# Metoxit Point 2023

NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2023_adjusted_UTC+1.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  "wqbmpwq2023_NoFlagged.csv",
                  'NERRS Waquoit Bay (Metoxit Point) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Metoxit_Point_NoFlagged.png')


# Metoxit Point 2023 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Metoxit_Point\\wqbmpwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Metoxit_Point_zoomed_in.png')
'''



# Menauhant 2020
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Menauhant.png')
'''

# Menauhant 2020 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Menauhant_zoomed_in.png')
'''

# Menauhant 2020 (outliers removed)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2020 Salinity (Outliers Removed)',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Menauhant_outliers_removed.png')
'''

# Menauhant 2021
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Menauhant.png')
'''

# Menauhant 2021 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Menauhant_zoomed_in.png')
'''

# Menauhant 2021 (outliers removed)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2021 Salinity (Outliers Removed)',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Menauhant_outliers_removed.png')
'''

# Menauhant 2022
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2022 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Menauhant.png')
'''

# Menauhant 2022 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2022 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Menauhant_zoomed_in.png')
'''

# Menauhant 2022 (outliers removed)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2022 Salinity (Outliers Removed)',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2022_Menauhant_outliers_removed.png')
'''
'''
# Menauhant 2023

NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Menauhant.png')
'''

# Menauhant 2023 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Menauhant_zoomed_in.png')
'''

# Menauhant 2023 (outliers removed)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Menauhant\\wqbmhwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Menauhant) 2023 Salinity (Outliers Removed)',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Menauhant_outliers_removed.png')
'''


# Childs River 2020
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Childs River) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Childs_River.png')
'''

# Childs River 2020 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2020.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  'NERRS Waquoit Bay (Childs River) 2020 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2020_Childs_River_zoomed_in.png')
'''

# Childs River 2021
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Childs River) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Childs_River.png')
'''

# Childs River 2021 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2021.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  'NERRS Waquoit Bay (Childs River) 2021 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2021_Childs_River_zoomed_in.png')
'''

# Childs River 2023
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Childs River) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Childs_River.png')
'''

# Childs River 2023 (zoomed in)
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\NERRS_Waquoit_Bay_Raw_Data\\Childs_River\\wqbcrwq2023.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Childs River) 2023 Salinity',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Childs_River_zoomed_in.png')
'''


# Metoxit Point 2023 outliers removed using NERRS_outlier_remover.ppy
'''
NERRS_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\wqbmpwq2023.csv_OR.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  'NERRS Waquoit Bay (Metoxit Point) 2023 Salinity No Outliers',
                  '\\Conductivity_Graphs\\NERRS_Graphs\\NERRS_Salinity_2023_Metoxit_Point_OR.png')
'''