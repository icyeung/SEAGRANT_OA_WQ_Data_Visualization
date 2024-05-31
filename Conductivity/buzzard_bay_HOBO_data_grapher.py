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

# saves csv as dataframe
# sorts by station
# checks start date & end date
# if there is no valid start or end date, uses entire time frame
# 

def commonDataRange(date, start_date, end_date):
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
'''    
def HOBO_grapher(file):
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


    # Takes out empty values in salinity data set
    with open(os.path.join(__location__, file)) as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            print(row)
      
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if numofLinesS > 1:
                if not row[0] == "-" and not row[1] == "-" and not row[2] == "-" and not row[0] == "" and not row[1] == "" and not row[2] == "":
                    salDate.append(row[0])
                    print(row[0])
                    condData.append(float(row[1]))
                    condTempData.append(float(row[2]))
                    numofLinesS += 1
            elif numofLinesS <= 1:
                numofLinesS += 1
            
    print(salDate)

    # Salinity data
    for time in salDate:
        timeObj = dt.strptime(time, '%m/%d/%y %H:%M:%S')
        eastern = pytz.timezone('US/Eastern')
        realTimeObj = timeObj.astimezone(eastern)       # Converts time from GMT to EST
        salDateTrue.append(realTimeObj)


    unrefinedCondData = pd.DataFrame({'Date': salDateTrue, 'Conductiviy': condData, 'Temperature (F)': condTempData})


    # Verified Measurement also has to be between 5000, 55000
    # If not, does not include data point in graph
    for index in range(0, len(salDateTrue)):
        if (condData[index] <= 5000) or (condData[index] >= 55000):
            unrefinedCondData = unrefinedCondData.drop(index)
    unrefinedCondData = unrefinedCondData.reset_index(drop=True)

    condTempDataC = []

    for temp in unrefinedCondData["Temperature (F)"]:
        tempC = (temp-32)/1.8
        condTempDataC.append(tempC)
    unrefinedCondData["Temperature (C)"] = condTempDataC


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
    for i in range(len(condData)):
        salinity = condSalConv(condData[i-1], condTempDataC[i-1])
        #print(salinity)
    
        if salinity != "":
            salinity = round(float(salinity), 3)
    
        convertedSalinityData.append(salinity)
        usedTemperature.append(condTempDataC[i-1])
        usedConductivity.append(condData[i-1])


    # Remove outliers by taking 10% of the regression line
    # Use Julian Days for the time    
    #print('salDate length', len(salDate))
    #print("salDateTrue length", len(salDateTrue))

    salDateTrueJulian = salDateTrue.copy()

    # Converts dates to ints
    # Not used as there are jumps due to the date format not being continuous as an int


    salDateJulian = []
    #salDateJulianHolder = []
    for date in salDateTrueJulian:
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second
        ts = pd.Timestamp(year, month, day, hour, second)
        jd = ts.to_julian_date()
        salDateJulian.append(jd)
        print(salDateJulian)

        #print("length of salDateInt", len(salDateInt))
        #print("length of salDateTrueOrdinal", len(salDateTrueOrdinal))

        salDateTrueOrdinalAry = np.array(salDateJulian)
        #salDateTrueOrdinal.toArray(salDateTrueOrdinalAry)

        condDataOR = usedConductivity.copy()
        condDataAry = np.array(condDataOR)
        #condData.toArray(condDataAry)

        dateStringUnrefinedCondData = pd.DataFrame({'Date': salDateTrueJulian, 'Conductiviy': condData, 'Temperature (C)': condTempData})   
        model = LinearRegression().fit(salDateTrueOrdinalAry.reshape(-1,1), condDataAry)
        r_sq = model.score(salDateTrueOrdinalAry.reshape(-1,1), condDataAry)
        print("intercept", model.intercept_)
        print("slope", model.coef_)
        #print('coefficient of determination:', r_sq)
        condDataFitPredList=[]
        for date in salDateJulian:
            condDataFitPredList.append((model.coef_*date)+model.intercept_)
        #condDataFitPredAry = model.predict(salDateTrueOrdinalAry.reshape(-1,1))
        #print("fit tester", condDataFitPredAry)

        #condDataFitPredList = condDataFitPredAry.tolist()
        print(len(salDateTrueJulian))
        print('before cutting', len(condDataFitPredList))

        #print("list", condDataFitPredList)

        # Salinity dataframe to remove null values
        salinityDF = pd.DataFrame({'Date': salDateTrue, 'Salinity Value': convertedSalinityData, 'Temperature (C)': usedTemperature, 'Conductivity': usedConductivity,
                                    'Fit': condDataFitPredList})
        print(len(salDateTrue))
        #print(salinityDF)


    # Removes all rows with null salinity

    # print(salinityDFSorted)

    salinityDF_copy = pd.DataFrame({'Date': salDateTrue, 'Salinity Value': convertedSalinityData, 'Temperature (C)': usedTemperature, 'Conductivity': usedConductivity,
                          'Fit': condDataFitPredList})
    salinityDFSortedNOreset = salinityDF_copy.reset_index(drop=True)
    #print(salinityDFSortedNOreset)

    print(len(condDataOR))
    if (len(condDataOR) == len(condDataFitPredList)):
        for index in range(0, len(condDataOR)):
            #print(condDataFitPredList[index])
            max_bound = condDataFitPredList[index]*1.1
            #print("max", max_bound)
            min_bound = condDataFitPredList[index]*0.9
            #print("min", min_bound)
            #print('data', condDataOR[index])
            if (condDataOR[index] < min_bound) or (condDataOR[index] > max_bound):
                salinityDFSortedNOreset = salinityDFSortedNOreset.drop(index)
                #print("hi")

    salinityDFSorted = salinityDF.loc[salinityDF['Salinity Value'] != ""]
    salinityDFSortedNOreset = salinityDFSortedNOreset.loc[salinityDFSortedNOreset['Salinity Value'] != ""]

    print('after cutting', len(salinityDFSortedNOreset.get("Date")))
    return salinityDFSortedNOreset
'''





def buzzard_bay_grapher(file, station, title, start_date, end_date, year, HOBO_file1, HOBO_file2, HOBO_file3, HOBO_file4):

    numofLinesS = 0
    raw_date_list = []
    raw_time_list = []
    temp_list = []
    salinity_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    file_BB = "Buzzards_Bay_Data\\" + file

    with open(os.path.join(__location__, file_BB),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            #print(row)
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[1] == "" and not row[3] == "" and not row[10] == "" and not row[19] == "" and not row[21] == "" and numofLinesS > 0:
                if row[1] == station:
                    #print("hi")
                    if commonDataRange(row[3], start_date, end_date):
                        raw_date_list.append(row[3])
                        raw_time_list.append(row[10])
                        temp_list.append(float(row[19]))
                        salinity_list.append(float(row[21]))
                        numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1
    
    print(raw_date_list)

    def timeConverterto24(time):
        ending = time.split(" ")[-1]
        time_number = time.split(" ")[0]
        h1, m1 = [int(number) for number in time_number.split(":")]
        if ending == "PM" and h1 != 12:
            h1 += 12
        if ending == "AM" and h1 == 12:
            h1 = 0
        converted_time = str(h1) + ":" + str(m1)
        converted_time_dt = dt.strptime(converted_time, "%H:%M")
        return converted_time_dt

    BB_data_time_converted_list = []
    for time in raw_time_list:
        BB_data_time_converted_list.append(timeConverterto24(time))
    #print("time", NOAA_tidal_data_time_converted_list)

    BB_data_date_converted_list = []    
    for date in raw_date_list:
        BB_data_date_converted_list.append(dt.strptime(date, "%m/%d/%Y"))
    #print("date", NOAA_tidal_data_date_converted_list)

    if len(BB_data_date_converted_list) == len(BB_data_time_converted_list):
        print("yayyyyy")
    else:
        print("OOps", "date", len(BB_data_date_converted_list), "time", len(BB_data_time_converted_list))

    print(BB_data_date_converted_list)


    BB_data_datetime_combined_list = []
    for index in range(0, len(BB_data_date_converted_list)):
        BB_data_datetime_combined_list.append(dt.combine(BB_data_date_converted_list[index], BB_data_time_converted_list[index].time()))

    BB_df = pd.DataFrame({"DateTime": BB_data_datetime_combined_list, "Temperature": temp_list, "Salinity": salinity_list})
    
    HOBO_1_part1 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file1), delimiter=",")

    HOBO_1_part2 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file2), delimiter=",")

    HOBO_2_part1 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file3), delimiter=",")

    HOBO_2_part2 = pd.read_csv(os.path.join(__location__, "Conductivity_Data_NO\\" + HOBO_file4), delimiter=",")

    def convertTime(df):
        graphingTime = []
        for date in df["Date"]:
            dateNew = date[:-6]
            print(dateNew)
            graphingTime.append(dateNew)
        df["Date (Corrected)"] = graphingTime
        return(df)

    HOBO_1_part1_fx = convertTime(HOBO_1_part1)
    #print(HOBO_1_part1_fx)
    HOBO_1_part2_fx = convertTime(HOBO_1_part2)
    HOBO_2_part1_fx = convertTime(HOBO_2_part1)
    HOBO_2_part2_fx = convertTime(HOBO_2_part2)
    
    HOBO1_data_time_converted_list = []
    for date in HOBO_1_part1["Date (Corrected)"]:
        print(HOBO_file1)
        print("hi", date)
        HOBO1_data_time_converted_list.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_1_part1_fx["Date (DT)"] = HOBO1_data_time_converted_list

    '''
    HOBO2_data_time_converted_list = []
    for date in HOBO_2_part1["Date (Corrected)"]:
        #print(HOBO_file1)
        print("hi", date)
        HOBO2_data_time_converted_list.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_2_part1_fx["Date (DT)"] = HOBO2_data_time_converted_list

    HOBO1_data_time_converted_list_2 = []
    for date in HOBO_1_part2["Date (Corrected)"]:
        #print(HOBO_file1)
        print("hi", date)
        HOBO1_data_time_converted_list_2.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_1_part2_fx["Date (DT)"] = HOBO1_data_time_converted_list_2

    HOBO2_data_time_converted_list_2 = []
    for date in HOBO_2_part2["Date (Corrected)"]:
        #print(HOBO_file1)
        print("hi", date)
        HOBO2_data_time_converted_list_2.append(dt.strptime(date, "%Y-%m-%d %H:%M:%S"))
    HOBO_2_part2_fx["Date (DT)"] = HOBO2_data_time_converted_list_2
    '''
    fig, ax1 = plt.subplots(figsize=(14,7))
    p1 = ax1.plot(BB_df["DateTime"], BB_df["Salinity"], color = "g", linestyle = 'solid', label = 'BB', linewidth=0.75)
    p2 = ax1.plot(HOBO_1_part1_fx["Date (DT)"], HOBO_1_part1_fx["Salinity Value"], color = 'b', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
    #p3 = ax1.plot(HOBO_2_part1_fx["Date (DT)"], HOBO_2_part1_fx["Salinity Value"], color = 'r', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
    #p4 = ax1.plot(HOBO_1_part2_fx["Date (DT)"], HOBO_1_part2_fx["Salinity Value"], color = 'cyan', linestyle = '-', label = "HOBO #1", linewidth = 0.75)
    #p5 = ax1.plot(HOBO_2_part2_fx["Date (DT)"], HOBO_2_part2_fx["Salinity Value"], color = 'orange', linestyle = '-', label = "HOBO #2", linewidth = 0.75)
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
    #ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "pco2" label for easy viewing
    ax1.set_ylabel("Salinity (%.)")
    ax1.set_xlabel("Dates (MM-DD)")
    ax1.yaxis.label.set_color("k")
    #ax1.legend()  

    #ax2 = ax1.twinx()
    #p13 = ax2.plot(BB_df["DateTime"], BB_df["Salinity"], color = 'g', linestyle = 'solid', label = 'Temperature')
    #ax2.set_ylabel("Temperature (C)")
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(title, loc='center')
    fig.legend(loc = 'upper right', ncol = 3, borderaxespad=4)


    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves without outliers graph to specified name in folder
    plt.savefig(my_path + '\\BB_vs_HOBO_' + station + '_' + year + '.png')
    plt.show()



#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "FC1X", "Buzzard's Bay Salinity: Fiddler's Cove (FC1X) vs HOBO 2021", "1/1/2021", "12/31/2021", "2021", "Salinity_Carolina_FiddlersCove_9-28-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")

buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2022", "1/1/2022", "12/31/2022", "2022", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")

#buzzard_bay_grapher("bbcdata1992to2023-ver23May2024-export_FC_PR.csv", "PR1", "Buzzard's Bay Salinity: Pocasset River (PR1) 2023", "1/1/2023", "12/31/2023", "2023", "Salinity_Carolina_Pocasset_12_9_22_1_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv", "Salinity_Carolina_FiddlersCove_9-28-21_2_NO.csv", "Salinity_Carolina_FiddlersCove_12-10-21_2_NO.csv")

