import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# Plot once every 10 lines of data
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

'''
boxplotData = pd.DataFrame({"Date": xData, "Temp": tyData, "CO2": cyData, "Battery": byData})
categorical_col = ["Date"]
numeric_col = ["Temp", "CO2", "Battery"]


boxplotData.boxplot(numeric_col)

for x in ["Date"]:
    q75,q25 = np.percentile(boxplotData.loc[:,x],[75,25])
    intr_qr = q75-q25
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)

    boxplotData.loc[boxplotData[x] < min,x] = np.nan
    boxplotData.loc[boxplotData[x] > max,x] = np.nan

print(boxplotData.isnull().sum())

boxplotData = boxplotData.dropna(axis = 0)

print(boxplotData.isnull().sum())


for x in ["Temp"]:
    q75,q25 = np.percentile(boxplotData.loc[:,x],[75,25])
    intr_qr = q75-q25
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)

    boxplotData.loc[boxplotData[x] < min,x] = np.nan
    boxplotData.loc[boxplotData[x] > max,x] = np.nan

print(boxplotData.isnull().sum())

tyData = boxplotData.dropna(axis = 0)

print(boxplotData.isnull().sum())


#boxplotDataT = pd.DataFrame({"CO2": cyData})
#ax = boxplotDataT[['CO2']].plot(kind='box', title='Outlier Visualizer (C)')

#boxplotDataT = pd.DataFrame({"Battery": byData})
#ax = boxplotDataT[['Battery']].plot(kind='box', title='Outlier Visualizer (B)')


# Outlier Removal Sourced From: https://www.askpython.com/python/examples/detection-removal-outliers-in-python

#DATA = pd.read_csv('C:\\Users\\isabe\\Source\\Repos\\icyeung\\pCO2-DataTrue\\pCO2_data\\completeData.csv')
#lines = csv.reader(DATA, delimiter='\t')
#categorical_col = ["Year Day"]
#numeric_col = ["Temparature C", "CO2", "Battery Voltage"]

#DATA.dtypes

#DATA.boxplot(["Temperature C"])

#for x in ["Date"]:
#    q75,q25 = np.percentile(DATA.loc[:,x],[75,25])
#    intr_qr = q75-q25
#    max = q75+(1.5*intr_qr)
#    min = q25-(1.5*intr_qr)

#    DATA.loc[DATA[x] < min,x] = np.nan
#    DATA.loc[DATA[x] > max,x] = np.nan

#print(DATA.isnull().sum())

#DATA = DATA.dropna(axis = 0)

#print(DATA.isnull().sum())

'''



# Converts Year Day Column to calendar day and time
time = ""

def timeConverter (date):
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
    
for date in xData:
    #ordinalDate.append(datetime.date.fromordinal(math.trunc(date)))
    #timeDate.append(timeConverter(date))
    dt = datetime.datetime.combine(datetime.date.fromordinal(math.trunc(date)), timeConverter(date))
    completeDate.append(dt)

    #completeDate.append(datetime.datetime.combine(datetime.date.fromordinal(math.trunc(date)), timeConverter(date)))

#print(completeDate)

# Makes graph wider so Dates can be viewed properly
# Causes blank Figure 1 to open
#plt.figure().set_figwidth(60)

# Allows for more than one set of data to be plotted

# Temperature plot
x = completeDate[::5]     # Plots once every 10 data lines
ty = tyData[::5]       # Plots once every 10 data lines


#xRange=range(len(x))

fig, ax1 = plt.subplots()
p1 = ax1.plot(x, ty, color = 'b', linestyle = 'solid', label = "Temperature (C)")

# Sets x-axis as Dates

date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)

ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))     # Step size of 1
#ax1.set_xticklabels(ax1.get_xticks(), rotation = 90)        # Rotates dates to be perpendiculat to x-axis

ax1.xaxis.set_minor_locator(mdates.DayLocator())

# Sets axis labels and changes font color for easy viewing
ax1.set_ylabel("Temperature (C)")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color(p1[0].get_color())


# CO2 plot
ax2 = ax1.twinx()
cy = cyData[::5]       # Plots once every 10 data lines
p2 = ax2.plot(x, cy, color = 'r', linestyle = 'solid', label = "CO2")
ax2.set_ylabel("CO2")
ax2.yaxis.label.set_color(p2[0].get_color())

# Battery Voltage plot
by = byData[::5]       # Plots once every 10 data lines
ax3 = ax1.twinx()
p3 = ax3.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
ax3.set_ylabel("Battery Voltage")
ax3.spines["right"].set_position(("outward", 60))
ax3.yaxis.label.set_color(p3[0].get_color())

  
# Sets title, adds a grid, and shows legend
plt.title('pCO2 Data (2021)', fontsize = 25)
plt.grid(True)
plt.legend(handles=p1+p2+p3)

plt.show()