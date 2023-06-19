import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

plt.style.use('_mpl-gallery')
  
x = []
ty = []
cy = []
by = []

numofLines = 0
 
with open('C:\\Users\\isabe\\Source\\Repos\\icyeung\\pCO2-DataTrue\\pCO2_data\\completeData.csv','r') as csvfile:
    lines = csv.reader(csvfile, delimiter='\t')
    for row in lines:
        if not row[1] == "" and not row[2] == "" and not row[3] == "" and numofLines > 0:
            x.append(float(row[0]))
            ty.append(float(row[1]))
            cy.append(float(row[2]))
            by.append(float(row[3]))
            numofLines += 1
        elif numofLines == 0:
            numofLines += 1
#plt.figure().set_figheight(15) 
plt.figure().set_figwidth(60)

fig, ax1 = plt.subplots()
p1 = ax1.plot(x, ty, color = 'b', linestyle = 'solid', label = "Temperature (C)")
ax1.set_ylabel("Temperature (C)")
ax2 = ax1.twinx()
p2 = ax2.plot(x, cy, color = 'r', linestyle = 'solid', label = "CO2")
ax2.set_ylabel("CO2")
ax3 = ax1.twinx()
p3 = ax3.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
ax3.set_ylabel("Battery Voltage")

ax3.spines["right"].set_position(("outward", 60))


#plt.plot(x, ty, color = 'b', linestyle = 'solid', label = "Temperature (C)")
#plt.plot(x, cy, color = 'r', linestyle = 'solid', label = "CO2")
#plt.plot(x, by, color = 'g', linestyle = 'solid', label = "Battery Voltage")
  
plt.xticks(np.arange(math.trunc(x[0]), math.trunc(x[-1]), 1), rotation = 90)
plt.xlabel('Dates')
plt.title('pCO2 Data', fontsize = 20)
plt.grid(True)
plt.legend(handles=p1+p2+p3)

plt.show()