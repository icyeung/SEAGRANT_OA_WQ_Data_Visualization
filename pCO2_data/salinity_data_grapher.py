import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import math
import datetime
import pytz
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates



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

# os.path.join(__location__, 'Salinity_2021.csv'
# Takes out empty values in salinity data set
with open(os.path.join(__location__, 'Carolina_June_2021.csv'),'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        
        # Checks if time entry has corresponding Time and Verified Measurement
        # If not, does not include data point in graph
        if not row[1] == "-" and not row[2] == "-" and not row[3] == "-" and not row[1] == "" and not row[2] == "" and not row[3] == "" and numofLinesS > 0:
            salDate.append(row[1])
            condData.append(float(row[2]))
            condTempData.append(float(row[3]))
            numofLinesS += 1
        elif numofLinesS <= 0:
            numofLinesS += 1
            

# Salinity data
for time in salDate:
    timeObj = datetime.datetime.strptime(time, '%m/%d/%Y %H:%M')
    eastern = pytz.timezone('US/Eastern')
    realTimeObj = timeObj.astimezone(eastern)       # Converts time from GMT to EST
    salDateTrue.append(realTimeObj)



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
    
        

# Converts all conductivity and temperature measurements to salinity
# Rounds salinity conversions to 3 decimal places
for i in range(len(condData)):
    salinity = condSalConv(condData[i-1], condTempData[i-1])
    
    if salinity != "":
        salinity = round(float(salinity), 3)
    
    convertedSalinityData.append(salinity)
    usedTemperature.append(condTempData[i-1])
    usedConductivity.append(condData[i-1])

# Salinity dataframe to remove null values
salinityDF = pd.DataFrame({'Date': salDateTrue, 'Salinity Value': convertedSalinityData, 'Temperature (C)': usedTemperature, 'Conductivity': usedConductivity})

# Removes all rows with null salinity
salinityDFSorted = salinityDF.loc[salinityDF['Salinity Value'] != ""]


def grapher(salDate, salValue, tempValue, condValue, name):
    sx = salDate
    sy = salValue
    ty = tempValue
    cy = condValue

    # Salinity plot
    fig, ax1 = plt.subplots()
    p1 = ax1.plot(sx, sy, color = 'b', linestyle = 'solid', label = 'Salinity (ppt)')

    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "Salinity" label for easy viewing
    ax1.set_ylabel("Salinity (ppt)")
    ax1.set_xlabel("Dates (MM-DD)")
    ax1.yaxis.label.set_color(p1[0].get_color())
    
   
    # Temperature plot
    ax2 = ax1.twinx()
    p2 = ax2.plot(sx, ty, color = 'r', linestyle = 'solid', label = "Temperature (C)")
    ax2.set_ylabel("Temperature (C)")
    ax2.spines["right"].set_position(("outward", 60))
    ax2.yaxis.label.set_color(p2[0].get_color())
    

    # Conductivity plot
    ax3 = ax1.twinx()
    p3 = ax3.plot(sx, cy, color = 'g', linestyle = 'solid', label = "Conductivity")
    ax3.set_ylabel("Conductivity")
    ax3.spines["right"].set_position(("outward", 120))
    ax3.yaxis.label.set_color(p3[0].get_color())
    
    # Sets title, adds a grid, and shows legend
    plt.title(name, fontsize = 20)
    plt.grid(True)
    plt.legend(handles=p1+p2+p3)

    return


# Plots graph without outliers
grapher(salinityDFSorted.get("Date"), salinityDFSorted.get("Salinity Value"), salinityDFSorted.get("Temperature (C)"), 
        salinityDFSorted.get("Conductivity"), "June 2021 (1) Conductivity Data (With Outliers)")

# Saves without outliers graph to specified name in pCO2_data folder
plt.savefig('Conductivity_June_2021_1_Graph_With_Outliers.png')

# Displays figures
plt.show()
