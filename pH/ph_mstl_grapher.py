import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import MSTL
from sklearn.ensemble import IsolationForest
from datetime import datetime as dt

import os
import csv
import math
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


# Converts Year Day Column to calendar day and time
# Extracts time in HH:MM:SS format from date in Year Day column
def timeConverter (date):
    time = ""

    timeDeciDay, timeWholeDay = math.modf(float(date))
    timeDeciDay = timeDeciDay * 24

    timeDeciHour, timeWholeHour = math.modf(timeDeciDay)
    hour = str(math.trunc(timeWholeHour))

    timeDeciMinute, timeWholeMinute = math.modf(timeDeciHour * 60)
    minute = str(math.trunc(timeWholeMinute))

    timeDeciSecond, timeWholeSecond = math.modf(timeDeciMinute * 60)
    second = str(math.trunc(timeWholeSecond))
        
    time = hour + ":" + minute + ":" + second

    timeObject = datetime.datetime.strptime(time, '%H:%M:%S').time()

    return timeObject


# Sourced from https://pythonhow.com/how/check-if-a-string-is-a-float/
    # Used to check if data is a numeric value
def is_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False


def sami_ph_mstl(file_loc, data_year, seasonal_period):
    
    print("hi 1")

    # SAMI data
    # pCO2 Data
    # Used to hold data from csv file  
    xData = []      # Dates (Ordinal)
    tyData = []     # Temperature
    sData = []      # Constant Salinity
    cyData = []     # pH
    byData = []     # Battery Voltage
    dData = []      # Date
    ttData = []     # Time

    # Used in taking out empty data values from pCO2 data
    numofLinesD = 0

    # Takes out empty data values in pCO2 data set
    with open(file_loc,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter='\t')
        for row in lines:
            
            # Checks if time entry has corresponding Temperature, CO2, and Battery Voltage
            # If not, does not include data point in graph
            if not row[1] == "" and is_float(row[1]) and not row[2] == "" and is_float(row[2]) and not row[3] == "" and is_float(row[3]) and float(row[3]) != 0.00 and not row[4] == "" and is_float(row[4]) and numofLinesD > 0:
                xData.append(float(row[0]))
                tyData.append(float(row[1]))
                sData.append(float(row[2]))
                cyData.append(float(row[3]))
                byData.append(float(row[4]))
                dData.append(str(row[5]))
                ttData.append(str(row[6]))
                numofLinesD += 1
            elif numofLinesD == 0:
                numofLinesD += 1

    # Displays total number of data points before outliers are taken out
    print("hi")

    # Dataframe of original data after blanks removed
    sami_ph_data = pd.DataFrame({"Ordinal_Date": xData, "Date": dData, "Time":ttData, "Temp": tyData, "pH": cyData, "Battery": byData})
    #print("hi", sami_ph_data)

    sami_ph_data.to_csv(str(data_year) + "_pH_Formatted_Data.csv", index=False)

    #print("Original SAMI Data:")
    #print(original_sami_data.head())

    # Extract the CO2 column
    pH_original = sami_ph_data['pH']
    #print("Original pCO2 Data:")
    #print(pco2_original.head())
    
    
    
    print("Original data after empty values are taken out: ", len(pH_original))
    #sami_data.set_index('Date (UTC)', inplace=True)
    

    datetime_dt_list = []
    for date_index in range(0, len(dData)):
        if data_year != 2021:
            date = dData[date_index]
            #print(date)
            time = ttData[date_index]
            y1, m1, d1 = [int(date_part) for date_part in date.split("-")]
            date1 = dt(y1, m1, d1)
            converted_time = dt.strptime(time, "%H:%M:%S")
            datetime_dt_utc = dt.combine(date1, converted_time.time())
            datetime_dt_list.append(datetime_dt_utc)
        elif data_year == 2021:
            ordinal_date = xData[date_index]
            date_dt_noyear = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(ordinal_date)), timeConverter(ordinal_date))
            datetime_dt_utc = date_dt_noyear.replace(year = data_year)
            datetime_dt_list.append(datetime_dt_utc)

    sami_ph_data['Date (UTC)'] = datetime_dt_list

    # MSTL Decomposition
    #result = seasonal_decompose(sami_data['CO2'], model='additive', period=seasonal_period)  # Assuming daily data with yearly seasonality
    
    result = MSTL(sami_ph_data['pH'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    #print(res)
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "pH_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Breakdown.png"
    plt.savefig(my_path + '\\pH_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = sami_ph_data[np.abs(z_scores) > 2.5]

    not_outliers = sami_ph_data[np.abs(z_scores) <= 2.5]
    
    #print(outliers)
    print ("# of Outliers: ", len(outliers))
    #print(not_outliers)
    print ("# of Non-Outliers: ", len(not_outliers))


    outlier_indices = outliers.index

    cleaned_sami_data = sami_ph_data.drop(sami_ph_data.index[outlier_indices])
    #print(cleaned_sami_data)

    # Save cleaned data to CSV
    cleaned_sami_data.to_csv('pH_' + str(data_year) + "_MSTL_Filtered_Data.csv", index=False)
    

    print("Filtered pH Data:", len(cleaned_sami_data))
    print("Number of Outliers:", len(outlier_indices))
    
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(sami_ph_data['Date (UTC)'], sami_ph_data['pH'], label='Original pH')
    axes[0].scatter(sami_ph_data['Date (UTC)'].iloc[outlier_indices], sami_ph_data['pH'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original pH Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_sami_data['Date (UTC)'], cleaned_sami_data['pH'], label='Filtered pH')
    axes[1].set_title(str(data_year) + ' pH Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_save_name = "pH_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5.png"
    plt.savefig(my_path + '\\pH_Graphs\\MSTL\\Z_Score_2.5\\' + graph_save_name)

    plt.tight_layout()
    plt.show()
    

sami_ph_mstl('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\pH\\SAMI_pH\\pH_Annual_Compiled_Data\\pH_2021_Complete_Data.csv',
                   2021,
                   [12,708])