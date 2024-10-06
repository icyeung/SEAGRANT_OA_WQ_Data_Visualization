import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime as dt

def arag_state_grapher(arag_file_loc, graph_title, graph_save_name):
    my_path = os.path.abspath(os.getcwd())

    arag_data = pd.read_csv(my_path + arag_file_loc)

    # Converts all time strings to datetime objects
    date_dt_list = []
    for date in arag_data["Date (UTC)"]:
        date_dt_obj = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_dt_list.append(date_dt_obj)
    
    # Graphing
    fig, ax1 = plt.subplots(figsize=(28,14))
    p1 = ax1.plot(date_dt_list, arag_data["Saturation Aragonite Out"], marker = '*', color = "blue", label = 'Aragonite Saturation State')
    
    # Sets axis labels
    ax1.set_ylabel("Aragonite Saturation State")
    ax1.set_xlabel("Dates (MM-DD) UTC")
    #ax1.yaxis.label.set_color(p2[0].get_color())
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval = 14))     # Displays x-axis label every 14 days
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    plt.xticks(rotation=45)
    
    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(graph_title, loc='center')
    fig.legend(loc = 'upper right')

    plt.savefig(my_path + '\\Aragonite_Saturation_State\\Arag_Graphs\\' + graph_save_name)

    plt.show()

# 2018 Deer Island (pCO2)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2018_After_pyco2sys.csv",
                   "2018 Deer Island Aragonite Staturation State",
                   "Arag_2018_DeerIsland_pCO2.png")

# 2019 Deer Island (pCO2)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2019_After_pyco2sys.csv",
                   "2019 Deer Island Aragonite Staturation State",
                   "Arag_2019_DeerIsland_pCO2.png")

# 2021 North Falmouth (pCO2)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2021_After_pyco2sys.csv",
                   "2021 North Falmouth Aragonite Staturation State",
                   "Arag_2021_NorthFalmouth_pCO2.png")

# 2022 Pocasset (pCO2)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2022_After_pyco2sys.csv",
                   "2022 Pocasset Aragonite Staturation State",
                   "Arag_2022_Pocasset_pCO2.png")

# 2023 Pocasset (pCO2)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2023_After_pyco2sys.csv",
                   "2023 Pocasset Aragonite Staturation State",
                   "Arag_2023_Pocasset_pCO2.png")

# 2019 Dennis (pH)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2019_After_pyco2sys.csv",
                   "2019 Dennis Aragonite Staturation State",
                   "Arag_2019_Dennis_pH.png")

# 2020 Harwich (pH)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2020_After_pyco2sys.csv",
                   "2020 Harwich Aragonite Staturation State",
                   "Arag_2020_Harwich_pH.png")

# 2021 Harwich (pH)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2021_After_pyco2sys.csv",
                   "2021 Harwich Aragonite Staturation State",
                   "Arag_2021_Harwich_pH.png")

# 2022 Harwich (pH)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2022_After_pyco2sys.csv",
                   "2022 Harwich Aragonite Staturation State",
                   "Arag_2022_Harwich_pH.png")

# 2023 Harwich (pH)
arag_state_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2023_After_pyco2sys.csv",
                   "2023 Harwich Aragonite Staturation State",
                   "Arag_2023_Harwich_pH.png")