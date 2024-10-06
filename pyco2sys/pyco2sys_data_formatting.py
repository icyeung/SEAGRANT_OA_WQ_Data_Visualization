# Need to create depth column (dbar) for sami
# 1.5m deep -> pressure ~1.15 atm -> 11.65237 dbar
# Match up closest ta/sal for each sami measurement

# ph & pco2 date as y-m-d
# sal data format varies by type

import pandas as pd
import datetime as datetime
from datetime import datetime as dt
import numpy as np
import os

# Converts from H:M:S to time/24    
def time_frac_cal(time):
    time_hour = int(time.split(":")[0])
    time_minute = int(time.split(":")[1])
    time_min_percent = round(time_minute/60, 4)
    time_frac_conv = float(time_hour + time_min_percent)
    return time_frac_conv

# Main program to call for formatting data file for pyco2sys
# Formatted file will be outputted using sami file as base
def file_formatting(sal_ta_file_loc, sami_file_loc, sami_file_name, input_type):
    
    my_path = os.path.abspath(os.getcwd())

    sal_ta_data = pd.read_csv(my_path + sal_ta_file_loc)
    sami_data = pd.read_csv(my_path + sami_file_loc)

    # Adds depth column to sami file
    depth_list = []
    for value in range(0, len(sami_data)):
        depth_list.append(11.65237)

    sami_data["Depth (dbar)"] = depth_list

    # Adds corresponding sal/ta date time column to sami file
    sami_data["Sal/TA Date (UTC)"] = ""

    # Adds corresponding sal column to sami file
    sami_data["Salinity"] = ""

    # Adds corresponding ta column to sami file
    sami_data["TA (Approximated)"] = ""

    if input_type == "2018 pCO2":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "DateTime (UTC)"
        sal_ta_sal_col_name = "Salinity"
        sal_ta_ta_col_name = "TA (Approximated)"

    if input_type == "2019 pCO2":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "Time (UTC)"
        sal_ta_sal_col_name = "Salinity"
        sal_ta_ta_col_name = "TA (Approximated)"

    if input_type == "2019 pH":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "Datetime_UTC"
        sal_ta_sal_col_name = "Salinity"
        sal_ta_ta_col_name = "TA (Approximated)"

    if input_type == "2020 pH" or input_type == "2021 pH" or input_type == "2022 pH" or input_type == "2023 pH":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "Datetime_Adjusted_UTC+1"
        sal_ta_sal_col_name = "Sal"
        sal_ta_ta_col_name = "TA (Approximated)"

    if input_type == "2021 pCO2":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "Date (UTC)"
        sal_ta_sal_col_name = "Salinity Value (Offset +4)"
        sal_ta_ta_col_name = "TA (Approximated)"

    if input_type == "2022 pCO2":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "Date (UTC)"
        sal_ta_sal_col_name = "Salinity Value (Offset +15)"
        sal_ta_ta_col_name = "TA (Approximated)"

    if input_type == "2023 pCO2":
        sami_date_col_name = "Date (UTC)"
        sal_ta_date_col_name = "Date (UTC) Offset -3 Hours"
        sal_ta_sal_col_name = "Salinity Value (Offset +15)"
        sal_ta_ta_col_name = "TA (Approximated)"
    

    # for date in sami, finds the same date in sal/ta file 
    # then calculates the closest time to that time stamp and obtain row #
    # then locates the corresponding sal/ta values from that row
    # saves all to three lists
    # works under the assumption data is chronological
    
    index=0     # Index for looking through sal/ta file
    opt_time_df_index = 0   # Initializes index to hold last used index for sami matching
    opt_sal_ta_time_index_list = []     # Holds all indices used for sami matching
    sami_rows_to_drop = []      # Rows of sami where there is no matching sal/ta; will be dropped
    sami_dates_to_drop = []     # Dates of sami where there is no matching sal/ta; will be dropped

    # Goes through all the sami entires individually
    # For each sami row, 
    for sami_index in range(0, len(sami_data[sami_date_col_name])):
        # Obtains sami date and time
        sami_dt = sami_data.loc[sami_index, sami_date_col_name]
        sami_date = sami_dt.split(" ")[0]
        #print("sami datetime", sami_dt)
        ys, ms, ds = [int(part) for part in sami_date.split("-")]
        # Obtains sami time as time frac
        sami_time_frac = time_frac_cal(sami_dt.split(" ")[1])
        #print("sami time frac", sami_time_frac)

        same_date_time_list = []    # Holds all time entries for same date for sal/ta
        same_date_sal_index_list = []   # Holds all corresponing indices for appropriate time entires
        #print("index before while", index)
        
        index = opt_time_df_index   # Sets the first sal/ta entry to look at each time is the one that was used to pair for the last sami; reduces search redundancy
        while index < len(sal_ta_data):
            sal_ta_dt = sal_ta_data.loc[index, sal_ta_date_col_name]   # Obtains date and time for each sal/ta row
            #print("sal date dt", sal_ta_dt)

            sal_ta_date = sal_ta_dt.split(" ")[0]   # Obtains date only from the date time

            if input_type == "2018 pCO2" or input_type == "2019 pCO2" or input_type == "2020 pH" or input_type == "2021 pH" or input_type == "2022 pH" or input_type == "2023 pH":
                m1, d1, y1 = [int(sal_part) for sal_part in sal_ta_date.split("/")]
            elif input_type == "2019 pH" or input_type == "2021 pCO2" or input_type == "2022 pCO2" or input_type == "2023 pCO2":
                y1, m1, d1 = [int(sal_part) for sal_part in sal_ta_date.split("-")]
            else:
                print("ERROR: input type does not match any")
                break

            # Checks if sal/ta date is same as sami date
            # If yes, adds sal/ta time as time frac to list and saves sal/ta index
            if y1 == ys and m1 == ms and d1 == ds:
                same_date_sal_index_list.append(index)
                same_date_time_list.append(time_frac_cal(sal_ta_dt.split(" ")[1]))
            
            # If date is not the same and other same dates have been found, breaks loop
            #       Reasoning is that data is chronological and all same dates have been found; reduces search redundancy
            if (y1 != ys or m1 != ms or d1 != ds) and (len(same_date_sal_index_list) != 0):
                break
            
            # Continues loop
            index += 1
        
        #print("index after while loop", index)
        
        
        # Once all same dates have been found:
        # If there are same dates, goes through all times from the same day and finds the difference between them and the sami time
        if len(same_date_time_list) != 0:
            difference_list = []
            for time in same_date_time_list:  
                difference = abs(float(sami_time_frac-time))
                #print(difference)         
                difference_list.append(difference)
            #print("list of time diff", difference_list)


            #print("same date index", same_date_sal_index_list)
            #print("same date list of times", same_date_time_list)
            
            
            # Identifies the smallest time difference
            min_time_diff = min(difference_list)
            
            #print("min time diff", min_time_diff)
            
            # Checks to see if smallest time difference is within 1 hour
            # If it is:
            if min_time_diff <= 1:
                # Identifies index in list of differences
                min_time_diff_index = difference_list.index(min_time_diff)
                #print("min time diff index", min_time_diff_index)

                # Uses difference index to find the value in sal/ta same day index list
                opt_time_df_index = same_date_sal_index_list[min_time_diff_index]
                
                # Appends that index to list
                opt_sal_ta_time_index_list.append(opt_time_df_index)

                # Finds corresponding sal/ta datettime, sal, and ta values and copies them to sami file
                sami_data.loc[sami_index, "Sal/TA Date (UTC)"] = sal_ta_data.loc[opt_time_df_index, sal_ta_date_col_name]
                
                sami_data.loc[sami_index, "Salinity"] = sal_ta_data.loc[opt_time_df_index, sal_ta_sal_col_name]
                
                sami_data.loc[sami_index, "TA (Approximated)"] = sal_ta_data.loc[opt_time_df_index, sal_ta_ta_col_name]

            else:
                sami_rows_to_drop.append(sami_index)
                sami_dates_to_drop.append(sami_data.loc[sami_index, sami_date_col_name])
                sami_data.loc[sami_index, "Sal/TA Date (UTC)"] = -99999
                sami_data.loc[sami_index, "Salinity"] = -99999
                sami_data.loc[sami_index, "TA (Approximated)"] = -99999

            #print("sal/ta index", index)
            #print("----------------------------------")

        # If there are no same dates, saves sami row to drop and inputs NaN values for 3 columns
        else:
            sami_rows_to_drop.append(sami_index)
            sami_dates_to_drop.append(sami_data.loc[sami_index, sami_date_col_name])
            sami_data.loc[sami_index, "Sal/TA Date (UTC)"] = -99999
            sami_data.loc[sami_index, "Salinity"] = -99999
            sami_data.loc[sami_index, "TA (Approximated)"] = -99999

    print("--------------------------------------------")
    print(input_type)
    print("list of rows to drop:", sami_rows_to_drop)

    print("list of sami times to drop:", sami_dates_to_drop)

    print("number of items to drop:", len(sami_rows_to_drop))

    print("length of df before drop:", len(sami_data))

    sami_data = sami_data.drop(sami_rows_to_drop)

    print("length of df after drop:", len(sami_data))
    print("--------------------------------------------")

    # Saves sami file with sal and ta to "Ready_For_pyco2sys" folder in "Used_Data" main folder
    file_name_adjusted = my_path + "\\Used_Data\\Ready_For_pyco2sys\\" + sami_file_name + "with_sal_ta_pyco2sys_ready.csv"

    sami_data.to_csv(file_name_adjusted, index=None)



# 2018 pco2
file_formatting("\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2018_TA_NO.csv",
                "\\Used_Data\\pCO2\\pCO2_2018_Complete_Annual_Data_NO.csv",
                "pCO2_2018_Complete_Annual_Data_NO",
                "2018 pCO2")

# 2019 pco2
file_formatting("\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2019_TA_NO.csv",
                "\\Used_Data\\pCO2\\pCO2_2019_Complete_Annual_Data_NO.csv",
                "pCO2_2019_Complete_Annual_Data_NO",
                "2019 pCO2")

# 2019 ph
file_formatting("\\Used_Data\\Total_Alkalinity\\CCCE_Barnstable_2019_TA.csv",
                "\\Used_Data\\pH\\pH_2019_Complete_Annual_Data_NO.csv",
                "pH_2019_Complete_Annual_Data_NO",
                "2019 pH")

# 2020 ph
file_formatting("\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2020_TA_NO.csv",
                "\\Used_Data\\pH\\pH_2020_Complete_Annual_Data_NO.csv",
                "pH_2020_Complete_Annual_Data_NO",
                "2020 pH")

# 2021 pco2
file_formatting("\\Used_Data\\Total_Alkalinity\\HOBO_NorthFalmouth_2021_Combined_TA_NO\\HOBO_NorthFalmouth_2021_Combined_TA_NO.csv",
                "\\Used_Data\\pCO2\\pCO2_2021_Complete_Annual_Data_NO.csv",
                "pCO2_2021_Complete_Annual_Data_NO",
                "2021 pCO2")

# 2021 ph
file_formatting("\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2021_TA_NO.csv",
                "\\Used_Data\\pH\\pH_2021_Complete_Annual_Data_NO.csv",
                "pH_2021_Complete_Annual_Data_NO",
                "2021 pH")

# 2022 pco2
file_formatting("\\Used_Data\\Total_Alkalinity\\HOBO_Pocasset_2022_TA_NO.csv",
                "\\Used_Data\\pCO2\\pCO2_2022_Complete_Annual_Data_NO.csv",
                "pCO2_2022_Complete_Annual_Data_NO",
                "2022 pCO2")

# 2022 ph
file_formatting("\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2022_TA_NO.csv",
                "\\Used_Data\\pH\\pH_2022_Complete_Annual_Data_NO.csv",
                "pH_2022_Complete_Annual_Data_NO",
                "2022 pH")

# 2023 pco2
file_formatting("\\Used_Data\\Total_Alkalinity\\HOBO_Pocasset_2023_TA_NO.csv",
                "\\Used_Data\\pCO2\\pCO2_2023_Complete_Annual_Data_NO.csv",
                "pCO2_2023_Complete_Annual_Data_NO",
                "2023 pCO2")

# 2023 ph
file_formatting("\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2023_TA_NO.csv",
                "\\Used_Data\\pH\\pH_2023_Complete_Annual_Data_NO.csv",
                "pH_2023_Complete_Annual_Data_NO",
                "2023 pH")


'''
# Small test case
file_formatting("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\ta_sal_test.csv",
                "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\pco2_test.csv",
                "test")
'''
