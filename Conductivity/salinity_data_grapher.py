import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import math
import datetime
import pytz
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression



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
with open(os.path.join(__location__, 'Salinity_Carolina_FiddlersCove_12-10-21_1.csv'),'r') as csvfile:
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
    timeObj = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S')
    eastern = pytz.timezone('US/Eastern')
    realTimeObj = timeObj.astimezone(eastern)       # Converts time from GMT to EST
    salDateTrue.append(realTimeObj)


unrefinedCondData = pd.DataFrame({'Date': salDateTrue, 'Conductivity': condData, 'Temperature (F)': condTempData})

condTempDataC = []

for temp in unrefinedCondData["Temperature (F)"]:
    tempC = (temp-32)/1.8
    condTempDataC.append(tempC)
unrefinedCondData["Temperature (C)"] = condTempDataC


# Verified Measurement also has to be between 5000, 55000
# If not, does not include data point in graph
for index in range(0, len(salDateTrue)):
    if (condData[index] <= 5000) or (condData[index] >= 55000):
        unrefinedCondData = unrefinedCondData.drop(index)
unrefinedCondData = unrefinedCondData.reset_index(drop=True)




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
for i in range(len(unrefinedCondData)):
    salinity = condSalConv(unrefinedCondData.loc[i, "Conductivity"], unrefinedCondData.loc[i, "Temperature (C)"])
    #print(salinity)
    
    if salinity != "":
        salinity = round(float(salinity), 3)
    
        convertedSalinityData.append(salinity)
        usedTime.append(unrefinedCondData.loc[i, "Date"])
        usedTemperature.append(unrefinedCondData.loc[i, "Temperature (C)"])
        usedConductivity.append(unrefinedCondData.loc[i, "Conductivity"])


# Remove outliers by taking 10% of the regression line
# Use Julian Days for the time    
#print('salDate length', len(salDate))
#print("salDateTrue length", len(salDateTrue))

salDateTrueJulian = usedTime.copy()

# Converts dates to ints
# Not used as there are jumps due to the date format not being continuous as an int
'''
salDateInt = []
#salDateIntHolder = []
for date in salDateTrueOrdinal:
    print(date)
    date = date.replace(" ", "")
    date = date.replace("/", "")
    date = date.replace(":", "")
    #date = [date[0]+date[1]]
    #print("Int Conversion Date (currently string)", date, type(date))
    date = int(date)
    #print("Int Conversion Date (currently int)", date, type(date))
    salDateInt.append(date)

'''


salDateJulianOR = []
#salDateJulianHolder = []
for date in usedTime:
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second
    ts = pd.Timestamp(year, month, day, hour, second)
    jd = ts.to_julian_date()
    salDateJulianOR.append(jd)
print(salDateJulianOR)

#print("length of salDateInt", len(salDateInt))
#print("length of salDateTrueOrdinal", len(salDateTrueOrdinal))

salDateTrueOrdinalAry = np.array(salDateJulianOR)
#salDateTrueOrdinal.toArray(salDateTrueOrdinalAry)

condDataOR = usedConductivity.copy()
condDataAry = np.array(condDataOR)
#condData.toArray(condDataAry)

#dateStringUnrefinedCondData = pd.DataFrame({'Date': salDateTrueJulian, 'Conductiviy': condData, 'Temperature (C)': condTempDataC})   
model = LinearRegression().fit(salDateTrueOrdinalAry.reshape(-1,1), condDataAry)
r_sq = model.score(salDateTrueOrdinalAry.reshape(-1,1), condDataAry)
print("intercept", model.intercept_)
print("slope", model.coef_)
#print('coefficient of determination:', r_sq)
condDataFitPredList=[]
for date in salDateJulianOR:
    condDataFitPredList.append((model.coef_*date)+model.intercept_)
#condDataFitPredAry = model.predict(salDateTrueOrdinalAry.reshape(-1,1))
#print("fit tester", condDataFitPredAry)

#condDataFitPredList = condDataFitPredAry.tolist()
print(len(salDateTrueJulian))
print('before cutting', len(condDataFitPredList))

#print("list", condDataFitPredList)

# Salinity dataframe to remove null values
salinityDF = pd.DataFrame({'Date': salDateTrueJulian, 'Salinity Value': convertedSalinityData, 'Temperature (C)': usedTemperature, 'Conductivity': usedConductivity,
                          'Fit': condDataFitPredList})
print(len(salDateTrue))
#print(salinityDF)


# Removes all rows with null salinity

# print(salinityDFSorted)

salinityDF_copy = pd.DataFrame({'Date': salDateTrueJulian, 'Salinity Value': convertedSalinityData, 'Temperature (C)': usedTemperature, 'Conductivity': usedConductivity,
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

#print(salinityDFSortedNOreset.get("Fit"))

salinityDFSorted.to_csv(os.path.dirname(os.path.abspath(__file__)) + 'Testing_before.csv')
salinityDFSortedNOreset.to_csv(os.path.dirname(os.path.abspath(__file__)) + 'Testing_after.csv')

def grapher(salDate, salValue, tempValue, condValue, fitValue, name):
    sx = salDate
    sy = salValue
    ty = tempValue
    cy = condValue
    fy = fitValue

    # Salinity plot
    fig, ax1 = plt.subplots(figsize=(14,7))
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
    p2 = ax2.plot(sx, ty, color = 'r', linestyle = 'solid', label = "Temperature (F)")
    ax2.set_ylabel("Temperature (C)")
    ax2.spines["right"].set_position(("outward", 60))
    ax2.yaxis.label.set_color(p2[0].get_color())


    # Conductivity plot
    ax3 = ax1.twinx()
    p3 = ax3.plot(sx, cy, color = 'c', linestyle = 'solid', label = "Conductivity")
    ax3.set_ylabel("Conductivity")
    ax3.spines["right"].set_position(("outward", 120))
    ax3.yaxis.label.set_color(p3[0].get_color())

    # Linear Regression of COnductivity Plot
    ax4 = ax1.twinx()
    p4 = ax4.plot(sx, fy, color = "g", linestyle = 'solid', label = "Fit Line")
    ax4.set_ylabel("Fit")
    ax4.spines["right"].set_position(("outward", 180))
    ax4.yaxis.label.set_color(p4[0].get_color())
    
    # Sets title, adds a grid, and shows legend
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(name, loc='center')
    plt.grid(True)
    plt.legend(handles=p1+p2+p3+p4)

    return


# Plots graph with outliers
grapher(salinityDFSorted.get("Date"), salinityDFSorted.get("Salinity Value"), salinityDFSorted.get("Temperature (C)"),
        salinityDFSorted.get("Conductivity"), salinityDFSorted.get("Fit"), "12-10-21 (1) Conductivity Data (With Outliers)")

# Finds location of .py program
my_path = os.path.dirname(os.path.abspath(__file__))

# Saves with outliers graph to specified name in folder
plt.savefig(my_path + '\\Conductivity_Graphs\\Conductivity_12-10-21_1_Graph_With_Outliers.png', dpi=2000)

print("no fit lenth", len(salinityDFSorted.get("Fit")))


# Plots graph without outliers
grapher(salinityDFSortedNOreset.get("Date"), salinityDFSortedNOreset.get("Salinity Value"), salinityDFSortedNOreset.get("Temperature (C)"),
        salinityDFSortedNOreset.get("Conductivity"), salinityDFSortedNOreset.get("Fit"), "12-10-21 (1) Conductivity Data (Without Outliers)")

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\Conductivity_Graphs\\Conductivity_12-10-21_1_Graph_Without_Outliers.png', dpi=2000)

salinityDFSortedNOreset.to_csv(my_path + '\\Conductivity_Data_NO\\Salinity_Carolina_FiddlersCove_12-10-21_1_NO.csv')

print("fitted length", len(salinityDFSortedNOreset.get("Fit")))

# Displays figures
plt.show()
