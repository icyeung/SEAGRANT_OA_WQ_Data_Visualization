# Matches surface bottle TA to calculated TA from conductivity


import pandas as pd
import datetime as datetime
from datetime import datetime as dt
import numpy as np
import os
import math

# Converts from H:M:S to time/24    
def time_frac_cal(time):
    time_hour = int(time.split(":")[0])
    time_minute = int(time.split(":")[1])
    time_min_percent = round(time_minute/60, 4)
    time_frac_conv = float(time_hour + time_min_percent)
    return time_frac_conv


def cal_vs_meas_ta_grapher(mwra_file_loc, cal_file_loc, year_loc, cal_time_name, cal_time_format, save_name):
    
    my_path = os.path.abspath(os.getcwd())

    mwra_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv")

    #print(my_path+mwra_file_loc)

    cal_data = pd.read_csv(cal_file_loc)

    #print(cal_data)

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
    

    def get_year(entry):
        date = entry.split(" ")[0]
        year = date.split("/")[2]
        return year

    def get_depth(name):
        print(name)
        print(type(name))
        if name.split("-")[0] == "Poc" or name.split("-")[0] == "NFal":
            return "s"
        if not(isinstance(name, float)): 
            depth = name.split("-")[1]
            if len(depth) == 1:
                return depth
            else:
                return depth[0]
        else:
            return "d"

    
    mwra_trunc_date_list =[]
    mwra_trunc_ta_list = [] 
    for index in range(0, len(mwra_data)):
        #print(mwra_data.loc[index, "STAT_ID"])
        #print(get_year(mwra_data.loc[index, "PROF_DATE_TIME_LOCAL"]))
        if ((mwra_data.loc[index, "STAT_ID"]) == mwra_key) & (int(get_year(mwra_data.loc[index, "PROF_DATE_TIME_LOCAL"])) == year):
            print(get_depth(mwra_data.loc[index, "Station_D"]))
            if (get_depth(mwra_data.loc[index, "Station_D"]) == "s") or (get_depth(mwra_data.loc[index, "Station_D"]) == "S"):
                #print("yay the date works")
                mwra_trunc_date_list.append(mwra_data.loc[index, "PROF_DATE_TIME_LOCAL"])
                mwra_trunc_ta_list.append(mwra_data.loc[index, "TA in (mmol/kgSW)"])
                #print("yay, extracted all bottle samples for location and year")

    mwra_trunc_df = pd.DataFrame({"PROF_DATE_TIME_LOCAL": mwra_trunc_date_list, "TA in (mmol/kgSW)": mwra_trunc_ta_list})

    #print(mwra_trunc_df)

    match_cal_ta_list = []
    match_cal_ta_time_list = []
    indexA = 0
    mwra_time_utc_list = []
    while indexA < (len(mwra_trunc_df)):
        mwra_ta = mwra_trunc_df.loc[indexA, "TA in (mmol/kgSW)"]
        #print(mwra_ta)
        mwra_date = mwra_trunc_df.loc[indexA, "PROF_DATE_TIME_LOCAL"]
        mwra_date_dt = pd.to_datetime(mwra_date, format="%m/%d/%Y %H:%M")

        #print(year)
        #print(mwra_date_dt)
        #print((mwra_date_dt >= dt(2018,3,11,2,0)))
        #print((mwra_date_dt <= dt(2018,11,4,2,0)))
        #print(mwra_date_dt + pd.Timedelta(hours=4))

        
        if year == 2018:
            if ((mwra_date_dt >= dt(2018,3,11,2,0)) & (mwra_date_dt <= dt(2018,11,4,2,0))):
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
                #print("hi")
                #print(mwra_date_dt_utc)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)

        if year == 2019:
            if (mwra_date_dt >= dt(2019,3,10,2,0)) & (mwra_date_dt <= dt(2019,11,3,2,0)):
                #print("in 2019")
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)

        if year == 2021:
            if (mwra_date_dt >= dt(2021,3,14,2,0)) & (mwra_date_dt <= dt(2021,11,7,2,0)):
                #print("in 2021")
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)

        if year == 2022:
            if (mwra_date_dt >= dt(2022,3,13,2,0)) & (mwra_date_dt <= dt(2022,11,6,2,0)):
                #print("in 2022")
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=4)
            else:
                mwra_date_dt_utc = mwra_date_dt + pd.Timedelta(hours=5)
        #print(mwra_date_dt_utc)
        #print(cal_data)
        #print(indexA, mwra_date_dt_utc)
        mwra_time_utc_list.append(mwra_date_dt_utc)
        


        #print(match_cal_ta_time_list)
        test_ta_list = []
        test_ta_diff_list = []
        test_ta_date_list = []
        
        start_time = mwra_date_dt_utc - pd.Timedelta(hours = 1)
        end_time = mwra_date_dt_utc + pd.Timedelta(hours = 1)    
        
        #print("start time",start_time)
        #print("end time", end_time)
        indexB = 0
        while indexB < len(cal_data):
            cal_date_dt = pd.to_datetime(cal_data.loc[indexB, cal_time_name], format=cal_time_format)
            #print(cal_date_dt)
            if (cal_date_dt >= start_time) & (cal_date_dt <= end_time):
                
                ta_diff = abs(mwra_ta-(cal_data.loc[indexB, "TA (Approximated)"]))
                
                test_ta_diff_list.append(ta_diff)
                test_ta_date_list.append(cal_date_dt)
                test_ta_list.append(cal_data.loc[indexB, "TA (Approximated)"])
            indexB +=1
            #print(test_ta_diff_list)
        
        #print(test_ta_diff_list)
        if test_ta_diff_list != []:
            min_ta_diff = min(test_ta_diff_list)
            min_ta_diff_index = test_ta_diff_list.index(min_ta_diff)
            match_cal_ta = test_ta_list[min_ta_diff_index]
            match_cal_ta_time = test_ta_date_list[min_ta_diff_index]
            match_cal_ta_list.append(match_cal_ta)
            match_cal_ta_time_list.append(match_cal_ta_time)
        else:
            match_cal_ta_list.append(0)
            match_cal_ta_time_list.append(0)
        indexA +=1

    #print(mwra_trunc_df)
    #print(match_cal_ta_time_list)
    #print(match_cal_ta_list)
    mwra_trunc_df["MWRA_UTC"] = mwra_time_utc_list
    mwra_trunc_df["Match_Cal_TA"] = match_cal_ta_list
    mwra_trunc_df["Match_Cal_TA_Datetime"] = match_cal_ta_time_list
    
    # Saves sami file with sal and ta to "Ready_For_pyco2sys" folder in "Used_Data" main folder
    file_name_adjusted = my_path + "\\Total_Alkalinity\\MWRA_CAL_TA_Data\\" + save_name + ".csv"

    mwra_trunc_df.to_csv(file_name_adjusted, index=None)



# 2018 pco2
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2018_TA_NO.csv",               
                "2018 Deer Island",
                "DateTime (UTC)",
                "%m/%d/%Y %H:%M",
                "pCO2_2018_Cal_Mea_TA_Data")

# 2019 pco2
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\Eureka_DeerIsland_2019_TA_NO.csv",               
                "2019 Deer Island",
                "Time (UTC)",
                "%m/%d/%Y %H:%M",
                "pCO2_2019_Cal_Mea_TA_Data")


# 2021 Harwich
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2021_TA_NO.csv",               
                "2021 Harwich",
                "Datetime_Adjusted_UTC+1",
                "%m/%d/%Y %H:%M",
                "pH_2021_Cal_Mea_TA_Data")

# 2021 North Falmouth
cal_vs_meas_ta_grapher("MWRA\\MWRA_Data\\MWRA_TA_DIC_2017_to_2022_v20240330.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\HOBO_NorthFalmouth_2021_Combined_TA_NO\\HOBO_NorthFalmouth_2021_Combined_TA_NO.csv",               
                "2021 North Falmouth",
                "Date (UTC)",
                "%Y-%m-%d %H:%M:%S",
                "pCO2_2021_Cal_Mea_TA_Data")

# 2022 pco2
cal_vs_meas_ta_grapher("\\Used_Data\\Total_Alkalinity\\HOBO_Pocasset_2022_TA_NO.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\Total_Alkalinity\HOBO_Pocasset_2022_TA_NO.csv",
                "2022 Pocasset",
                "Date (UTC)",
                "%Y-%m-%d %H:%M:%S",
                "pCO2_2022_Cal_Mea_TA_Data")

# 2022 ph
cal_vs_meas_ta_grapher("\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2022_TA_NO.csv",
                "C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\Total_Alkalinity\\NERRS_Metoxit_2022_TA_NO.csv",
                "2022 Harwich",
                "Datetime_Adjusted_UTC+1",
                "%m/%d/%Y %H:%M",
                "pH_2022_Cal_Mea_TA_Data")

