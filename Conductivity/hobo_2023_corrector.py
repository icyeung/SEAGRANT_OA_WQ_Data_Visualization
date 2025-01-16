# Use 5/17 SBM value as the first BBC sample for the beginning of HOBO
#Calculate the difference between the “first” BBC and the HOBO and translate by that amount
#If period of time is greater than 2 weeks between BBC, create false BBC point (average of all BBC to use)
#Find midpoint of 2 BBC samples, correct corresponding period of HOBO to the BBC measurement until midpoint
#See next slide for an example
#For period after the last true BBC sample, use false BBC average after the 1 week period and correct remaining period to that

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as md
import datetime


# Cuts original data files so that the file now only contains period we are interested in
def commonDataRange(data_df, data_type, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    if data_type == "BBC":
        parameter = "SAMP_DATE"
    elif data_type == "SBM" or data_type == "HOBO":
        parameter = "Date"

    logger_dates_list = data_df[parameter].tolist()
    for date in logger_dates_list:
        if date == np.nan:
            break
        else:
            print(date)
            m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
            date1 = dt(y1, m1, d1)
      
            if not((date1 <= date3) & (date1>= date2)):
                invalid_date_list.append(date)
                invalid_date_index_list.append(logger_date_index)
            else:
                print("bruh it's working?", date)
            logger_date_index += 1
    data_df = data_df.drop(invalid_date_index_list)
    data_df = data_df.reset_index()
    data_df = data_df.drop(columns = "index")
    
    return data_df



# Converts AM/PM to 24 hour time
# If timestamp has seconds, nosec = False, else nosec = True
def timeConverterto24(time, nosec):
    ending = time.split(" ")[-1]
    time_number = time.split(" ")[0]
    if nosec == True:
        h1, m1 = [int(number) for number in time_number.split(":")]
    if nosec == False:
        h1, m1, s1 = [int(number) for number in time_number.split(":")]
    if ending == "PM" and h1 != 12:
        h1 += 12
    if ending == "AM" and h1 == 12:
        h1 = 0
    if nosec == True:
        converted_time = str(h1) + ":" + str(m1)
        #converted_time_dt = dt.strptime(converted_time, "%H:%M")
    else:
        converted_time = str(h1) + ":" + str(m1) + ":" + str(s1)
        #converted_time_dt = dt.strptime(converted_time, "%H:%M:%S")
    return converted_time


#Applies custom correction to desired time period
def commonDataRangeCorrector (data_df, correction_amount, start_date, end_date):
    for index in range(0, len(data_df)):
        date = data_df.loc[index, "Datetime_noyear"]
        date_dt = dt.strptime(date, "%m/%d/%Y %H:%M")
        start_date_dt = dt.strptime(start_date, "%m/%d/%Y %H:%M")
        end_date_dt = dt.strptime(end_date, "%m/%d/%Y %H:%M")
        if not((date_dt <= start_date_dt) & (date_dt > end_date_dt)):
            sal_value = data_df.loc[index, "Salinity Value (Offset +15)"]
            corrected_sal_value = sal_value+correction_amount
            data_df.loc[index, "Salinity_Value_Corrected"] = corrected_sal_value



# Main function for correction
def hobo_2023_corrector(hobo_file, bbc_file, sbm_file, correction_period, correcction_placement):

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # HOBO #1 2022 (Pocasset)
    hobo_data = pd.read_csv(os.path.join(__location__, hobo_file))

    #BBC PR1 2023
    BBC_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), bbc_file))

    # Scallop Bay Marina 2023 (SBM)
    sbm_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), sbm_file))

    sbm_data_fitted = commonDataRange(sbm_data, "SBM", "01-01-2023", "12-31-2023")


    #Formatting BBC Data
    bbc_d_date_list = []
    bbc_d_time_list = []
    bbc_d_sal_list = []
    bbc_d_samp_depth_list = []
    bbc_d_total_depth_list = []

    for bbc_index in range(0, len(BBC_data)):
        if BBC_data.loc[bbc_index, "STN_ID"] == "PR1":
            #print(BBC_data.loc[bbc_index, "SAMP_DATE"].split("/")[2])
            if BBC_data.loc[bbc_index, "SAMP_DATE"].split("/")[2] == "2023":
                #print(BBC_data.loc[bbc_index, "UNIQUE_ID"].split("-")[-3])
                if BBC_data.loc[bbc_index, "UNIQUE_ID"].split("-")[-3] == "D":
                    bbc_d_date_list.append(BBC_data.loc[bbc_index, "SAMP_DATE"])
                    bbc_d_time_list.append(BBC_data.loc[bbc_index, "TIME"])
                    bbc_d_sal_list.append(BBC_data.loc[bbc_index, "SAL_FIELD"])
                    bbc_d_samp_depth_list.append(BBC_data.loc[bbc_index, "SAMPDEP_M"])
                    bbc_d_total_depth_list.append(BBC_data.loc[bbc_index, "TOTDEP_M"])

    bbc_deep_df = pd.DataFrame({"SAMP_DATE": bbc_d_date_list, "TIME": bbc_d_time_list, "SAL_FIELD": bbc_d_sal_list,
                                "SAMPDEP_M": bbc_d_samp_depth_list, "TOTDEP_M": bbc_d_total_depth_list})

    bbc_d_24_time_list = []
    for time in bbc_d_time_list:
        bbc_d_24_time_list.append(timeConverterto24(time, True))
        
    bbc_d_datetime_utc_list = []
    for bbc_indexb in range(0, len(bbc_d_24_time_list)):
        bbc_d_datetime_string = bbc_d_date_list[bbc_indexb] + " " + bbc_d_24_time_list[bbc_indexb]
        # Convert the combined string to a datetime object
        bbc_d_datetime_object = dt.strptime(bbc_d_datetime_string, "%m/%d/%Y %H:%M")
        if (bbc_d_datetime_object >= dt(2023,3,12,2,0)) & (bbc_d_datetime_object <= dt(2023,11,5,2,0)):
            bbc_d_datetime_utc = bbc_d_datetime_object + pd.Timedelta(hours=4)
        else:
            bbc_d_datetime_utc = bbc_d_datetime_object + pd.Timedelta(hours=5)
        bbc_d_datetime_utc_list.append(bbc_d_datetime_utc)

    bbc_deep_df["Datetime"] = bbc_d_datetime_utc_list

    bbc_d_datetime_noyear_list = []
    for date in bbc_d_datetime_utc_list:
        date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
        date_no_year = str(date_no_year)
        dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
        bbc_d_datetime_noyear_list.append(dt_date_no_year)

    bbc_deep_df["Datetime_noyear"] = bbc_d_datetime_noyear_list



    #Formatting SBM Data Date
    sbm_datetime_noyear_list = []
    for date in sbm_data_fitted["Date"]:
        date_no_year = '{:%m-%d}'.format(dt.strptime(str(date), '%m/%d/%Y'))
        date_no_year = str(date_no_year)
        dt_date_no_year = dt.strptime(date_no_year, "%m-%d")
        sbm_datetime_noyear_list.append(dt_date_no_year)
    
    sbm_data_fitted["Datetime_noyear"] = sbm_datetime_noyear_list

    #Formatting HOBO Date 
    hobo_sal = hobo_data["Salinity Value (Offset +15)"]
    hobo_date_with_year = hobo_data["Date (UTC)"]
    hobo_date_no_year = []
    for date in hobo_date_with_year:
        date_no_year = '{:%m-%d %H:%M}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
        date_no_year = str(date_no_year)
        dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M")
        dt_date_no_year_time_shift = dt_date_no_year - datetime.timedelta(hours=3)
        hobo_date_no_year.append(dt_date_no_year_time_shift)
    hobo_data["Datetime_noyear"] = hobo_date_no_year
    hobo_data["Salinity_Value_Corrected"] = ""



    # Dataframes for hobo, bbc, and sbm are now created
    # hobo_data, bbc_deep_df, sbm_data_fitted
    bbc_deep_df.to_csv("bbc_2023_deep.csv", index=None)
    hobo_data.to_csv("hobo_2023.csv", index=None)
    sbm_data_fitted.to_csv("sbm_2023.csv", index=None)


    # Correction begins here
    bbc_index = -1
    while bbc_index < len(bbc_deep_df):
        if bbc_index == -1:
            sbm_index = sbm_data_fitted.isin(['5/17/2023']).any(axis=1).idxmax()
            correction_amt = sbm_index.loc[sbm_index, "Salinity (psu)"]-hobo_data.loc[0, "Salinity Value (Offset +15)"]
            commonDataRangeCorrector(hobo_data, correction_amt, "1900-05-17 00:00", bbc_deep_df.loc[0, "Datetime_noyear"])
        else:
            if (bbc_deep_df.loc[bbc_index+1, "Datetime_noyear"] - bbc_deep_df.loc[bbc_index, "Datetime_noyear"].days) > correction_period:
                mid_length = int((bbc_deep_df.loc[bbc_index+1, "Datetime_noyear"] - bbc_deep_df.loc[bbc_index, "Datetime_noyear"].days)/2)
                midpoint_time = bbc_deep_df.loc[bbc_index, "Datetime_noyear"] + datetime.timedelta(days=mid_length)
                bbc_avg_value = round((sum(bbc_deep_df["SAL_FIELD"])/len(bbc_deep_df["SAL_FIELD"])), 4)
                correction = bbc_avg_value - 
                commonDataRangeCorrector(hobo_data, correction, bbc_deep_df.loc[bbc_index, "Datetime_noyear"], )
        bbc_counter += 1


# Test Run 1
hobo_2023_corrector("HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Pocasset_12-9-22_1_NO_offset.csv",
                    "Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv",
                    "Conductivity\\Sourced_Data\\Scallop_Bay_Marina\\Scallop_Bay_Marina_2023_Salinity.csv",
                    13,
                    "after")