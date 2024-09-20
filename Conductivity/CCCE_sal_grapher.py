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



def CCCE_sal_grapher(file_location, date_start, date_end, trunc_date_start, trunc_date_end, title, file_save_location, graph_save_location):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    CCCE_data = pd.read_csv(file_location)
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    
    # Converts time stamp from EST to UTC (adds 5 hours)
    def CCCE_time_converter(date_time):
        date = date_time.split(" ")[0]
        time = date_time.split(" ")[1]
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
        date1 = dt(y1, m1, d1)
        converted_time = dt.strptime(time, "%H:%M")
        datetime_dt_est = dt.combine(date1, converted_time.time())

        datetime_dt_utc = datetime_dt_est + datetime.timedelta(hours=5)

        return datetime_dt_utc

    
    CCCE_datetime_list = []
    
    for value in CCCE_data["Date/Time"]:
        CCCE_datetime_list.append(CCCE_time_converter(value))


    CCCE_data["Datetime_UTC"] = CCCE_datetime_list


    def commonDataRange_CCCE(data_df, start_date, end_date):
        m2, d2, y2 = [int(date) for date in start_date.split("-")]
        date2 = dt(y2, m2, d2)

        m3, d3, y3 = [int(date) for date in end_date.split("-")]
        date3 = dt(y3, m3, d3)   

        invalid_date_list = []
        invalid_date_index_list = []
        logger_date_index = 0

        #print(data_df)

        logger_dates_list = data_df["Datetime_UTC"].tolist()
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

    CCCE_fitted_data = commonDataRange_CCCE(CCCE_data, date_start, date_end)
    CCCE_fitted_data = CCCE_fitted_data.reset_index()

    print(CCCE_fitted_data)
    
    CCCE_fitted_data = CCCE_fitted_data.drop('level_0', axis=1)
    CCCE_fitted_data = CCCE_fitted_data.drop('index', axis=1)

    CCCE_fitted_data.to_csv(my_path + file_save_location, index = None)

    # Graphing
    fig, ax1 = plt.subplots(figsize=(14,7))

    p1 = ax1.scatter(CCCE_fitted_data["Datetime_UTC"], CCCE_fitted_data["Salinity"], 5, color = 'blue', marker = "o", label = 'CCCE Salinity')

    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 8))     # Displays x-axis label every 14 days
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 7))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=90)
    

    ax1.set_xlim([trunc_date_start, trunc_date_end])
    #ax1.set_ylim(26, 33)
        
    # Sets axis labels and changes font color of "pco2" label for easy viewing
    ax1.set_xlabel("Dates (MM-DD) UTC")
    ax1.set_ylabel("Salinity (ppt)")
    ax1.yaxis.label.set_color("k")  


    # Sets title, adds a grid, and shows legend
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper left', ncol = 2, borderaxespad=4)


    

    # Saves without outliers graph to specified name in folder
    plt.savefig(my_path + graph_save_location)
    plt.show()


# Cotuit Bay
'''
CCCE_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Cape_Cod_Cooperative_Extension_Data\\Cotuit_Bay\\cotb-dock-wq-2022.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  'CCCE Cotuit Bay 2022 Salinity',
                  '\\Conductivity_Graphs\\CCCE_Graphs\\CCCE_Salinity_2022_Cotuit.png')
'''

# Barnstable Harbor
CCCE_sal_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Cape_Cod_Cooperative_Extension_Data\\Barnstable_Harbor\\BH2019 Aug Sept.csv",
                  "08-01-2019", "10-02-2019",
                  datetime.date(2019, 8, 1), datetime.date(2019, 10, 2),
                  'CCCE Barnstable Harbor 2019 Salinity',
                  '\\Sourced_Data\\Cape_Cod_Cooperative_Extension_Data\\Barnstable_Harbor\\CCCE_Barnstable_Salinity_Data_2019_UTC.csv',
                  '\\Conductivity_Graphs\\CCCE_Graphs\\CCCE_Salinity_2019_Barnstable.png')