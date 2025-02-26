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
import time
from statsmodels.tsa.seasonal import MSTL


def NERRS_mstl_grapher(file_location, date_start, date_end, trunc_date_start, trunc_date_end, data_save_name, seasonal_period, data_year):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    NERRS_data = pd.read_csv(file_location)

    # Converts string time stamps from EST to GMT/UTC
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

        return datetime_dt_utc

    nerrs_datetime_list = []
    for value in NERRS_data["DateTimeStamp"]:
        nerrs_datetime_list.append(NERRS_time_converter(value))


    NERRS_data["Datetime_UTC"] = nerrs_datetime_list


    def commonDataRange_NERRS(data_df, start_date, end_date):
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
        data_df = data_df.reset_index(drop=True)
        
        return data_df

    NERRS_fitted_data = commonDataRange_NERRS(NERRS_data, date_start, date_end)
    NERRS_fitted_data = NERRS_fitted_data.reset_index(drop=True)

    #print(NERRS_fitted_data)

    not_flagged_data = NERRS_fitted_data.apply(lambda row: row[(NERRS_fitted_data["F_Sal"] == "<0> ") | (NERRS_fitted_data["F_Sal"] == "<0> (CRE)")])
    not_flagged_data = not_flagged_data.reset_index(drop=True)
    not_flagged_data.to_csv(data_save_name, index = False)


    # MSTL Decomposition  
    result = MSTL(not_flagged_data['Sal'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    print(res)

    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "NERRS_" + str(data_year) + "Metoxit_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Breakdown.png"
    plt.savefig(my_path + '\\Conductivity_Graphs\\NERRS_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = not_flagged_data[np.abs(z_scores) > 2.5]

    not_outliers = not_flagged_data[np.abs(z_scores) <= 2.5]
    
    print(outliers)
    print ("# of Outliers: ", len(outliers))
    print(not_outliers)
    print ("# of Non-Outliers: ", len(not_outliers))

    '''
    # 2. **Using Isolation Forest to detect outliers** (alternative method)
    iso_forest = IsolationForest(contamination=0.05)  # 5% contamination (outliers)
    outliers_pred = iso_forest.fit_predict(sami_data['CO2'].values.reshape(-1, 1))

    # Mark the outliers
    outlier_indices = np.where(outliers_pred == -1)[0]  # -1 indicates outliers
    '''

    outlier_indices = outliers.index

    cleaned_nerrs_data = not_flagged_data.drop(not_flagged_data.index[outlier_indices])
    #print(cleaned_sami_data)

    # Save cleaned data to CSV
    cleaned_nerrs_data.to_csv('NERRS_' + str(data_year) + "_Metoxit_MSTL_Filtered_Data.csv", index=False)
    

    print("Filtered Salinity Data:", len(cleaned_nerrs_data))
    print("Number of Outliers:", len(outlier_indices))
    
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(not_flagged_data['Datetime_UTC'], not_flagged_data['Sal'], label='Original Salinity')
    axes[0].scatter(not_flagged_data['Datetime_UTC'].iloc[outlier_indices], not_flagged_data['Sal'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original NERRS Metoxit Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_nerrs_data['Datetime_UTC'], cleaned_nerrs_data['Sal'], label='Filtered Salinity')
    axes[1].set_title(str(data_year) + ' NERRS Metoxit Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "NERRS_" + str(data_year) + "Metoxit_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5.png"
    plt.savefig(my_path + '\\Conductivity_Graphs\\NERRS_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)

    plt.tight_layout()
    plt.show()


# Metoxit Point 2020
NERRS_mstl_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2020_adjusted_UTC+1.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  "wqbmpwq2020_NoFlagged.csv",
                  [12, 708],
                  2020)

# Metoxit Point 2021
NERRS_mstl_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2021_adjusted_UTC+1.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  "wqbmpwq2021_NoFlagged.csv",
                  [12, 708],
                  2021)

# Metoxit Point 2022
NERRS_mstl_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2022_adjusted_UTC+1.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  "wqbmpwq2022_NoFlagged.csv",
                  [12, 708],
                  2022)

# Metoxit Point 2023
NERRS_mstl_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2023_adjusted_UTC+1.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  "wqbmpwq2023_NoFlagged.csv",
                  [12, 708],
                  2023)