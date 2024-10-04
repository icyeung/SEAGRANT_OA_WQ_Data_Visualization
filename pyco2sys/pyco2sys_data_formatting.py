# Need to create depth column (dbar) for sami
# 1.5m deep -> pressure ~1.15 atm -> 11.65237 dbar
# Match up closest ta/sal for each sami measurement

# ph & pco2 date as y-m-d
# sal data format varies by type

import pandas as pd
import datetime as datetime
from datetime import datetime as dt
import numpy as np

# Converts from H:M:S to time/24    
def time_frac_cal(time):
    time_hour = int(time.split(":")[0])
    time_minute = int(time.split(":")[1])
    time_min_percent = round(time_minute/60, 4)
    time_frac_conv = float(time_hour + time_min_percent)
    return time_frac_conv

# Main program to call for formatting data file for pyco2sys
# Formatted file will be outputted using sami file as base
def file_formatting(sal_ta_file_loc, sami_file_loc, sami_file_name):
    
    sal_ta_data = pd.read_csv(sal_ta_file_loc)
    sami_data = pd.read_csv(sami_file_loc)

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


    # for date in sami, finds the same date in sal/ta file 
    # then calculates the closest time to that time stamp and obtain row #
    # then locates the corresponding sal/ta values from that row
    # saves all to three lists
    # works under the assumption data is chronological
    
    index=0     # Index for looking through sal/ta file
    opt_time_df_index = 0   # Initializes index to hold last used index for sami matching
    opt_sal_ta_time_index_list = []     # Holds all indices used for sami matching
    sami_rows_to_drop = []      # Rows of sami where there is no matching sal/ta; will be dropped

    # Goes through all the sami entires individually
    # For each sami row, 
    for sami_index in range(0, len(sami_data["Date (UTC)"])):
        # Obtains sami date and time
        sami_dt = sami_data["Date (UTC)"].iloc[sami_index]
        sami_date = sami_dt.split(" ")[0]
        print("sami datetime", sami_dt)
        ys, ms, ds = [int(part) for part in sami_date.split("-")]
        # Obtains sami time as time frac
        sami_time_frac = time_frac_cal(sami_dt.split(" ")[1])
        print("sami time frac", sami_time_frac)

        same_date_time_list = []    # Holds all time entries for same date for sal/ta
        same_date_sal_index_list = []   # Holds all corresponing indices for appropriate time entires
        print("index before while", index)
        
        index = opt_time_df_index   # Sets the first sal/ta entry to look at each time is the one that was used to pair for the last sami; reduces search redundancy
        while index < len(sal_ta_data):
            sal_ta_dt = sal_ta_data["DateTime (UTC)"].iloc[index]   # Obtains date and time for each sal/ta row
            print("sal date dt", sal_ta_dt)

            sal_ta_date = sal_ta_dt.split(" ")[0]   # Obtains date only from the date time
            m1, d1, y1 = [int(sal_part) for sal_part in sal_ta_date.split("/")]

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
        
        print("index after while loop", index)
        
        
        # Once all same dates have been found:
        # If there are same dates, goes through all times from the same day and finds the difference between them and the sami time
        if len(same_date_time_list) != 0:
            difference_list = []
            for time in same_date_time_list:  
                difference = abs(float(sami_time_frac-time))
                print(difference)         
                difference_list.append(difference)
            print("list of time diff", difference_list)


            print("same date index", same_date_sal_index_list)
            print("same date list of times", same_date_time_list)
            
            
            # Identifies the smallest time difference
            min_time_diff = min(difference_list)
            
            print("min time diff", min_time_diff)
            
            # Checks to see if smallest time difference is within 1 hour
            # If it is:
            if min_time_diff <= 1:
                # Identifies index in list of differences
                min_time_diff_index = difference_list.index(min_time_diff)
                print("min time diff index", min_time_diff_index)

                #opt_time = same_date_time_list[min_time_diff_index]

                # Uses difference index to find the value in sal/ta same day index list
                opt_time_df_index = same_date_sal_index_list[min_time_diff_index]
                # Appends that index to list
                opt_sal_ta_time_index_list.append(opt_time_df_index)

                # Finds corresponding sal/ta datettime, sal, and ta values and copies them to sami file
                sal_dt_value = sal_ta_data.loc[opt_time_df_index, "DateTime (UTC)"]
                sami_data.loc[sami_index, "Sal/TA Date (UTC)"] = sal_dt_value
                
                sal_value = sal_ta_data.loc[opt_time_df_index, "Salinity"]
                sami_data.loc[sami_index, "Salinity"] = sal_value
                
                sami_data.loc[sami_index, "TA (Approximated)"] = sal_ta_data.loc[opt_time_df_index, "TA (Approximated)"]

            print("sal/ta index", index)
            print("----------------------------------")

        # If there are no same dates, saves sami row to drop and inputs NaN values for 3 columns
        else:
            sami_rows_to_drop.append(sami_index)
            sami_data["Sal/TA Date (UTC)"].iloc[sami_index] = np.NaN
            sami_data["Salinity"].iloc[sami_index] = np.NaN
            sami_data["TA (Approximated)"].iloc[sami_index] = np.NaN

    '''
    sal_ta_dt_list = []
    salinity_list = []
    alkalinity_list = []
    for indexA in opt_sal_ta_time_index_list:
        sal_ta_opt_dt = sal_ta_data["DateTime (UTC)"].iloc[indexA]
        sal_ta_dt_list.append(sal_ta_opt_dt)

        salinity = sal_ta_data["Salinity"].iloc[indexA]
        salinity_list.append(salinity)

        alkalinity = sal_ta_data["TA (Approximated)"].iloc[indexA]
        alkalinity_list.append(alkalinity)

    sami_data["Sal/TA Date (UTC)"] = sal_ta_dt_list

    sami_data["Salinity"] = salinity_list

    sami_data["TA (Approximated)"] = alkalinity_list
    '''

    print(sami_rows_to_drop)

    

    file_name_adjusted = sami_file_name + "with_sal_ta_pyco2sys_ready.csv"

    sami_data.to_csv(file_name_adjusted, index=None)




file_formatting("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2018_TA_NO.csv",
                "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\pCO2\\pCO2_2018_Complete_Annual_Data_NO.csv",
                "pCO2_2018_Complete_Annual_Data_NO")

'''
file_formatting("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\ta_sal_test.csv",
                "C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\pco2_test.csv",
                "test")
'''
