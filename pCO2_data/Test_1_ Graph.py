import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import csv
import math


# Sets the graph layout colors and style
plt.style.use('default')

# Used to hold data from csv file  
x = []      # Dates
ty = []     # Temperature
cy = []     # CO2
by = []     # Battery Voltage

numofLines = 0
 
with open('C:\\Users\\isabe\\Source\\Repos\\icyeung\\pCO2-DataTrue\\pCO2_data\\completeData.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter='\t')
    for row in lines:
        
        # Checks if time entry has corresponding Temperature, CO2, and Battery Voltage
        # If not, does not include data point in graph
        if not row[1] == "" and not row[2] == "" and not row[3] == "" and numofLines > 0:
            x.append(float(row[0]))
            ty.append(float(row[1]))
            cy.append(float(row[2]))
            by.append(float(row[3]))
            numofLines += 1
        elif numofLines == 0:
            numofLines += 1

# Makes graph wider so Dates can be viewed properly
plt.figure().set_figwidth(60)

# Allows for more than one set of data to be plotted

# Temperature plot
fig, ax1 = plt.subplots()
p1 = ax1.plot(x, ty, color = 'b', linestyle = 'solid', label = "Temperature (C)")

# Sets x-axis as Dates
ax1.xaxis.set_ticks(np.arange(math.trunc(x[0]), math.trunc(x[-1]), 1))     # Step size of 1
ax1.set_xticklabels(ax1.get_xticks(), rotation = 90)        # Rotates dates to be perpendiculat to x-axis

# Sets axis labels and changes font color for easy viewing
ax1.set_ylabel("Temperature (C)")
ax1.set_xlabel("Dates")
ax1.yaxis.label.set_color(p1[0].get_color())


# CO2 plot
ax2 = ax1.twinx()
p2 = ax2.plot(x, cy, color = 'r', linestyle = 'solid', label = "CO2")
ax2.set_ylabel("CO2")
ax2.yaxis.label.set_color(p2[0].get_color())

# Battery Voltage plot
ax3 = ax1.twinx()
p3 = ax3.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
ax3.set_ylabel("Battery Voltage")
ax3.spines["right"].set_position(("outward", 60))
ax3.yaxis.label.set_color(p3[0].get_color())

  
# Sets title, adds a grid, and shows legend
plt.title('pCO2 Data', fontsize = 20)
plt.grid(True)
plt.legend(handles=p1+p2+p3)

plt.show()