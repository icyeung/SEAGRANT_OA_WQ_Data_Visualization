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
from scipy.stats import kstest



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



# Takes out empty data values in pCO2 data set
with open(os.path.join(__location__, 'SAMI_pCO2\\pCO2_Annual_Compiled_Data\\pCO2_2023_Complete_Data.csv'),'r') as csvfile:
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


# Sourced from https://www.analyticsvidhya.com/blog/2022/09/dealing-with-outliers-using-the-iqr-method/
def IQR(dfName):
    percentile25 = dfName["CO2"].quantile(0.25)
    percentile75 = dfName["CO2"].quantile(0.75)
    iqr = percentile75 - percentile25
    upperLimit = percentile75 + 1.5*iqr
    lowerLimit = percentile25 - 1.5*iqr
    noOutliersDf = dfName[(dfName["CO2"] < upperLimit) & (dfName["CO2"] > lowerLimit)]
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
    noOutliersDf = IQR(completeRowData)
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
#extractedData = pd.concat([januaryDf, februaryDf, marchDf, aprilDf, mayDf, juneDf, julyDF, augustDf, septemberDf, octoberDf, novemberDf, decemberDf])
 
extractedData = januaryDf

print(januaryDf)

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
    trueDate = dateValue.replace(year = 2023)
    xDataTrueO.append(trueDate)

# Data with no outliers
for dateValue in extractedData.get("Date"):
    dateValue = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(dateValue)), timeConverter(dateValue))
    trueDate = dateValue.replace(year = 2023)
    xDataTrueNO.append(trueDate)





# Creates dataframes of data grapher without outliers
pco2DF = pd.DataFrame({"Year Day": extractedData.get("Date"), "Temperature C": extractedData.get("Temp"), 
                       "CO2": extractedData.get("CO2"), "Battery": extractedData.get("Battery"), "Date (UTC)": xDataTrueNO})


# Saves dataframes to csv files


pco2DF['Date (UTC)'] = pd.to_datetime(pco2DF['Date (UTC)'])

print(pco2DF)

#pco2DF.to_csv("pCO2_2023_Complete_Annual_Data_NO_1.csv", index=None)
# Histogram of CO2 measurements
# plt.hist(extractedData.get("CO2"), edgecolor='black', bins=20)
# plt.hist(extractedData.get("Temp"), edgecolor='black', bins=20)
# plt.hist(extractedData.get("Battery"), edgecolor='black', bins=20)

# K-S test
# print(kstest(extractedData.get("CO2"), 'norm'))     # Not normally distributed
# print(kstest(extractedData.get("Temp"), 'norm'))    # Not normally distributed
# print(kstest(extractedData.get("Battery"), 'norm')) # Not normally distributed


def grapher(time, tempC, CO2, batteryV, name):
    x = time
    ty = tempC
    cy = CO2
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

   
    
    # Sets title, adds a grid, and shows legend
    plt.title(name, fontsize = 20)
    plt.grid(True)
    plt.legend(handles=p1+p2+p3)

    return

# Plots graph without outliers
grapher(xDataTrueNO, extractedData.get("Temp"), extractedData.get("CO2"), extractedData.get("Battery"), 
        "2023 pCO2 Data (No Outliers)")

# Finds location of .py program
my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
#plt.savefig(my_path + '\\pCO2_Graphs\\Only_pCO2_2023_Graph_No_Outliers_Monthly.png')

# Plots graph with outliers
grapher(xDataTrueO, tyData, cyData, byData, "2023 pCO2 Data (With Outliers)")

# Saves with outliers graph to specified name in folder
#plt.savefig(my_path + '\\pCO2_Graphs\\Only_pCO2_2023_Graph_With_Outliers.png')


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

scaledValueCO2 = []
scaledValueTemp = []
scaledValueBattery = []


# Dataframe only contains scaled values
minMax(extractedData.get("CO2"), scaledValueCO2)
minMax(extractedData.get("Temp"), scaledValueTemp)
minMax(extractedData.get("Battery"), scaledValueBattery)


pco2DFscaled = pd.DataFrame({"Date": xDataTrueNO, "Temperature (C)": scaledValueTemp, "CO2": scaledValueCO2, 
                             "Battery": scaledValueBattery})
'''




