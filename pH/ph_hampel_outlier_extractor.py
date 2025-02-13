import pandas as pd
import datetime
from datetime import datetime as dt
from hampel import hampel
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

def sami_hampel_filter(file_loc, year, window):
    # pCO2 Data
    # Used to hold data from csv file  
    xData = []      # Dates
    tyData = []     # Temperature
    cyData = []     # CO2
    byData = []     # Battery Voltage

    # Used in taking out empty data values from pCO2 data
    numofLinesD = 0


    # Outliers
    # Holds information on outliers
    outlierData = []
    outlierDataSal = []

    # Used in taking out empty values from salinity data
    numofLinesS = -1


    # Time
    # Holds converted time values
    xDataTrueO =[]      # Outlier times
    xDataTrueNO = []    # No outlier times



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
    original_sami_data = pd.DataFrame({"Date": xData, "Temp": tyData, "CO2": cyData, "Battery": byData})

    original_sami_data.to_csv(str(year) + "_pCO2_Formatted_Data.csv", index=False)

    #print("Original SAMI Data:")
    #print(original_sami_data.head())

    # Extract the CO2 column
    pco2_original = original_sami_data['CO2']
    #print("Original pCO2 Data:")
    #print(pco2_original.head())
    
    print("Original data after empty values are taken out: ", len(pco2_original))
    
    # Apply the Hampel filter
    result = hampel(pco2_original, window_size=window)

    # Extract the filtered data and outliers
    filtered_sami = result.filtered_data
    outlier_indices = result.outlier_indices
    medians = result.medians
    mad_values = result.median_absolute_deviations
    thresholds = result.thresholds

    print("Filtered pCO2 Data:", len(filtered_sami))
    print("Number of Outliers:", len(outlier_indices))

    
    #print("Filtered pCO2 Data:")
    #print(filtered_sami.head())
    #print("Outlier Indices:")
    #print(outlier_indices)
    #print("Medians:")
    #print(medians)
    #print("MAD Values:")
    #print(mad_values)
    #print("Thresholds:")
    #print(thresholds)

    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(original_sami_data['Date'], pco2_original, label='Original pH')
    #axes[0].fill_between(range(len(original_sami_data)), medians + thresholds, medians - thresholds, color='gray', alpha=0.5, label='Median +- Threshold')
    axes[0].scatter(original_sami_data['Date'].iloc[outlier_indices], pco2_original.iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(year) + ' Original pH Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(original_sami_data['Date'], filtered_sami, label='Filtered pH')
    axes[1].set_title(str(year) + ' pH Data Hampel Filter' + ' (Window Size = ' + str(window) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_save_name = "pH_" + str(year) + "_Hampel_Graph_WindowSize_" + str(window)+ ".png"
    plt.savefig(my_path + '\\pH_Graphs\\Hampel_Filter\\' + graph_save_name)

    plt.tight_layout()
    plt.show()


sami_hampel_filter('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\pCO2\\SAMI_pCO2\\pCO2_Annual_Compiled_Data\\pCO2_2022_Complete_Data.csv', 
                   2022,
                   10)
