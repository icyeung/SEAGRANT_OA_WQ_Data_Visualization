# Data is in UTC/GMT time zone

import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt


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

def battery_grapher (battery_file, graph_name, save_name):
    # Used to find location of specified file within Python code folder
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # Holds data
    dateList = []
    co2List = []
    batteryList = []
    cvList = []

    # Saves csv as tuple for every row
    with open(os.path.join(__location__, battery_file), 'r') as csvfile:
        data=[tuple(line) for line in csv.reader(csvfile)]
        
    # For every row in tuple, coefficient of variation is calculated and appended to holder list 
    # as each co2 measurement is extracted from tuple
    for row in data[1:]:
        dateList.append(row[0])
        co2List.append(float(row[1]))
        batteryList.append(float(row[2]))
        
        # Skips first co2 value as DoF would be < 1
        # Substitutes first coefficient of variation value calculation with 0
        if len(co2List) > 1:
            co2CV = np.std(co2List,ddof=1) / np.mean(co2List)
            cvList.append(co2CV)
        else:
            cvList.append(float(0))
        
    # Creates dataframe of data used for calculation & graph
    pco2_Battery_DF = pd.DataFrame({"Date": dateList, "CO2": co2List, "Battery": batteryList, 
                                    "Coefficient of Variation": cvList})


    print(pco2_Battery_DF)

    # Creates graph
    plt.figure(figsize=(14,7)) 
    plt.plot(batteryList, cvList)
    plt.axis([max(batteryList), min(batteryList), min(cvList), max(cvList)])
    plt.xlabel('Battery Level')
    plt.ylabel('Coefficient of Variation')
    plt.title(graph_name, fontsize = 15)
    plt.grid(True)

    # Finds location of .py program
    my_path = os.path.dirname(os.path.abspath(__file__))

    # Saves figure as png under desired save name in same folder as .py program
    plt.savefig(my_path + save_name)

    plt.show()

battery_grapher("pco2_Battery_Data.csv", "Coefficient of Variation vs Battery (2021 pCO2)", "\\2021_pco2CV_vs_Battery.png")