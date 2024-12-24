import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# pH
# get one file of pH processed data for each year
# input each year as a series
# plot temperature and pH
# potential issues: need to figure out how to make the x axis equal, graoh on same y axis scale



__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

pH_2019_data = pd.read_csv(os.path.join(__location__, "pH_Data_2019_Compiled_Monthly.csv"))

pH_2020_data = pd.read_csv(os.path.join(__location__, "pH_Data_2020_Compiled_Monthly.csv"))

pH_2021_data = pd.read_csv(os.path.join(__location__, "pH_Data_2021_Compiled_Monthly.csv"))

pH_2022_data = pd.read_csv(os.path.join(__location__, "pH_Data_2022_Compiled_Monthly.csv"))

pH_2023_data = pd.read_csv(os.path.join(__location__, "pH_Data_2023_Compiled_Monthly.csv"))


data_2019 = pH_2019_data["pH"]
temp_2019 = pH_2019_data["Temperature (C)"]
date_2019 = pH_2019_data["Date"]
date_2019_revised = []
for date in date_2019:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2019_revised.append(dt_date_no_year)


data_2020 = pH_2020_data["pH"]
temp_2020 = pH_2020_data["Temperature (C)"]
date_2020 = pH_2020_data["Date"]
date_2020_revised = []
for date in date_2020:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2020_revised.append(dt_date_no_year)


data_2021 = pH_2021_data["pH"]
temp_2021 = pH_2021_data["Temperature (C)"]
date_2021 = pH_2021_data["Date"]
date_2021_revised = []
for date in date_2021:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2021_revised.append(dt_date_no_year)


data_2022 = pH_2022_data["pH"]
temp_2022 = pH_2022_data["Temperature (C)"]
date_2022 = pH_2022_data["Date"]
date_2022_revised = []
for date in date_2022:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2022_revised.append(dt_date_no_year)


data_2023 = pH_2023_data["pH"]
temp_2023 = pH_2023_data["Temperature (C)"]
date_2023 = pH_2023_data["Date"]
date_2023_revised = []
for date in date_2023:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    date_2023_revised.append(dt_date_no_year)


    # Salinity plot
fig, ax1 = plt.subplots(figsize=(14,7))
p1a = ax1.plot(date_2019_revised, data_2019, color = 'r', linestyle = 'solid', label = '2019', linewidth=0.85)
#p1b = ax1.plot(date_2020_revised, data_2020, color = 'g', linestyle = 'solid', label = '2020', linewidth=0.85)
#p1c = ax1.plot(date_2021_revised, data_2021, color = 'b', linestyle = 'solid', label = '2021', linewidth=0.85)
#p1d = ax1.plot(date_2022_revised, data_2022, color = "m", linestyle = 'solid', label = '2022', linewidth=0.85)
#p1e = ax1.plot(date_2023_revised, data_2023, color = "c", linestyle = 'solid', label = '2023', linewidth=0.85)

    # Sets x-axis as Dates
date_form = DateFormatter("%m-%d")
ax1.xaxis.set_major_formatter(date_form)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    
    # Sets axis labels and changes font color of "Salinity" label for easy viewing
ax1.set_ylabel("pH")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")
 
    
    # Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("pH-SAMI Dennis (2019)", loc='center')
plt.grid(True)
plt.legend(handles=p1a)


my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\pH_2019_Graph_No_Outliers.png')

plt.show()
