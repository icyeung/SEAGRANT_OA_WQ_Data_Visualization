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

def eureka_grapher(file, title, start_date, end_date, year):

    numofLinesS = 0
    raw_datetime_list = []
    water_temp_list = []
    ph_list = []
    cond_list = []
    depth_list = []
    chlorophyll_list = []
    do_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    formatted_folder_location = os.path.join(__location__, "Eureka_Data\\Eureka_Formatted_Data\\")
    formatted_year_data_folder = "Formatted_" + year + "_Data\\"
    formatted_data_year_location = os.path.join(formatted_folder_location, formatted_year_data_folder)

    eureka_data = pd.read_csv(os.path.join(formatted_data_year_location, file))

   
    # Fixes time
    def timeConverterto24(datetime):
        time_number = datetime.split(" ")[1]
        h1, m1, s1 = [int(number) for number in time_number.split(":")]
        converted_time = str(h1) + ":" + str(m1)
        converted_time_dt = dt.strptime(converted_time, "%H:%M")
        return converted_time_dt

    eureka_data_time_converted_list = []
    for time in eureka_data["Time (UTC)"]:
        eureka_data_time_converted_list.append(timeConverterto24(time))
    #print("time", NOAA_tidal_data_time_converted_list)

    eureka_data_date_converted_list = []    
    for date in eureka_data["Time (UTC)"]:
        eureka_data_date_converted_list.append(dt.strptime((date.split(" ")[0]), "%m-%d-%Y"))
    #print("date", NOAA_tidal_data_date_converted_list)

    if len(eureka_data_date_converted_list) == len(eureka_data_time_converted_list):
        print("yayyyyy, everything works fine so far")
    else:
        print("Oops", "date", len(eureka_data_date_converted_list), "time", len(eureka_data_time_converted_list))

    print(eureka_data_date_converted_list)


    eureka_data_datetime_combined_list = []
    for index in range(0, len(eureka_data_date_converted_list)):
        eureka_data_datetime_combined_list.append(dt.combine(eureka_data_date_converted_list[index], eureka_data_time_converted_list[index].time()))

    eureka_data["DateTime"] = eureka_data_datetime_combined_list


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
    used_cond = []  
    for i in range(len(eureka_data)):
        salinity = condSalConv(eureka_data.loc[i, "Sp Cond"], eureka_data.loc[i, "Temperature"])
        #print(salinity)
        
        if salinity != "":
            salinity = round(float(salinity), 3)
        
            cal_sal_list.append(salinity)
            used_time.append(eureka_data.loc[i, "DateTime"])
            used_temp.append(eureka_data.loc[i, "Temperature"])
            used_cond.append(eureka_data.loc[i, "Sp Cond"])

    cal_sal_df = pd.DataFrame({"Date": used_time, "Temperature": used_temp, "Conductivity": used_cond, "Salinity": cal_sal_list})


    fig, ax1 = plt.subplots(figsize=(14,7))
    p1 = ax1.plot(eureka_data["DateTime"], eureka_data["Salinity"], color = "brown", label = 'Eureka Salinity')
    p2 = ax1.plot(cal_sal_df['Date'], cal_sal_df["Salinity"], color = "purple", label = 'Calculated Salinity')

    '''
    ax3 = ax1.twinx()
    p4 = ax3.plot(eureka_data["DateTime"], eureka_data["Chlorophyll"], color = "g", label = "Chlorophyll")
    ax3.set_ylabel("Chlorophyll (ug/L)")
    ax3.spines["right"].set_position(("outward", 60))
    ax3.yaxis.label.set_color(p4[0].get_color())

    ax4 = ax1.twinx()
    p5 = ax4.plot(eureka_data["DateTime"], eureka_data["DO"], color = "orange", label = "Dissolved Oxygen")
    ax4.set_ylabel("Dissolved Oxygen (mg/L)")
    ax4.spines["right"].set_position(("outward", 120))
    ax4.yaxis.label.set_color(p5[0].get_color())
    
    ax2 = ax1.twinx()
    p3 = ax2.plot(eureka_data["DateTime"], eureka_data["pH"], color = "b", label = "pH")
    ax2.set_ylabel("pH")
    ax2.spines["right"].set_position(("outward", 0))
    ax2.yaxis.label.set_color(p3[0].get_color())
    '''

    # Sets axis labels
    ax1.set_ylabel("Salinity (PSU)")
    ax1.set_xlabel("Dates (MM-DD)")
    ax1.yaxis.label.set_color(p2[0].get_color())
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=45)

    
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper center', ncol = 3, borderaxespad=4)

    my_path = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(my_path + '\\Eureka_Graphs\\Eureka_Deer_Island_Salinity_Comparison_' + year + '.png')

    plt.show()

# Deer Island 2018 Conductivity
#eureka_grapher("Deer_Island-SG1-2018_Annual_Data.csv", "Eureka 2018 Deer Island (SG1) Conductivity", "01/01/2018", "12/31/2018", "2018")

# Deer Island 2019 Conductivity
#eureka_grapher("Deer_Island-SG1-2019_Annual_Data.csv", "Eureka 2019 Deer Island (SG1) Conductivity", "01/01/2019", "12/31/2019", "2019")

# Deer Island 2018 Multi-Parameter
#eureka_grapher("Deer_Island-SG1-2018_Annual_Data.csv", "Eureka 2018 Deer Island (SG1)", "01/01/2018", "12/31/2018", "2018")

# Deer Island 2019 Multi-Parameter
eureka_grapher("Deer_Island-SG1-2019_Annual_Data.csv", "Eureka 2019 Deer Island (SG1)", "01/01/2019", "12/31/2019", "2019")
