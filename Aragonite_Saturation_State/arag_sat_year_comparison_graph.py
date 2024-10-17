import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime as dt
import datetime

def arag_state_year_grapher(arag_file1_loc, arag_file1_year, arag_file2_loc, arag_file2_year, arag_file3_loc, arag_file3_year, arag_file4_loc, arag_file4_year, file_number, graph_title, graph_save_name):
    my_path = os.path.abspath(os.getcwd())
    
    if arag_file1_loc != "N/A":
        arag_data_1 = pd.read_csv(my_path + arag_file1_loc)

        # Converts all time strings to datetime objects
        date1_dt_list = []
        for date in arag_data_1["Date (UTC)"]:
            date_obj = date.split(" ")[0]
            y1, m1, d1 = [int(date_part) for date_part in date_obj.split("-")]
            date1 = dt(2020, m1, d1)
            converted_time_dt = dt.strptime(date.split(" ")[1], "%H:%M:%S")
            date1_dt_list.append(dt.combine(date1, converted_time_dt.time()))
            
            #date1_dt_obj = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
            # #date1_dt_list.append(date1_dt_obj)

    if arag_file2_loc != "N/A":
        arag_data_2 = pd.read_csv(my_path + arag_file2_loc)

        # Converts all time strings to datetime objects
        date2_dt_list = []
        for date in arag_data_2["Date (UTC)"]:
            date_obj = date.split(" ")[0]
            y2, m2, d2 = [int(date_part) for date_part in date_obj.split("-")]
            date2 = dt(2020, m2, d2)
            converted_time_dt = dt.strptime(date.split(" ")[1], "%H:%M:%S")
            date2_dt_list.append(dt.combine(date2, converted_time_dt.time()))

            #date2_dt_obj = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
            #date2_dt_list.append(date2_dt_obj)

    if arag_file3_loc != "N/A":
        arag_data_3 = pd.read_csv(my_path + arag_file3_loc)

        # Converts all time strings to datetime objects
        date3_dt_list = []
        for date in arag_data_3["Date (UTC)"]:
            date_obj = date.split(" ")[0]
            y3, m3, d3 = [int(date_part) for date_part in date_obj.split("-")]
            date3 = dt(2020, m3, d3)
            converted_time_dt = dt.strptime(date.split(" ")[1], "%H:%M:%S")
            date3_dt_list.append(dt.combine(date3, converted_time_dt.time()))

            #date3_dt_obj = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
            #date3_dt_list.append(date3_dt_obj)

    if arag_file4_loc != "N/A":
        arag_data_4 = pd.read_csv(my_path + arag_file4_loc)

        # Converts all time strings to datetime objects
        date4_dt_list = []
        for date in arag_data_4["Date (UTC)"]:
            date_obj = date.split(" ")[0]
            y4, m4, d4 = [int(date_part) for date_part in date_obj.split("-")]
            date4 = dt(2020, m4, d4)
            converted_time_dt = dt.strptime(date.split(" ")[1], "%H:%M:%S")
            date4_dt_list.append(dt.combine(date4, converted_time_dt.time()))

            #date4_dt_obj = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
            #date4_dt_list.append(date4_dt_obj)

    
    # Graphing
    fig, ax1 = plt.subplots(file_number, sharex=True, sharey=True, figsize=(28,14), constrained_layout = True)

    if arag_file1_loc != "N/A":
        p1 = ax1[0].plot(date1_dt_list, arag_data_1["Saturation Aragonite Out"], marker = '*', color = "blue", label = arag_file1_year)
        ax1[0].grid()
        ax1[0].tick_params("y", labelsize = 19)

    if arag_file2_loc != "N/A":
        p2 = ax1[1].plot(date2_dt_list, arag_data_2["Saturation Aragonite Out"], marker = '*', color = "green", label = arag_file2_year)
        ax1[1].grid()
        ax1[1].tick_params("y", labelsize = 19)

    if arag_file3_loc != "N/A":
        p3 = ax1[2].plot(date3_dt_list, arag_data_3["Saturation Aragonite Out"], marker = '*', color = "red", label = arag_file3_year)
        ax1[2].grid()
        ax1[2].tick_params("y", labelsize = 19)

    if arag_file4_loc != "N/A":
        p4 = ax1[3].plot(date4_dt_list, arag_data_4["Saturation Aragonite Out"], marker = '*', color = "purple", label = arag_file4_year)
        ax1[3].grid()
        ax1[3].tick_params("y", labelsize = 19)
    
    # Sets axis labels
    fig.supylabel("Aragonite Saturation State", fontsize = 22, fontweight = "bold")
    fig.supxlabel("Dates (MM-DD) UTC", fontsize = 22, fontweight = "bold")
    #ax1.yaxis.label.set_color(p2[0].get_color())
    
    
    # Sets x-axis as Dates
    date_form = DateFormatter("%m-%d")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 7))     # Displays x-axis label every 14 days
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval = 1))       # Indicates each day (without label) on x-axis
    plt.gca().set_xbound(datetime.date(2020,4,30), datetime.date(2020,12,18))
    plt.xticks(rotation=45, fontsize = 19)
    

    #plt.xlim(datetime.date(2020,1,1), datetime.date(2020,12,31))
    plt.ylim(0,5)
    
    
    
    
    #plt.gca().grid(True)
    #plt.tight_layout()
    #plt.tight_layout(pad=2, w_pad=0.5, h_pad=1.0)
    #plt.subplots_adjust(top=0.01)
    #plt.title(graph_title)

    fig.suptitle(graph_title, fontsize = 26, fontweight = "bold")
    fig.legend(loc = 'center right', fontsize = 19)

    plt.savefig(my_path + '\\Aragonite_Saturation_State\\Arag_Graphs\\' + graph_save_name)
    
    plt.show()

# 2018-2019 Deer Island (pCO2)
arag_state_year_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2018_After_pyco2sys.csv",
                        "2018",
                        "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2019_After_pyco2sys.csv",
                        "2019",
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A",
                        2,
                        "2018-2019 Deer Island Aragonite Staturation State",
                        "Arag_2018-2019_DeerIsland_pCO2.png")

# 2022-2023 Pocasset (pCO2)
arag_state_year_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2022_After_pyco2sys.csv",
                        "2022",
                        "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2023_After_pyco2sys.csv",
                        "2023",
                        "N/A",
                        "N/A",
                        "N/A",
                        "N/A",
                        2,
                        "2022-2023 Pocasset Aragonite Staturation State",
                        "Arag_2022-2023_Pocasset_pCO2.png")

# 2020-2023 Harwich (pH)
arag_state_year_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2020_After_pyco2sys.csv",
                        "2020",
                        "\\pyco2sys\\pyco2sys_Output_Files\\pH_2021_After_pyco2sys.csv",
                        "2021",
                        "\\pyco2sys\\pyco2sys_Output_Files\\pH_2022_After_pyco2sys.csv",
                        "2022",
                        "\\pyco2sys\\pyco2sys_Output_Files\\pH_2023_After_pyco2sys.csv",
                        "2023",
                        4,
                        "2020-2023 Harwich Aragonite Staturation State",
                        "Arag_2020-2023_Harwich_pH.png")
