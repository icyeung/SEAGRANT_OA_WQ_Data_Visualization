import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime as dt

def pco2_ta_grapher(arag_file_loc, graph_title, graph_save_name):
    my_path = os.path.abspath(os.getcwd())

    data = pd.read_csv(my_path + arag_file_loc)

    # Converts all time strings to datetime objects
    date_dt_list = []
    for date in data["Date (UTC)"]:
        date_dt_obj = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_dt_list.append(date_dt_obj)
    
    # Graphing
    fig, ax1 = plt.subplots(figsize=(28,14))

    # pCO2 Plot
    p1 = ax1.plot(date_dt_list, data["CO2"], marker = '*', color = "blue", label = 'pCO2')
    
    # Sets axis labels
    ax1.set_ylabel("pCO2")
    ax1.set_xlabel("Dates (MM-DD) UTC")
    ax1.yaxis.label.set_color(p1[0].get_color())
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 14))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=45)
    
    # TA Plot
    ax2 = ax1.twinx()
    p2 = ax2.plot(date_dt_list, data["TA (Approximated)"], color = 'red', marker = "^", label = "TA")
    ax2.set_ylabel("TA")
    ax2.yaxis.label.set_color(p2[0].get_color())

    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(graph_title, loc='center')
    fig.legend(loc = 'upper right')

    plt.savefig(my_path + '\\Comparisons_Different_Parameters\\pCO2_TA_Grapher\\pCO2_TA_Graphs\\' + graph_save_name)

    plt.show()

# 2018 Deer Island (pCO2)
pco2_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2018_After_pyco2sys.csv",
                   "2018 Deer Island pCO2 vs TA",
                   "2018_DeerIsland_pCO2_TA.png")

# 2019 Deer Island (pCO2)
pco2_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2019_After_pyco2sys.csv",
                   "2019 Deer Island pCO2 vs TA",
                   "2019_DeerIsland_pCO2_TA.png")

# 2021 North Falmouth (pCO2)
pco2_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2021_After_pyco2sys.csv",
                   "2021 North Falmouth pCO2 vs TA",
                   "2021_NorthFalmouth_pCO2_TA.png")

# 2022 Pocasset (pCO2)
pco2_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2022_After_pyco2sys.csv",
                   "2022 Pocasset pCO2 vs TA",
                   "2022_Pocasset_pCO2_TA.png")

# 2023 Pocasset (pCO2)
pco2_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2023_After_pyco2sys.csv",
                   "2023 Pocasset pCO2 vs TA",
                   "2023_Pocasset_pCO2_TA.png")