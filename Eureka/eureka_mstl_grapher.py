# Date time column, index = 0
# Specific coonductivity column, index = 17
# Water temperature column, index = 15
# pH column, index = 16
# Depth column, index = 18
# Chloropyll column, index = 19
# DO column, index = 20

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import math
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import datetime
import numpy as np
from statsmodels.tsa.seasonal import MSTL


def commonDataRange(datetime, start_date, end_date):

    date = datetime.split(" ")[0]

    m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
    date1 = dt(y1, m1, d1)
    
    m2, d2, y2 = [int(date) for date in start_date.split("/")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("/")]
    date3 = dt(y3, m3, d3)       
      
    if (date1 <= date3) & (date1>= date2):
        return True
    else:
        return False

def eureka_mstl_grapher(file, data_year, seasonal_period, title, year):
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    formatted_folder_location = os.path.join(__location__, "Eureka_Data\\Eureka_Formatted_Data\\")
    formatted_year_data_folder = "Formatted_" + year + "_Data\\"
    formatted_data_year_location = os.path.join(formatted_folder_location, formatted_year_data_folder)

    eureka_data = pd.read_csv(os.path.join(formatted_data_year_location, file))

    #eureka_data = eureka.copy(deep=True)

    invalid_index_list = []

    print("why are you not being detected", eureka_data.loc[0, "Sp Cond"])

    for i in range(len(eureka_data)):
        if (float(eureka_data.loc[i, "Sp Cond"]) == 0) or (eureka_data.loc[i, "Sp Cond"] == "nan") or (eureka_data.loc[i, "Temperature"] == np.NaN) or float((eureka_data.loc[i, "Temperature"] == 0)):
            invalid_index_list.append(i)
    
    print(invalid_index_list)

    eureka_data = eureka_data.dropna()
    eureka_data = eureka_data.drop(invalid_index_list)
    eureka_data = eureka_data.reset_index()

    print(eureka_data)
   
    # Fixes time
    def timeConverterto24(datetime):
        time_number = datetime.split(" ")[1]
        h1, m1, s1 = [int(number) for number in time_number.split(":")]
        converted_time = str(h1) + ":" + str(m1)
        converted_time_dt = dt.strptime(converted_time, "%H:%M")
        return converted_time_dt

    if data_year == 2018:
        date_column_name = "Time (America/New_York)"
    elif data_year == 2019:
        date_column_name = "Time (UTC)"

    eureka_data_time_converted_list = []
    for time in eureka_data[date_column_name]:
        eureka_data_time_converted_list.append(timeConverterto24(time))
    #print("time", NOAA_tidal_data_time_converted_list)

    eureka_data_date_converted_list = []    
    for date in eureka_data[date_column_name]:
        eureka_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%m-%d-%Y"))
    #print("date", NOAA_tidal_data_date_converted_list)

    if len(eureka_data_date_converted_list) == len(eureka_data_time_converted_list):
        print("yayyyyy, everything works fine so far")
    else:
        print("Oops", "date", len(eureka_data_date_converted_list), "time", len(eureka_data_time_converted_list))

    #print(eureka_data_date_converted_list)

    


    eureka_data_datetime_combined_list = []
    for index in range(0, len(eureka_data_date_converted_list)):
        combined_dt_lst = dt.combine(eureka_data_date_converted_list[index], eureka_data_time_converted_list[index].time())
        if data_year == 2018:
            combined_dt_utc = combined_dt_lst + datetime.timedelta(hours=4)
        elif data_year == 2019:
            combined_dt_utc = combined_dt_lst
        eureka_data_datetime_combined_list.append(combined_dt_utc)

    eureka_data["DateTime (UTC)"] = eureka_data_datetime_combined_list

    print(eureka_data)

    # Calculates Conductivity from Specific Conductivity and Temperature
    # Temperature must be in C
    def spec_cond_2_cond(specificCond, temperature):
        conductivity = specificCond * (1 + 0.02 * (temperature - 25))
        return conductivity

    conductivity_list = []
    for i in range(len(eureka_data)):
        conductivity = spec_cond_2_cond(eureka_data.loc[i, "Sp Cond"], eureka_data.loc[i, "Temperature"])
        #print(salinity)
        
        conductivity_list.append(conductivity)
        
    eureka_data["Conductivity"] = conductivity_list

    print(eureka_data)

    # Calculates salinity
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
        
    print("salinity", condSalConv(45000, 16))        

    # Converts all conductivity and temperature measurements to salinity
    # Rounds salinity conversions to 3 decimal places

    cal_sal_list = []  
    used_time = []
    used_temp = []
    used_sp_cond = []
    used_cond = []  
    for i in range(len(eureka_data)):
        salinity = condSalConv(eureka_data.loc[i, "Conductivity"], eureka_data.loc[i, "Temperature"])
        #print(salinity)
        
        if salinity != "":
            salinity = round(float(salinity), 3)
        
            cal_sal_list.append(salinity)
            used_time.append(eureka_data.loc[i, "DateTime (UTC)"])
            used_temp.append(eureka_data.loc[i, "Temperature"])
            used_sp_cond.append(eureka_data.loc[i, "Sp Cond"])
            used_cond.append(eureka_data.loc[i, "Conductivity"])

    print(len(cal_sal_list))

    cal_sal_df = pd.DataFrame({"Date": used_time, "Temperature": used_temp, "Conductivity": used_cond, "Sp Cond": used_sp_cond, "Salinity": cal_sal_list})

    print(cal_sal_df)

    print(len(eureka_data))

    eureka_data["Salinity"] = cal_sal_list

    eureka_data = eureka_data.drop('index', axis=1)

    eureka_data.to_csv("Deer_Island-SG1-2018_Annual_Data_UTC.csv", index = None)



    # MSTL Decomposition
    result = MSTL(eureka_data['Salinity'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    #print(res)
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "Eureka_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Breakdown.png"
    plt.savefig(my_path + '\\Eureka_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = eureka_data[np.abs(z_scores) > 2.5]

    not_outliers = eureka_data[np.abs(z_scores) <= 2.5]
    
    #print(outliers)
    print ("# of Outliers: ", len(outliers))
    #print(not_outliers)
    print ("# of Non-Outliers: ", len(not_outliers))


    outlier_indices = outliers.index

    cleaned_eureka_data = eureka_data.drop(eureka_data.index[outlier_indices])
    #print(cleaned_sami_data)

    # Save cleaned data to CSV
    cleaned_eureka_data.to_csv('Eureka_' + str(data_year) + "_MSTL_Filtered_Data.csv", index=False)
    

    print("Filtered Eureka Data:", len(cleaned_eureka_data))
    print("Number of Outliers:", len(outlier_indices))




    # Graphing
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(eureka_data['DateTime (UTC)'], eureka_data['Salinity'], label='Original Salinity')
    axes[0].scatter(eureka_data['DateTime (UTC)'].iloc[outlier_indices], eureka_data['Salinity'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original Eureka Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_eureka_data['DateTime (UTC)'], cleaned_eureka_data['Salinity'], label='Filtered Salinity')
    axes[1].set_title(str(data_year) + ' Eureka Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_save_name = "Eureka_" + str(data_year) + "_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5.png"
    plt.savefig(my_path + '\\Eureka_Graphs\\MSTL\\Z_Score_2.5\\' + graph_save_name)

    
    plt.tight_layout()
    plt.show()

# Deer Island 2018 Conductivity
eureka_mstl_grapher("Deer_Island-SG1-2018_Annual_Data.csv", 2018, [12, 708], "Eureka 2018 Deer Island (SG1) Conductivity", "2018")

# Deer Island 2019 Conductivity
#eureka_mstl_grapher("Deer_Island-SG1-2019_Annual_Data.csv", 2019, [12, 708], "Eureka 2019 Deer Island (SG1) Conductivity", "2019")
