import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import math
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime as dt
from statsmodels.tsa.seasonal import MSTL



def timeConverterto24(datetime):
        time_number = datetime.split(" ")[1]
        h1, m1, s1 = [int(number) for number in time_number.split(":")]
        converted_time = str(h1) + ":" + str(m1) + ":" + str(s1)
        converted_time_dt = dt.strptime(converted_time, "%H:%M:%S")
        return converted_time_dt


# Conductivity conversion to salinity
# Conversion function
# Input conductivity and corresponding temperature measurement
# Temperature must be between 0,30 C (exclusive)
# Conductivity must be greater than 0
# Formula & code retrived from: http://www.fivecreeks.org/monitor/sal.shtml
def condSalConv(conductivity, temperature):
    

    a0 = 0.008
    a1 = -0.1692
    a2 = 25.3851
    a3 = 14.0941
    a4 = -7.0261
    a5 = 2.7081

    b0 = 0.0005
    b1 = -0.0056
    b2 = -0.0066
    b3 = -0.0375
    b4 = 0.0636
    b5 = -0.0144

    c0 = 0.6766097
    c1 = 0.0200564
    c2 = 0.0001104259
    c3 = -0.00000069698
    c4 = 0.0000000010031

    try:
        if float(temperature) > 0 and float(temperature) < 30 and float(conductivity) > 0:
            r = conductivity/42914
            r/= (c0 + temperature * (c1 + temperature * (c2 + temperature * (c3 + temperature * c4))))

            r2 = math.sqrt(r)

            ds = b0 + r2 * (b1 + r2 * (b2 + r2 * (b3 + r2 * (b4 + r2 * b5))))

            ds*= ((temperature - 15.0) / (1.0 + 0.0162 * (temperature - 15.0)))

            salinity = a0 + r2 * (a1 + r2 * (a2 + r2 * (a3 + r2 * (a4 + r2 * a5)))) + ds

            return salinity
        else:
            salinity = ""
            return salinity
            print("Error: Input is out of bounds")
    except ValueError:
        print("Error: Input is not a float")



def hobo_mstl_grapher(file, data_year, seasonal_period, hobo_num, sal_offset_num):
    
    # Used to find location of specified file within Python code folder
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


    # Salinity Data
    # Used to hold salinity data from csv file
    salDate = []
    condData = []
    condTempData = []


    # Used in taking out empty values from salinity data
    numofLinesS = -1

    salDateTrue = []    # Salinity times

    # Converted Salinity
    # Holds converted salinity values
    convertedSalinityData = []
    salinityDates = []
    salinityValues = []
    usedTemperature = []
    usedConductivity = []
    usedTime = []


    # Takes out empty values in salinity data set
    with open(os.path.join(__location__, file),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
                #print(row)
        
                # Checks if time entry has corresponding Time and Verified Measurement
                # If not, does not include data point in graph
                if numofLinesS > 1:
                    if not row[0] == "-" and not row[1] == "-" and not row[2] == "-" and not row[0] == "" and not row[1] == "" and not row[2] == "":
                        salDate.append(row[0])
                        condData.append(float(row[1]))
                        condTempData.append(float(row[2]))
                        numofLinesS += 1
                elif numofLinesS <= 1:
                    numofLinesS += 1
                
    #print(len(salDate))
    #print(len(condData))
    #print(len(condTempData))
    
    
    hobo_data = pd.DataFrame({'Date': salDate, 'Conductivity': condData, 'Temperature (F)': condTempData})
    
    
    
    # Salinity time conversion
    hobo_data_time_converted_list = []
    hobo_data_date_converted_list = []   
    for date in hobo_data["Date"]:
        hobo_data_time_converted_list.append(timeConverterto24(date))
        hobo_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%m/%d/%y"))

    if len(hobo_data_date_converted_list) == len(hobo_data_time_converted_list):
        print("yayyyyy, everything works fine so far")
    else:
        print("Oops", "date", len(hobo_data_date_converted_list), "time", len(hobo_data_time_converted_list))
    


    hobo_data_datetime_combined_list = []
    for index in range(0, len(hobo_data_date_converted_list)):
        combined_dt_lst = dt.combine(hobo_data_date_converted_list[index], hobo_data_time_converted_list[index].time())
        combined_dt_utc = combined_dt_lst + datetime.timedelta(hours=4)
        hobo_data_datetime_combined_list.append(combined_dt_utc)

    hobo_data["DateTime (UTC)"] = hobo_data_datetime_combined_list

    
    # Converts temperature from F to C
    condTempDataC = []
    for temp in hobo_data["Temperature (F)"]:
        tempC = (temp-32)/1.8
        condTempDataC.append(tempC)
    hobo_data["Temperature (C)"] = condTempDataC
    
    print("Lenth of Conductivity Data after empty values taken out:", len(hobo_data))

    # Verified Measurement also has to be between 5000, 55000
    # If not, does not include data point in graph
    for index in range(0, len(salDateTrue)):
        if (condData[index] <= 5000) or (condData[index] >= 55000):
            hobo_data = hobo_data.drop(index)
    hobo_data = hobo_data.reset_index(drop=True)

    print("Length of Conductivity Data after data points outside range taken out:", len(hobo_data))

    # Cond to sal Test case        
    print("cond to salinity", condSalConv(45000, 16))        

    # Converts all conductivity and temperature measurements to salinity
    # Rounds salinity conversions to 3 decimal places
    # Adds calculated salinity values to hobo_data dataframe
    for i in range(len(hobo_data)):
        salinity = condSalConv(hobo_data.loc[i, "Conductivity"], hobo_data.loc[i, "Temperature (C)"])
        #print("here", salinity)
        
        if salinity != "":
            salinity = round(float(salinity), 3)
        
            convertedSalinityData.append(salinity)
            usedTime.append(hobo_data.loc[i, "Date"])
            usedTemperature.append(hobo_data.loc[i, "Temperature (C)"])
            usedConductivity.append(hobo_data.loc[i, "Conductivity"])
        else:
            convertedSalinityData.append("")

    hobo_data["Salinity Value"] = convertedSalinityData

    # Takes out empty values in salinity data from hobo_data dataframe
    for index in range(0, len(hobo_data)):
        if (convertedSalinityData[index] == ""):
            hobo_data = hobo_data.drop(index)
    hobo_data = hobo_data.reset_index(drop=True)
    
    # Offsets Salinity Values by year
    corrected_sal_value_list = []
    if sal_offset_num != 0:
        for index in range(0, len(hobo_data)):
            sal_value = hobo_data.loc[index, "Salinity Value"]
            corrected_sal_value = sal_value + sal_offset_num
            corrected_sal_value_list.append(corrected_sal_value)
        name = "Salinity Value (Offset +" + str(sal_offset_num) + ")"
        hobo_data[name] = corrected_sal_value_list
    
    hobo_data.to_csv('HOBO_#' + str(hobo_num) + "_" + str(data_year) + "_Formatted_Data.csv", index=False)

    print("Length of Conductivity Data after empty salinity values taken out:", len(hobo_data)) 
    

    # MSTL Decomposition
    result = MSTL(hobo_data['Salinity Value'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    #print(res)
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "HOBO_#" + str(hobo_num) + "_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Breakdown.png"
    plt.savefig(my_path + '\\Conductivity_Graphs\\HOBO_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = hobo_data[np.abs(z_scores) > 2.5]

    not_outliers = hobo_data[np.abs(z_scores) <= 2.5]
    
    #print(outliers)
    print ("# of Outliers: ", len(outliers))
    #print(not_outliers)
    print ("# of Non-Outliers: ", len(not_outliers))


    outlier_indices = outliers.index

    cleaned_hobo_data = hobo_data.drop(hobo_data.index[outlier_indices])

    cleaned_hobo_data = cleaned_hobo_data.reset_index(drop=True)

    
    

    # Save cleaned data to CSV
    cleaned_hobo_data.to_csv('HOBO_#' + str(hobo_num) + "_" + str(data_year) + "_MSTL_Filtered_Data.csv", index=False)
    

    print("Filtered Eureka Data:", len(cleaned_hobo_data))
    print("Number of Outliers:", len(outlier_indices))




    # Graphing
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(hobo_data['DateTime (UTC)'], hobo_data['Salinity Value'], label='Original Salinity')
    axes[0].scatter(hobo_data['DateTime (UTC)'].iloc[outlier_indices], hobo_data['Salinity Value'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original HOBO #' + str(hobo_num) + ' Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_hobo_data['DateTime (UTC)'], cleaned_hobo_data['Salinity Value'], label='Filtered Salinity')
    axes[1].set_title(str(data_year) + ' HOBO #' + str(hobo_num) + ' Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "HOBO_#" + str(hobo_num) + "_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5.png"
    plt.savefig(my_path + '\\Conductivity_Graphs\\HOBO_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)

    
    plt.tight_layout()

    # Displays figures
    plt.show()

'''
# Part 1 of 2021 NF
hobo_mstl_grapher("HOBO_Data\\Conductivity_Data_With_Outliers\\Salinity_Carolina_FiddlersCove_9-28-21_2.csv",
                  2021,
                  [12, 708],
                  2.1,
                  4) 

# Part 2 of 2021 NF
hobo_mstl_grapher("HOBO_Data\\Conductivity_Data_With_Outliers\\Salinity_Carolina_FiddlersCove_12-10-21_2.csv",
                  2021,
                  [12, 708],
                  2.2,
                  4) 


# 2021 NF Combined
hobo_mstl_grapher("HOBO_Data\\Conductivity_Data_With_Outliers\\HOBO_2_2021_Combined_Formatted_Data.csv",
                  2021,
                  [12, 708],
                  2,
                  4) 
'''

# 2022 Poc
hobo_mstl_grapher("HOBO_Data\\Conductivity_Data_With_Outliers\\Salinity_Carolina_Pocasset_12-9-22_1.csv",
                  2022,
                  [12, 708],
                  1,
                  15)
 