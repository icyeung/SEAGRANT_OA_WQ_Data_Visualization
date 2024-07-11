import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import pytz

# Create graph overlay of water sampling date and pco2 or ph
# y-axis would be total alkalinity/DIC and calculated pco2/ph 
# maybe use 2020 as an example (not 2022 as it has the errors)
# will have to use 2021 as there is no water sample data for HAR besides 2021 


# use data from 2017-2022 mwra
# tco2=dic
# ta
# out vlues are calculated
#Stat_ID = HAR

# Separate DIC, TA, and calculated pH values by location of water sample
# Different colors for same symbol?
# red for top
# green for bottom

# Have small arrow denoting incoming or outgoing tide
# Pointing up for incoming
# Pointing down for outgoing


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

MWRA_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv")

MWRA_trunc_2020_df = pd.DataFrame()
MWRA_trunc_2020_df = pd.DataFrame(data=MWRA_trunc_2020_df, columns=MWRA_data.columns)

MWRA_trunc_2021_df = pd.DataFrame()
MWRA_trunc_2021_df = pd.DataFrame(data=MWRA_trunc_2021_df, columns=MWRA_data.columns)

MWRA_trunc_2022_df = pd.DataFrame()
MWRA_trunc_2022_df = pd.DataFrame(data=MWRA_trunc_2022_df, columns=MWRA_data.columns)

MWRA_trunc_2023_df = pd.DataFrame()
MWRA_trunc_2023_df = pd.DataFrame(data=MWRA_trunc_2023_df, columns=MWRA_data.columns)


def get_year(entry):
    date = entry.split(" ")[0]
    year = date.split("/")[2]
    return year

# Obtains desired data for location
for index in range(0, len(MWRA_data)):
#print("A:", indexA)
    if ((MWRA_data.loc[index, "STAT_ID"])) == "POC" and (get_year(MWRA_data.loc[index, "PROF_DATE_TIME_LOCAL"]) == "2020") :
        print("yay the date works")
        new_row = MWRA_data.loc[index].copy()
        MWRA_trunc_2020_df.loc[index] = new_row
        print("yay")


# Obtains desired data for location
for index in range(0, len(MWRA_data)):
#print("A:", indexA)
    if ((MWRA_data.loc[index, "STAT_ID"])) == "POC" and (get_year(MWRA_data.loc[index, "PROF_DATE_TIME_LOCAL"]) == "2021") :
        print("yay the date works")
        new_row = MWRA_data.loc[index].copy()
        MWRA_trunc_2021_df.loc[index] = new_row
        print("yay")


# Obtains desired data for location
for index in range(0, len(MWRA_data)):
#print("A:", indexA)
    if ((MWRA_data.loc[index, "STAT_ID"])) == "POC" and (get_year(MWRA_data.loc[index, "PROF_DATE_TIME_LOCAL"]) == "2022") :
        print("yay the date works")
        new_row = MWRA_data.loc[index].copy()
        MWRA_trunc_2022_df.loc[index] = new_row
        print("yay")

MWRA_trunc_2022_df.to_csv("sal_ta_poc_2022.csv")

# pH 2021 data section is good
# converts pH date to mm/dd format by dropping year
sal_2020_data = MWRA_trunc_2020_df["SAL (PSU)"]
ta_2020_data = MWRA_trunc_2020_df["TA in (mmol/kgSW)"]

sal_2021_data = MWRA_trunc_2021_df["SAL (PSU)"]
ta_2021_data = MWRA_trunc_2021_df["TA in (mmol/kgSW)"]

sal_2022_data = MWRA_trunc_2022_df["SAL (PSU)"]
ta_2022_data = MWRA_trunc_2022_df["TA in (mmol/kgSW)"]
 
if len(sal_2020_data) == len(ta_2020_data):
    
    print("yayyyy, no issues for 2020 yet")
else:
    print("warning, 2020 lengths do not match")

if len(sal_2021_data) == len(ta_2021_data):
    print("yayyyy, no issues for 2021 yet")
else:
    print("warning, 2021 lengths do not match")

if len(sal_2022_data) == len(ta_2022_data):
    print("yayyyy, no issues for 2022 yet")
else:
    print("warning, 2022 lengths do not match")


# Graphing
fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.scatter(sal_2020_data, ta_2020_data, color = "r", marker = "*", label = '2020', linewidth=0.75)
p2 = ax1.scatter(sal_2021_data, ta_2021_data, color = "g", marker = "*", label = '2021', linewidth=0.75)
p3 = ax1.scatter(sal_2022_data, ta_2022_data, color = "b", marker = "*", label = '2022', linewidth=0.75)
#p4 = ax1.scatter(bottom_date_GMT, bottom_cal_pCO2_data, color = 'olivedrab', marker = "D", label = "Calculated pCO2- Bottom Sample", zorder=3)
#p5 = ax1.scatter(top_date_GMT, top_cal_pCO2_data, color = 'greenyellow', marker = "D", label = "Calculated pCO2- Top Sample", zorder=3)
#p12 = ax1.scatter(mid_date_GMT, mid_cal_pCO2_data, color = 'teal', marker = "D", label = "Calculated pCO2- Middle Sample", zorder=3)

# Sets x-axis as Dates
# Displays x-axis label every 14 days
#ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 2))       # Indicates each day (without label) on x-axis
    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("TA (mmol/kgSW)")
ax1.set_xlabel("SAL (PSU)")
ax1.yaxis.label.set_color("k")
#ax1.legend()  


# Sets title, adds a grid, and shows legend
plt.grid(True)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("SAL vs TA: Pocasset (2020-2022)", loc='center')
fig.legend(loc = 'upper center', ncol = 3, borderaxespad=4)


my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
#plt.savefig(my_path + '\\sal_vs_ta_pocasset_2020_2022.png')
plt.show()
