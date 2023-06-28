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

# Used to hold data after outliers are removed
x = None
ty = None
cy = None
by = None

# Used to hold data from csv file  
xData = []      # Dates
tyData = []     # Temperature
cyData = []     # CO2
byData = []     # Battery Voltage

numofLines = 0

ordinalDate = []
timeDate = []
completeDate = []



# Sets the graph layout colors and style
plt.style.use('default')

with open('C:\\Users\\isabe\\Source\\Repos\\icyeung\\pCO2-DataTrue\\pCO2_data\\completeData.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter='\t')
    for row in lines:
        
        # Checks if time entry has corresponding Temperature, CO2, and Battery Voltage
        # If not, does not include data point in graph
        if not row[1] == "" and not row[2] == "" and not row[3] == "" and numofLines > 0:
            xData.append(float(row[0]))
            tyData.append(float(row[1]))
            cyData.append(float(row[2]))
            byData.append(float(row[3]))
            numofLines += 1
        elif numofLines == 0:
            numofLines += 1

# Extracts outliers from dataframe
# If anr value in the 3 colums is a outlier, removes entire row
completeRowData = pd.DataFrame({"Date": xData, "Temp": tyData, "CO2": cyData, "Battery": byData})
completeRowData = completeRowData[(np.abs(stats.zscore(completeRowData)) < 3).all(axis = 1)]

print(stats.zscore(completeRowData))

# Converts Year Day Column to calendar day and time

# Extracts time in HH:MM:SS format from date in Year Day
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

# Converts all dates in Year Day to 0001-MM-DD HH:MM:SS    
for date in xData:
    dt = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(date)), timeConverter(date))
    completeDate.append(dt)


# Allows for more than one set of data to be plotted

# Temperature plot
x = completeRowData.get("Date")     # Plots Dates
ty = completeRowData.get("Temp")       # Plots Temp



fig, ax1 = plt.subplots()
p1 = ax1.plot(x, ty, color = 'b', linestyle = 'solid', label = "Temperature (C)")

# Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)

ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days

ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis

# Sets axis labels and changes font color for easy viewing
ax1.set_ylabel("Temperature (C)")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color(p1[0].get_color())


# CO2 plot
ax2 = ax1.twinx()
cy = completeRowData.get("CO2")       # Plots CO2 
p2 = ax2.plot(x, cy, color = 'r', linestyle = 'solid', label = "CO2")
ax2.set_ylabel("CO2")
ax2.yaxis.label.set_color(p2[0].get_color())

# Battery Voltage plot
by = completeRowData.get("Battery")       # Plots Battery
ax3 = ax1.twinx()
p3 = ax3.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
ax3.set_ylabel("Battery Voltage")
ax3.spines["right"].set_position(("outward", 60))
ax3.yaxis.label.set_color(p3[0].get_color())

 
# Sets title, adds a grid, and shows legend
plt.title('pCO2 Data (2021)', fontsize = 25)
plt.grid(True)
plt.legend(handles=p1+p2+p3)
plt.savefig('pCO2_2021_Graph.png')
plt.show()
