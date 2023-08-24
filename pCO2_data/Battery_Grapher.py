import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import math

# Used to find location of specified file within Python code folder
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

dateList = []
co2List = []
batteryList = []
cvList = []

with open(os.path.join(__location__,'pco2_Battery_Data.csv'), 'r') as csvfile:
    data=[tuple(line) for line in csv.reader(csvfile)]
    
print(data)

for row in data[1:]:
    dateList.append(row[0])
    co2List.append(float(row[1]))
    batteryList.append(float(row[2]))
    
    if len(co2List) > 1:
        co2CV = np.std(co2List,ddof=1) / np.mean(co2List) * 100
        cvList.append(co2CV)
    else:
        cvList.append(float(0))
    

pco2_Battery_DF = pd.DataFrame({"Date": dateList, "CO2": co2List, "Battery": batteryList, 
                                "Coefficient of Variation": cvList})


print(pco2_Battery_DF)

plt.plot(batteryList, cvList)
plt.axis([max(batteryList), min(batteryList), min(cvList), max(cvList)])
# new_list = range(math.floor(min(batteryList)), math.floor(math.ceil(max(batteryList))+1))
# plt.xticks(new_list)
# plt.xticks(rotation ='vertical')
plt.xlabel('Battery Level')
plt.ylabel('Coefficient of Variation')
plt.title('Coefficient of Variation vs Battery', fontsize = 15)
plt.grid(True)
plt.show()


plt.savefig('2021_pco2CV_vs_Battery.png')

'''

for every instance a pco2 sample is added to the data set
the cov is recalculated and graphed against the battery

time stamps must be kept
add the cv as a separate column 

loop that adds the data row to the data frame
in same loop, pulls out the co2 column and calculates the cv
stores cv entry in cv column

repeats until the no more rows to add
- all entries in row are null

what if data row is stored in a tuple

'''