import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import MSTL
from sklearn.ensemble import IsolationForest

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


def sami_mstl(file_loc, data_year, seasonal_period):
    # SAMI data
    # pCO2 Data
    # Used to hold data from csv file  
    xData = []      # Dates
    tyData = []     # Temperature
    cyData = []     # CO2
    byData = []     # Battery Voltage

    # Used in taking out empty data values from pCO2 data
    numofLinesD = 0

    # Takes out empty data values in pCO2 data set
    with open(file_loc,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter='\t')
        for row in lines:
            
            # Checks if time entry has corresponding Temperature, CO2, and Battery Voltage
            # If not, does not include data point in graph
            if not row[1] == "" and not row[2] == "" and not row[3] == "" and numofLinesD > 0:
                xData.append(float(row[0]))
                tyData.append(float(row[1]))
                cyData.append(float(row[2]))
                byData.append(float(row[3]))
                numofLinesD += 1
            elif numofLinesD == 0:
                numofLinesD += 1

    # Displays total number of data points before outliers are taken out
   

    # Dataframe of original data after blanks removed
    sami_data = pd.DataFrame({"Date": xData, "Temp": tyData, "CO2": cyData, "Battery": byData})

    sami_data.to_csv(str(data_year) + "_pCO2_Formatted_Data.csv", index=False)

    #print("Original SAMI Data:")
    #print(original_sami_data.head())

    # Extract the CO2 column
    pco2_original = sami_data['CO2']
    #print("Original pCO2 Data:")
    #print(pco2_original.head())
    
    

    ordinal_date_list = sami_data['Date']
    # Convert ordinal date ("Date") to datetime format
    # Converts all dates in Year Day to 2021-MM-DD HH:MM:SS
    # Original Data

    datetime_list = []    
    for dateValue in ordinal_date_list:
        date_dt_noyear = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(dateValue)), timeConverter(dateValue))
        date_dt = date_dt_noyear.replace(year = data_year)
        datetime_list.append(date_dt)

    print("Original data after empty values are taken out: ", len(pco2_original))

    sami_data['Date (UTC)'] = datetime_list
    #sami_data.set_index('Date (UTC)', inplace=True)
    
    # MSTL Decomposition
    #result = seasonal_decompose(sami_data['CO2'], model='additive', period=seasonal_period)  # Assuming daily data with yearly seasonality
    
    result = MSTL(sami_data['CO2'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    print(res)
    
    '''
    trend = result
    seasonal_intraday = result.seasonal[0]
    seasonal_monthly = result.seasonal[1]
    '''
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = sami_data[np.abs(z_scores) > 2]

    not_outliers = sami_data[np.abs(z_scores) <= 2]
    
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

    cleaned_sami_data = sami_data.drop(sami_data.index[outlier_indices])
    print(cleaned_sami_data
          )
    # Save cleaned data to CSV
    #cleaned_data.to_csv('cleaned_file.csv')
    

    print("Filtered pCO2 Data:", len(cleaned_sami_data))
    print("Number of Outliers:", len(outlier_indices))
    
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(sami_data['Date (UTC)'], sami_data['CO2'], label='Original pCO2')
    axes[0].scatter(sami_data['Date (UTC)'].iloc[outlier_indices], sami_data['CO2'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original pCO2 Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_sami_data['Date (UTC)'], cleaned_sami_data['CO2'], label='Filtered pCO2')
    axes[1].set_title(str(data_year) + ' pCO2 Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_save_name = "pCO2_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ ".png"
    plt.savefig(my_path + '\\pCO2_Graphs\\MSTL\\' + graph_save_name)

    plt.tight_layout()
    plt.show()
    

sami_mstl('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\pCO2\\SAMI_pCO2\\pCO2_Annual_Compiled_Data\\pCO2_2018_Complete_Data.csv',
                   2018,
                   [12,708])