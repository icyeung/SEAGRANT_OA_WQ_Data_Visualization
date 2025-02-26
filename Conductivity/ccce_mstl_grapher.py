import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import date2num
import math
import pytz
import datetime
from statsmodels.tsa.seasonal import MSTL



def ccce_mstl_grapher(file_location, date_start, date_end, trunc_date_start, trunc_date_end, seasonal_period, data_year, location):
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

    #print(CCCE_fitted_data)
    
    CCCE_fitted_data = CCCE_fitted_data.drop('level_0', axis=1)
    CCCE_fitted_data = CCCE_fitted_data.drop('index', axis=1)

    CCCE_fitted_data.to_csv('CCCE_' + str(data_year) + "_" + location + "_Formatted_Data.csv", index=False)

    

    # MSTL Decomposition
    result = MSTL(CCCE_fitted_data['Salinity'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    #print(res)
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = 'CCCE_' + str(data_year) + "_" + location + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Breakdown.png"
    plt.savefig(my_path + '\\Conductivity_Graphs\\CCCE_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = CCCE_fitted_data[np.abs(z_scores) > 2.5]

    not_outliers = CCCE_fitted_data[np.abs(z_scores) <= 2.5]
    
    #print(outliers)
    print ("# of Outliers: ", len(outliers))
    #print(not_outliers)
    print ("# of Non-Outliers: ", len(not_outliers))


    outlier_indices = outliers.index

    cleaned_ccce_data = CCCE_fitted_data.drop(CCCE_fitted_data.index[outlier_indices])

    cleaned_ccce_data = cleaned_ccce_data.reset_index(drop=True)

    
    

    # Save cleaned data to CSV
    cleaned_ccce_data.to_csv('CCCE_' + str(data_year) + "_" + location + "_MSTL_Filtered_Data.csv", index=False)
    

    print("Filtered Eureka Data:", len(cleaned_ccce_data))
    print("Number of Outliers:", len(outlier_indices))




    # Graphing
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(CCCE_fitted_data['Datetime_UTC'], CCCE_fitted_data['Salinity'], label='Original Salinity')
    axes[0].scatter(CCCE_fitted_data['Datetime_UTC'].iloc[outlier_indices], CCCE_fitted_data['Salinity'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original CCCE ' + location + ' Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_ccce_data['Datetime_UTC'], cleaned_ccce_data['Salinity'], label='Filtered Salinity')
    axes[1].set_title(str(data_year) + ' CCCE ' + location + ' Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = 'CCCE_' + str(data_year) + "_" + location + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5.png"
    plt.savefig(my_path + '\\Conductivity_Graphs\\CCCE_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)

    
    plt.tight_layout()
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
ccce_mstl_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\Cape_Cod_Cooperative_Extension_Data\\Barnstable_Harbor\\BH2019 Aug Sept.csv",
                  "08-01-2019", "10-02-2019",
                  datetime.date(2019, 8, 1), datetime.date(2019, 10, 2),
                  [12, 708],
                  2019,
                  "Barnstable")