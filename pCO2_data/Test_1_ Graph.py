import os
from runpy import _TempModule
from xmlrpc.client import DateTime, _datetime
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from scipy import stats

# Used to find location of specified file within Python code folder
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# pCO2 Data
# Used to hold data from csv file  
xData = []      # Dates
tyData = []     # Temperature
cyData = []     # CO2
byData = []     # Battery Voltage

# Used in taking out empty data values from pCO2 data
numofLinesD = 0

# Weather Data
# Used to hold weather data from csv file
weaDate = []
wyData = []
ryData = []

# Used in taking out empty data values from weather data
numofLinesW = 0

# Outliers
# Holds information on outliers
outlierData = []

# Used for creating table on outlier information
headersH = ["# Values Before Outliers Extracted", "# Values After Outliers Extracted", "# Outliers Extracted"]                          # Horizontal Headers
headersV = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]   # Vertical Headers

# Time
# Holds converted time values
xDataTrueO =[]      # Outlier times
xDataTrueNO = []    # No outlier times
weaDateTrue =[]     # Weather times

# Takes out empty data values in pCO2 data set
with open(os.path.join(__location__, 'completeData.csv'),'r') as csvfile:
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
print("Original data after empty values are taken out: ", len(xData))

# Dataframe of original data after blanks removed
completeRowData = pd.DataFrame({"Date": xData, "Temp": tyData, "CO2": cyData, "Battery": byData})

# Takes out empty values in weather data set
with open(os.path.join(__location__, '2021_Barlow_Weather_Data_Formatted.csv'),'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        
        # Checks if time entry has corresponding Temperature, CO2, and Battery Voltage
        # If not, does not include data point in graph
        if not row[11] == "" and not row[15] == "" and numofLinesW > 0:
            weaDate.append(row[0])
            wyData.append(float(row[11]))
            ryData.append(float(row[15]))
            numofLinesW += 1
        elif numofLinesW == 0:
            numofLinesW += 1


# Extracts outliers from dataframe
# If any value in the 3 colums is an outlier, removes entire row
# Stores information about # of outliers taken out
def extractOutliers(start, end, intervalName):
    outlierDataHolder = []
    intervalDf = completeRowData.loc[(completeRowData['Date'] >= start) & (completeRowData['Date'] < end)]
    bOutliers = len(intervalDf.get('Date'))        # Number of datapoints before outliers are removed
    outlierDataHolder.append(bOutliers)
    noOutliersDf = intervalDf[(np.abs(stats.zscore(intervalDf)) < 3).all(axis = 1)]     # Removes points greater than 3 standard deviations
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
extractedData = pd.concat([januaryDf, februaryDf, marchDf, aprilDf, mayDf, juneDf, julyDF, augustDf, septemberDf, octoberDf, novemberDf, decemberDf])
 
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
    trueDate = dateValue.replace(year = 2021)
    xDataTrueO.append(trueDate)

# Data with no outliers
for dateValue in extractedData.get("Date"):
    dateValue = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(dateValue)), timeConverter(dateValue))
    trueDate = dateValue.replace(year = 2021)
    xDataTrueNO.append(trueDate)

# Weather data    
for dateValue in weaDate:
    trueDate = datetime.datetime.strptime(dateValue, '%m/%d/%Y').date()
    weaDateTrue.append(trueDate)
  

# Graph plotter function
# Provide date, temperature, CO2, and battery data
# Provide weather dates, wind, and rain data
# Provide name of graph in string format 
def grapher(time, tempC, CO2, batteryV, weatherD, wind, rain, name):
    x = time
    ty = tempC
    cy = CO2
    by = batteryV
    wx = weatherD
    wy = wind
    ry = rain

    fig, ax1 = plt.subplots()
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

    # CO2 plot
    ax2 = ax1.twinx()
    p2 = ax2.plot(x, cy, color = 'c', linestyle = 'solid', label = "CO2")
    ax2.set_ylabel("CO2")
    ax2.yaxis.label.set_color(p2[0].get_color())

    # Battery Voltage plot
    ax3 = ax1.twinx()
    p3 = ax3.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
    ax3.set_ylabel("Battery Voltage")
    ax3.spines["right"].set_position(("outward", 60))
    ax3.yaxis.label.set_color(p3[0].get_color())

    # Wind Speed plot
    ax4 = ax1.twinx()
    p4 = ax4.plot(wx, wy, color = 'b', linestyle = 'solid', label = "Average Wind Speed (mph)")
    ax4.set_ylabel("Average Wind Speed (mph)")
    ax4.spines["right"].set_position(("outward", 120))
    ax4.yaxis.label.set_color(p4[0].get_color())

    # Rainfall plot
    ax5 = ax1.twinx()
    p5 = ax5.plot(wx, ry, color = 'r', linestyle = 'solid', label = "Rainfall (in)")
    ax5.set_ylabel("Rainfall (in)")
    ax5.spines["right"].set_position(("outward", 180))
    ax5.yaxis.label.set_color(p5[0].get_color())

    # Sets title, adds a grid, and shows legend
    plt.title(name, fontsize = 20)
    plt.grid(True)
    plt.legend(handles=p1+p2+p3+p4+p5)

    return

# Plots graph without outliers
grapher(xDataTrueNO, extractedData.get("Temp"), extractedData.get("CO2"), extractedData.get("Battery"), weaDateTrue, wyData, ryData, "2021 pCO2 Data (No Outliers)")

# Saves without outliers graph to specified name in pCO2_data folder
plt.savefig('pCO2_2021_Graph_No_Outliers.png')

# Plots graph with outliers
grapher(xDataTrueO, tyData, cyData, byData, weaDateTrue, wyData, ryData, "2021 pCO2 Data (With Outliers)")

# Saves with outliers graph to specified name in pCO2_data folder
plt.savefig('pCO2_2021_Graph_With_Outliers.png')

# Displays figures
plt.show()