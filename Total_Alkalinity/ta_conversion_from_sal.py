# TA Linear Regression Line (Rheuban 2019)
# Slope: 54.6
# Y-Intercept: 409
# Input: Salinity PSU
# Output: TA umol/kg

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


def ta_conversion (sal_file_loc, sal_source, file_save_name):
    
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    sal_data = pd.read_csv(sal_file_loc)

    if sal_source == "HOBO 2021":
        sal_value_list = sal_data["Salinity Value (Offset +4)"]
    
    if sal_source == "HOBO 2022":
        sal_value_list = sal_data["Salinity Value (Offset +15)"]
    
    if sal_source == "HOBO 2023":
        sal_value_list = sal_data["Salinity Value (Offset +15)"]
                                  
    if sal_source == "Eureka":
        sal_value_list = sal_data["Salinity"]

    if sal_source == "NERRS":
        sal_value_list = sal_data["Sal"]
    
    if sal_source == "CCCE":
        sal_value_list = sal_data["Salinity"]



    def sal_to_ta(sal):
        if sal == 0 or sal == np.NaN or sal == 0.01:
            ta = 0
        else:
            ta = (54.6*sal) + 409
        return ta


    ta_value_list = []
    for value in sal_value_list:
        ta_value = sal_to_ta(value)
        ta_value_list.append(ta_value)

    sal_data["TA (Approximated)"] = ta_value_list

    print(sal_data)

    sal_data.to_csv(file_save_name, index = None)


# NERRS Metoxit 2020
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2020_OR.csv",
              "NERRS",
              "NERRS_Metoxit_2020_TA_NO.csv")


# NERRS Metoxit 2021
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2021_OR.csv",
              "NERRS",
              "NERRS_Metoxit_2021_TA_NO.csv")


# NERRS Metoxit 2022
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2022_OR.csv",
              "NERRS",
              "NERRS_Metoxit_2022_TA_NO.csv")


# NERRS Metoxit 2023
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\wqbmpwq2023_OR.csv",
              "NERRS",
              "NERRS_Metoxit_2023_TA_NO.csv")

'''
# CCCE Barnstable 2019
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\CCCE_Barnstable_Salinity_Data_2019_UTC.csv",
              "CCCE",
              "CCCE_Barnstable_2019_TA.csv")
'''

# Eureka 2018
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\Deer_Island-SG1-2018_Annual_Data_UTC_OR.csv",
              "Eureka",
              "Eureka_DeerIsland_2018_TA_NO.csv")


# Eureka 2019
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\Deer_Island-SG1-2019_Annual_Data_UTC_OR.csv",
              "Eureka",
              "Eureka_DeerIsland_2019_TA_NO.csv")

'''

# HOBO 2021 Part 1
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\Salinity_Carolina_FiddlersCove_9-28-21_2_NO_offset.csv",
              "HOBO 2021",
              "HOBO_NorthFalmouth_06-092021_TA.csv")


# HOBO 2021 Part 2
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\Salinity_Carolina_FiddlersCove_12-10-21_2_NO_offset.csv",
              "HOBO 2021",
              "HOBO_NorthFalmouth_09-122021_TA.csv")


# HOBO 2022
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\Salinity_Carolina_Pocasset_12-9-22_1_NO_offset.csv",
              "HOBO 2022",
              "HOBO_Pocasset_2022_TA.csv")


# HOBO 2023
ta_conversion("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\Salinity\\Salinity_Carolina_Pocasset_12-9-22_1_NO_offset_all.csv",
              "HOBO 2023",
              "HOBO_Pocasset_2023_TA.csv")
    
'''