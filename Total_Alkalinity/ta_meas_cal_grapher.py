
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
def cal_vs_meas_ta_grapher(mwra_file_loc, cal_file_loc, year_loc, save_name):
    
    my_path = os.path.abspath(os.getcwd())

    mwra_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv")

    #print(my_path+mwra_file_loc)

    cal_data = pd.read_csv(cal_file_loc)

    if year_loc == "2018 Deer Island":
        mwra_key = "SG1"
        year = 2018
        loc = "Deer Island"

    if year_loc == "2019 Deer Island":
        mwra_key = "SG1"
        year = 2019
        loc = "Deer Island"

    if year_loc == "2021 Harwich":
        mwra_key = "HAR"
        year = 2021
        loc = "Harwich"

    if year_loc == "2021 North Falmouth":
        mwra_key = "NFAL"
        year = 2021
        loc = "North Falmouth"

    if year_loc == "2022 Harwich":
        mwra_key = "HAR"
        year = 2022
        loc = "Harwich"

    if year_loc == "2022 Pocasset":
        mwra_key = "POC"
        year = 2022
        loc = "Pocasset"
    

    mwra_trunc_df = pd.DataFrame()
    mwra_trunc_df = pd.DataFrame(data=mwra_trunc_df, columns=mwra_data.columns)

    def get_year(entry):
        date = entry.split(" ")[0]
        year = date.split("/")[2]
        return year

    for index in range(0, len(mwra_data)):
        if ((mwra_data.loc[index, "STAT_ID"])) == mwra_key and (get_year(mwra_data.loc[index, "PROF_DATE_TIME_LOCAL"]) == year) :
            print("yay the date works")
            new_row = mwra_data.loc[index].copy()
            mwra_trunc_df.loc[index] = new_row
            print("yay, extracted all bottle samples for location and year")


    match_cal_ta_list = []
    match_cal_ta_time_list = []
    for indexA in range(0, len(mwra_trunc_df)):
        mwra_ta = mwra_trunc_df.loc[indexA, ""]
        mwra_date = mwra_trunc_df.loc[indexA, "PROF_DATE_TIME_LOCAL"]
        mwra_date_dt = pd.to_datetime(mwra_date, format="%m/%d/%Y %H:%M")

        if year == "2018":
            if (mwra_date_dt >= dt(2018,3,11,2,0)) & (mwra_date_dt <= dt(2018,11,4,2,0)):
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)

        if year == "2021":
            if (mwra_date_dt >= dt(2021,3,14,2,0)) & (mwra_date_dt <= dt(2021,11,7,2,0)):
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)

        if year == "2022":
            if (mwra_date_dt >= dt(2022,3,13,2,0)) & (mwra_date_dt <= dt(2021,11,6,2,0)):
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)


        test_ta_list = []
        test_ta_diff_list = []
        test_ta_date_list = []
        start_time = mwra_date_dt_utc - pd.Timedelta(hours = 1)
        end_time = mwra_date_dt_utc - pd.Timedelta(hours = 1)    
        for indexB in range(0, len(cal_data)):
            cal_date_dt = pd.to_datetime(cal_data.loc[indexB, "Datetime_UTC"], format="%Y-%m-%d %H:%M:%S")
            if (cal_date_dt >= start_time) & (cal_date_dt <= end_time):
                ta_diff = abs(mwra_ta-(cal_data.loc[indexB, "TA (Approximated)"]))
                test_ta_diff_list.append(ta_diff)
                test_ta_date_list.append(cal_date_dt)
                test_ta_list.append(cal_data.loc[indexB, "TA (Approximated)"])
        
        print(test_ta_diff_list)
        if test_ta_diff_list != []:
            min_ta_diff = min(test_ta_diff_list)
            min_ta_diff_index = test_ta_diff_list.index(min_ta_diff)
            match_cal_ta = test_ta_list[min_ta_diff_index]
            match_cal_ta_time = test_ta_date_list[min_ta_diff_index]
            match_cal_ta_list.append(match_cal_ta)
            match_cal_ta_time_list.append(match_cal_ta_time)

    mwra_trunc_df["Match_Cal_TA"] = match_cal_ta_list
    mwra_trunc_df["Match_Cal_TA_Datetime"] = match_cal_ta_time_list
         
    # Saves sami file with sal and ta to "Ready_For_pyco2sys" folder in "Used_Data" main folder
    file_name_adjusted = my_path + "\\Total_Alkalinity\\MWRA_CAL_TA_Data\\" + save_name + ".csv"

    mwra_trunc_df.to_csv(file_name_adjusted, index=None)



# 2018 pco2
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2018_TA_NO.csv",               
                "2018 Deer Island",
                "pCO2_2018_Cal_Mea_TA_Data")

# 2019 pco2
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2019_TA_NO.csv",               
                "2019 Deer Island",
                "pCO2_2019_Cal_Mea_TA_Data")


# 2021 Harwich
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2021_TA_NO.csv",               
                "2021 Harwich",
                "pH_2021_Cal_Mea_TA_Data")

# 2021 North Falmouth
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\HOBO_NorthFalmouth_2021_Combined_TA_NO\\HOBO_NorthFalmouth_2021_Combined_TA_NO.csv",               
                "2021 North Falmouth",
                "pCO2_2021_Cal_Mea_TA_Data")

# 2022 pco2
cal_vs_meas_ta_grapher("\\Used_Data\\Total_Alkalinity\\HOBO_Pocasset_2022_TA_NO.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\Total_Alkalinity\HOBO_Pocasset_2022_TA_NO.csv",
                "2022 Pocasset",
                "pCO2_2022_Cal_Mea_TA_Data")

# 2022 ph
cal_vs_meas_ta_grapher("\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2022_TA_NO.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2022_TA_NO.csv",
                "2022 Harwich",
                "pH_2022_Cal_Mea_TA_Data")

