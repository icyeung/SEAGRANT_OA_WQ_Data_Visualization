import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# PCO2
# get one file of pco2 processed data for each year
# input each year as a series
# plot temperature and co2
# potential issues: need to figure out how to make the x axis equal, graph on same y axis scale



__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

pco2_2021_data = pd.read_csv(os.path.join(__location__, "pco2_2021_Total_Data_Compiled_Monthly.csv"))

pco2_2022_data = pd.read_csv(os.path.join(__location__, "pco2_2022_Total_Data_Compiled_Monthly.csv"))

pco2_2023_data = pd.read_csv(os.path.join(__location__, "pco2_2023_Total_Data_Compiled_Monthly.csv"))




data_2021 = pco2_2021_data["CO2"]
temp_2021 = pco2_2021_data["Temperature (C)"]
date_2021 = pco2_2021_data["Date"]
date_2021_revised = []
for date in date_2021:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2021_revised.append(dt_date_no_year)



data_2022 = pco2_2022_data["CO2"]
temp_2022 = pco2_2022_data["Temperature (C)"]
date_2022 = pco2_2022_data["Date"]
date_2022_revised = []
for date in date_2022:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2022_revised.append(dt_date_no_year)



data_2023 = pco2_2023_data["CO2"]
temp_2023 = pco2_2023_data["Temperature (C)"]
date_2023 = pco2_2023_data["Date"]
date_2023_revised = []
for date in date_2023:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2023_revised.append(dt_date_no_year)


    # Salinity plot
fig, ax1 = plt.subplots(figsize=(14,7))
p1a = ax1.plot(date_2021_revised, data_2021, color = 'b', linestyle = 'solid', label = '2021', linewidth=0.35)
p1b = ax1.plot(date_2022_revised, data_2022, color = "g", linestyle = 'solid', label = '2022', linewidth=0.35)
p1c = ax1.plot(date_2023_revised, data_2023, color = "r", linestyle = 'solid', label = '2023', linewidth=0.35)

    # Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "Salinity" label for easy viewing
ax1.set_ylabel("pCO2")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")
    
'''   
    # Temperature plot
ax2 = ax1.twinx()
p2 = ax2.plot(sx, ty, color = 'r', linestyle = 'solid', label = "Temperature (F)")
p2a = ax2.plot(date_2021_revised, temp_2021, color = 'b', linestyle = 'dashed', label = '2021')
p2b = ax2.plot(date_2022_revised, temp_2022, color = "g", linestyle = 'dashed', label = '2022')
p2c = ax2.plot(date_2023_revised, temp_2023, color = "r", linestyle = 'dashed', label = '2023')
ax2.set_ylabel("Temperature (C)")
'''    
    
    # Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("pCO2 (2021-2023)", loc='center')
plt.grid(True)
plt.legend(handles=p1a+p1b+p1c)

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\pco2_2021_2023_Graph_No_Outliers.png')

plt.show()

# Current issue: plot is accumulating the series on the x axis, instead of separating them
# Possible fix: strip year from each date and then graph using current method?