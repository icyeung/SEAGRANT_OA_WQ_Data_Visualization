import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime as dt

def ph_ta_grapher(arag_file_loc, graph_title, graph_save_name):
    my_path = os.path.abspath(os.getcwd())

    data = pd.read_csv(my_path + arag_file_loc)

    # Converts all time strings to datetime objects
    date_dt_list = []
    for date in data["Date (UTC)"]:
        date_dt_obj = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_dt_list.append(date_dt_obj)
    
    # Graphing
    fig, ax1 = plt.subplots(figsize=(28,14))

    # pH Plot
    p1 = ax1.plot(date_dt_list, data["pHConstSal"], marker = '*', color = "blue", label = 'pH')
    
    # Sets axis labels
    ax1.set_ylabel("pH")
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

    plt.savefig(my_path + '\\Comparisons_Different_Parameters\\pH_TA_Grapher\\pH_TA_Graphs\\' + graph_save_name)

    plt.show()

# 2019 Dennis (pH)
ph_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2019_After_pyco2sys.csv",
                   "2019 Dennis pH vs TA",
                   "2019_Dennis_pH_TA.png")

# 2020 Harwich (pH)
ph_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2020_After_pyco2sys.csv",
                   "2020 Harwich pH vs TA",
                   "2020_Harwich_pH_TA.png")

# 2021 Harwich (pH)
ph_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2021_After_pyco2sys.csv",
                   "2021 Harwich pH vs TA",
                   "2021_Harwich_pH_TA.png")

# 2022 Harwich (pH)
ph_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2022_After_pyco2sys.csv",
                   "2022 Harwich pH vs TA",
                   "2022_Harwich_pH_TA.png")

# 2023 Harwich (pH)
ph_ta_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2023_After_pyco2sys.csv",
                   "2023 Harwich pH vs TA",
                   "2023_Harwich_pH_TA.png")