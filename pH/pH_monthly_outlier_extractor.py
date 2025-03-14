from binascii import a2b_base64
from cgi import test
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from scipy import stats
import pytz

from sklearn.preprocessing import MinMaxScaler
from scipy.stats import kstest


def ph_monthly_extractor(file_loc, data_year):

    # Used to find location of specified file within Python code folder
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # pCO2 Data
    # Used to hold data from csv file  
    xData = []      # Dates
    tyData = []     # Temperature
    syData = []     # Salinity
    pyData = []     # pH
    byData = []     # Battery Voltage
    dsData = []     # Date (Calendar)
    tsData = []     # Time 
    date_str_list = []
    time_str_list = []


    # Used in taking out empty data values from pCO2 data
    numofLinesD = 0


    # Outliers
    # Holds information on outliers
    outlierData = []
    outlierDataSal = []

    # Used in taking out empty values from salinity data
    numofLinesS = -1

    # Used for creating table on outlier information
    headersH = ["# Values Before Outliers Extracted", "# Values After Outliers Extracted", "# Outliers Extracted"]                          # Horizontal Headers
    headersV = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]   # Vertical Headers

    # Time
    # Holds converted time values
    xDataTrueO =[]      # Outlier times
    xDataTrueNO = []    # No outlier times


    # Sourced from https://pythonhow.com/how/check-if-a-string-is-a-float/
    # Used to check if data is a numeric value
    def is_float(string):
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False
        


    # Takes out empty data values in pCO2 data set
    with open(os.path.join(__location__, file_loc),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter='\t')
        for row in lines:
            
            # Checks if time entry has corresponding Temperature, Salinity, pH, Battery Voltage, Calendar Date, and Time
            # If not, does not include data point in graph
            if not row[1] == "" and is_float(row[1]) and not row[2] == "" and is_float(row[2]) and not row[3] == "" and is_float(row[3]) and float(row[3]) != 0.00 and not row[4] == "" and is_float(row[4]) and numofLinesD > 0:
                xData.append(float(row[0]))
                tyData.append(float(row[1]))
                syData.append(float(row[2]))
                pyData.append(float(row[3]))
                byData.append(float(row[4]))
                date_str_list.append(row[5])
                time_str_list.append(row[6])
                numofLinesD += 1
            elif numofLinesD == 0:
                numofLinesD += 1

    # Displays total number of data points before outliers are taken out
    print("Original data after empty values are taken out: ", len(xData))

    # Dataframe of original data after blanks removed
    completeRowData = pd.DataFrame({"Date": xData, "Temp": tyData, "ConstSal": syData, "pH": pyData, "Battery": byData, "DateStr": date_str_list, "TimeStr": time_str_list})

    # Sourced from https://www.analyticsvidhya.com/blog/2022/09/dealing-with-outliers-using-the-iqr-method/
    def IQR(dfName):
        percentile25 = dfName["pH"].quantile(0.25)
        percentile75 = dfName["pH"].quantile(0.75)
        iqr = percentile75 - percentile25
        upperLimit = percentile75 + 1.5*iqr
        lowerLimit = percentile25 - 1.5*iqr
        noOutliersDf = dfName[(dfName["pH"] < upperLimit) & (dfName["pH"] > lowerLimit)]
        return noOutliersDf

    # Extracts outliers from dataframe
    # If any value in the 3 colums is an outlier, removes entire row
    # Stores information about # of outliers taken out
    # Input start and end dates of desired outlier identification time frame in Ordinal form
    def extractOutliers(start, end, intervalName):
        outlierDataHolder = []
        intervalDf = completeRowData.loc[(completeRowData['Date'] >= start) & (completeRowData['Date'] < end)]
        bOutliers = len(intervalDf.get('Date'))        # Number of datapoints before outliers are removed
        outlierDataHolder.append(bOutliers)
        noOutliersDf = IQR(intervalDf)     
        aOutliers = len(noOutliersDf.get('Date'))      # Number of datapoints after outliers are removed
        outlierDataHolder.append(aOutliers)
        nOutliers = bOutliers - aOutliers              # Number of outliers
        outlierDataHolder.append(nOutliers)
        outlierData.append(outlierDataHolder)
        return noOutliersDf

    # Identifies and extracts outliers using a monthly interval
    januaryDf = extractOutliers(1, 32, "January")
    februaryDf = extractOutliers(32, 60, "February")
    marchDf = extractOutliers(60, 91, "March")
    aprilDf = extractOutliers(91, 121, "April")
    mayDf = extractOutliers(121, 152, "May")
    juneDf = extractOutliers(152, 182, "June")
    julyDF = extractOutliers(182, 213, "July")
    augustDf = extractOutliers(213, 244, "August")
    septemberDf = extractOutliers(244, 274, "September")
    octoberDf = extractOutliers(274, 305, "October")
    novemberDf = extractOutliers(305, 335, "November")
    decemberDf = extractOutliers(335, 366, "December")

    # Displays table with # of outliers taken out per month
    print("")
    print(pd.DataFrame(outlierData, headersV, headersH))
    print("")

    # Dataframe without outliers
    extractedData = pd.concat([januaryDf, februaryDf, marchDf, aprilDf, mayDf, juneDf, julyDF, 
                            augustDf, septemberDf, octoberDf, novemberDf, decemberDf])
    
    # Displays total number of data points after outliers are removed
    print("Original data after all outliers are removed: ", len(extractedData.get("Date")))

    # Display number of outliers
    print("Number of outliers: ", (len(xData) - (len(extractedData.get("Date")))))


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

    # Converts all dates in Year Day to 2021-MM-DD HH:MM:SS
    # Original Data    
    for dateValue in xData:
        dateValue = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(dateValue)), timeConverter(dateValue))
        trueDate = dateValue.replace(year = data_year)
        xDataTrueO.append(trueDate)

    # Data with no outliers
    for dateValue in extractedData.get("Date"):
        dateValue = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(dateValue)), timeConverter(dateValue))
        trueDate = dateValue.replace(year = data_year)
        xDataTrueNO.append(trueDate)





    # Creates dataframes of data grapher without outliers
    pHDF = pd.DataFrame({"Year Day": extractedData.get("Date"), "Temperature C": extractedData.get("Temp"), "SalinityConst": extractedData.get("ConstSal"),
                        "pHConstSal": extractedData.get("pH"), "Battery Voltage": extractedData.get("Battery"), "DateStr": extractedData.get("DateStr"),
                        "TimeStr": extractedData.get("TimeStr"), "Date (UTC)": xDataTrueNO})


    # Saves dataframes to csv files


    pHDF['Date (UTC)'] = pd.to_datetime(pHDF['Date (UTC)'])

    #pHDF.to_csv("pH_2019_Complete_Annual_Data_NO.csv", index = None)
    # Histogram of CO2 measurements
    # plt.hist(extractedData.get("pH"), edgecolor='black', bins=20)
    # plt.hist(extractedData.get("Temp"), edgecolor='black', bins=20)
    #plt.hist(extractedData.get("Battery"), edgecolor='black', bins=20)

    '''
    # K-S test
    print(kstest(extractedData.get("pH"), 'norm'))     # Not normally distributed
    print(kstest(extractedData.get("Temp"), 'norm'))    # Not normally distributed
    print(kstest(extractedData.get("Battery"), 'norm')) # Not normally distributed
    '''

    def grapher(time, tempC, pH, batteryV, name):
        x = time
        ty = tempC
        py = pH
        by = batteryV

        fig, ax1 = plt.subplots(figsize=(14,7))
        #fig.subplots_adjust(right = 0.75)
        p1 = ax1.plot(x, ty, color = 'm', linestyle = 'solid', label = 'Temperature (C)')

        # Sets x-axis as Dates
        date_form = DateFormatter("%m-%d")
        ax1.xaxis.set_major_formatter(date_form)
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
        ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis

        
        # Sets axis labels and changes font color of "Temperature (C)" label for easy viewing
        ax1.set_ylabel("Temperature (C)")
        ax1.set_xlabel("Dates (MM-DD)")
        ax1.yaxis.label.set_color(p1[0].get_color())

        
        # pH plot
        ax2 = ax1.twinx()
        p2 = ax2.plot(x, py, color = 'c', linestyle = 'solid', label = "pH")
        ax2.set_ylabel("pH")
        ax2.yaxis.label.set_color(p2[0].get_color())
        
        '''
        # Battery Voltage plot
        ax3 = ax1.twinx()
        p3 = ax3.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
        ax3.set_ylabel("Battery Voltage")
        ax3.spines["right"].set_position(("outward", 60))
        ax3.yaxis.label.set_color(p3[0].get_color())
        '''
        
        '''
        # Salinity plot
        ax4 = ax1.twinx()
        p4 = ax4.plot(x, by, color = 'k', linestyle = 'solid', label = "Salinity")
        ax4.set_ylabel("Salinity")
        ax4.spines["right"].set_position(("outward", 120))
        ax4.yaxis.label.set_color(p4[0].get_color())
        '''
    
        
        # Sets title, adds a grid, and shows legend
        plt.title(name, fontsize = 20)
        plt.grid(True)
        plt.legend(handles=p1+p2)

        return

    # Plots graph without outliers
    grapher(xDataTrueNO, extractedData.get("Temp"), extractedData.get("pH"), extractedData.get("Battery"), 
            str(data_year) + " pH Data (No Outliers) Monthly")

    # Finds location of .py program
    my_path = os.path.dirname(os.path.abspath(__file__))


    # Saves without outliers graph to specified name in folder
    #plt.savefig(my_path + '\\pH_Graphs\\pH_2023_Graph_No_Outliers_Monthly.png')

    # Plots graph with outliers
    grapher(xDataTrueO, tyData, pyData, byData, str(data_year) + " pH Data (With Outliers) Monthly")


    # Saves with outliers graph to specified name in folder
    #plt.savefig(my_path + '\\pH_Graphs\\pH_2023_Graph_With_Outliers_Monthly.png')

    # Displays figures
    plt.show()

    '''
    # Scaling data
    # scaled point = (x-min)/(max-min)
    # Input data that is to be scaled and empty list that scaled data is saved in
    def minMax(data, output):
        for point in data:
            scaledValue = (point-min(data))/(max(data)-min(data))
            output.append(scaledValue)

    scaledValuePH = []
    scaledValueTemp = []
    scaledValueBattery = []
    #scaledValueSalinity = []


    # Dataframe only contains scaled values
    minMax(extractedData.get("pH"), scaledValuePH)
    minMax(extractedData.get("Temp"), scaledValueTemp)
    minMax(extractedData.get("Battery"), scaledValueBattery)
    #minMax(extractedData.get("Salinity"), scaledValueSalinity)


    phDFscaled = pd.DataFrame({"Date": xDataTrueNO, "Temperature (C)": scaledValueTemp, "pH": scaledValuePH, 
                                "Battery": scaledValueBattery})
    '''


ph_monthly_extractor("SAMI_pH\\pH_Annual_Compiled_Data\\pH_2023_Complete_Data.csv", 2023)