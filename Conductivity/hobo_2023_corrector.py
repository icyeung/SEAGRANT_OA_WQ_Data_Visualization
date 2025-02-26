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
            #print(date)
            m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
            date1 = dt(y1, m1, d1)
      
            if not((date1 <= date3) & (date1>= date2)):
                invalid_date_list.append(date)
                invalid_date_index_list.append(logger_date_index)
            #else:
                #print("bruh it's working?", date)
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

def find_closest_hobo(hobo_file, date, start_index):

        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        index = start_index
        isAfter = False
        while not(isAfter):
            #print("in find closest hobo")

            if (hobo_file.loc[index, "Datetime_noyear"] < date_dt) and not(isAfter):
                index +=1
                #print(hobo_file.loc[index, "Datetime_noyear"])
                #print(date_dt)
                #print(index)
            else:
                isAfter = True
                #print("another one done", index)
                break
        return index

# output will give you list of type of range and start/end date(s)
# range = 1; start and end date for bbc_index
# range = 2; start and end date for bbc_index (7 days after first measurement) and start and end date of bbc_index +1 (7 days before )
def find_midpoint_range(bbc_deep_df, bbc_index):
    output_list = []

    if bbc_index == -1:

        #print("in find midpoint bbc-1")
        bbc_false_sample_date = dt(1900,5,17,14,6,18)
        bbc_next_sample_date = bbc_deep_df.loc[0, "Datetime_noyear"]
        time_between = (bbc_next_sample_date-bbc_false_sample_date)
        time_between_days = time_between.days
        time_between_sec = time_between.seconds
            
        if time_between_days > 14 or (time_between_days == 14 and time_between_sec > 0): 
            bbc_first_end_date = bbc_false_sample_date+datetime.timedelta(days = 7)
            bbc_second_start_date = bbc_next_sample_date-datetime.timedelta(days = 7)
            output_list.append("2")
            output_list.append(bbc_false_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_first_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))

        if time_between_days < 14 or (time_between_days == 14 and time_between_sec == 0):
            time_between_allsec = time_between.total_seconds()
            midlength_time_between = time_between_allsec/2
            bbc_false_end_date = bbc_false_sample_date+datetime.timedelta(seconds=midlength_time_between)
            bbc_second_start_date = bbc_false_end_date+datetime.timedelta(seconds=1)
            output_list.append("1")
            output_list.append(bbc_false_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_false_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))

    if bbc_index == len(bbc_deep_df)-1:

        #print("in find midpoint lenbbc-1")
        bbc_sample_date = bbc_deep_df.loc[bbc_index, "Datetime_noyear"]
        bbc_end_date = bbc_deep_df.loc[bbc_index, "Datetime_noyear"]+datetime.timedelta(days = 7)
        output_list.append("2")
        output_list.append(bbc_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
        output_list.append(bbc_end_date.strftime("%Y-%m-%d %H:%M:%S"))

    if bbc_index != -1 and bbc_index != len(bbc_deep_df)-1:
        
        #print("in find midpoint !=-1")
        bbc_sample_date = bbc_deep_df.loc[bbc_index, "Datetime_noyear"]
        bbc_next_sample_date = bbc_deep_df.loc[bbc_index+1, "Datetime_noyear"]
        time_between = (bbc_next_sample_date-bbc_sample_date)
        time_between_days = time_between.days
        time_between_sec = time_between.seconds
        if time_between_days > 14 or (time_between_days == 14 and time_between_sec > 0): 
            bbc_first_end_date = bbc_sample_date+datetime.timedelta(days = 7)
            bbc_second_start_date = bbc_next_sample_date-datetime.timedelta(days = 7)
            output_list.append("2")
            output_list.append(bbc_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_first_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))

        if time_between_days < 14 or (time_between_days == 14 and time_between_sec == 0):
            time_between_allsec = time_between.total_seconds()
            midlength_time_between = time_between_allsec/2
            bbc_first_end_date = bbc_sample_date+datetime.timedelta(seconds=midlength_time_between)
            bbc_second_start_date = bbc_first_end_date+datetime.timedelta(seconds=1)
            output_list.append("1")
            output_list.append(bbc_sample_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_first_end_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_second_start_date.strftime("%Y-%m-%d %H:%M:%S"))
            output_list.append(bbc_next_sample_date.strftime("%Y-%m-%d %H:%M:%S"))   
    
    print("midpoint range output", output_list)
    return(output_list)

corrected_sal_value_list = []

#Applies custom correction to desired time period
def commonDataRangeCorrector (data_df, correction_amount, start_date, end_date):
    
    data_df['Datetime_noyear'] = pd.to_datetime(data_df['Datetime_noyear'], format="%Y-%m-%d %H:%M:%S")


    start_date_dt = dt.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date_dt = dt.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    
    

    for index in range(0, len(data_df)):
        
        
        date_dt = data_df.loc[index, "Datetime_noyear"]
        
        
        if ((date_dt >= start_date_dt) & (date_dt <= end_date_dt)):
            #print("in date range corrector")
            #print(date_dt)
            #print(start_date_dt)
            #print(end_date_dt)
            sal_value = data_df.loc[index, "Salinity Value (Offset +15)"]
            corrected_sal_value = sal_value+correction_amount
            corrected_sal_value_list.append(corrected_sal_value)
            data_df.at[index, "Salinity_Value_Corrected"] = corrected_sal_value
            #print(corrected_sal_value)
            #print(correction_amount)

    #print(corrected_sal_value_list)

    return data_df



# Main function for correction
def hobo_2023_corrector(hobo_file, bbc_file, sbm_file):

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # HOBO #1 2022 (Pocasset)
    hobo_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), hobo_file))

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
    hobo_date_with_year = hobo_data["DateTime (UTC)"]
    hobo_date_no_year = []
    for date in hobo_date_with_year:
        date_no_year = '{:%m-%d %H:%M}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
        date_no_year = str(date_no_year)
        dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M")
        dt_date_no_year_time_shift = dt_date_no_year - datetime.timedelta(hours=3)
        hobo_date_no_year.append(dt_date_no_year_time_shift)
    hobo_data["Datetime_noyear"] = hobo_date_no_year
    hobo_data["Salinity_Value_Corrected"] = [0]*len(hobo_data)

    bbc_deep_df = bbc_deep_df.drop([2])
    bbc_deep_df = bbc_deep_df.reset_index()

    # Dataframes for hobo, bbc, and sbm are now created
    # hobo_data, bbc_deep_df, sbm_data_fitted
    bbc_deep_df.to_csv("bbc_2023_deep.csv", index=None)
    hobo_data.to_csv("hobo_2023.csv", index=None)
    sbm_data_fitted.to_csv("sbm_2023.csv", index=None)


    # Correction begins here
    bbc_indexc = -1
    while bbc_indexc < len(bbc_deep_df):
        if bbc_indexc == -1:
            sbm_index = sbm_data_fitted.isin(['5/17/2023']).any(axis=1).idxmax()
            #print(sbm_index)
            correction_amt_1 = sbm_data_fitted.loc[sbm_index, "Salinity (psu)"]-hobo_data.loc[0, "Salinity Value (Offset +15)"]
            time_ranges = find_midpoint_range(bbc_deep_df, bbc_indexc)
            start_time_1 = time_ranges[1]
            end_time_1 = time_ranges[2]
            commonDataRangeCorrector(hobo_data, correction_amt_1, "1900-05-17 00:00:00", end_time_1)
            print("bbc -1 correction_amt_1", correction_amt_1)
            
            start_time_2 = time_ranges[3]
            end_time_2 = time_ranges[4]

            if time_ranges[0] == "2":
                bbc_avg_value = round(((bbc_deep_df["SAL_FIELD"]).sum()/len(bbc_deep_df["SAL_FIELD"])), 4)
                correction_amt_3 = bbc_avg_value-hobo_data.loc[find_closest_hobo(hobo_data, end_time_1, 0), "Salinity Value (Offset +15)"]
                hobo_index_tracker = find_closest_hobo(hobo_data, end_time_1, 0)
                commonDataRangeCorrector(hobo_data, correction_amt_3, end_time_1, start_time_2)
                print("bbc -1 correction_amt_3", correction_amt_3)
            
            
            correction_amt_2 = bbc_deep_df.loc[bbc_indexc+1, "SAL_FIELD"]-hobo_data.loc[find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc+1, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), 0), "Salinity Value (Offset +15)"]
            commonDataRangeCorrector(hobo_data, correction_amt_2, start_time_2, end_time_2)
            hobo_index_tracker = find_closest_hobo(hobo_data,  (bbc_deep_df.loc[bbc_indexc+1, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), 0)
            print("bbc -1 correction_amt_2", correction_amt_2)
            
            '''
            if time_ranges[0] == "1":
                print ("should be working")
            elif time_ranges[0] != "2":
                print("you screwed up")
            '''
        
        
        
        if bbc_indexc != -1 and bbc_indexc != len(bbc_deep_df)-1:
            time_ranges = find_midpoint_range(bbc_deep_df, bbc_indexc)
            start_time_1 = time_ranges[1]
            end_time_1 = time_ranges[2]
            correction_amt_1 = bbc_deep_df.loc[bbc_indexc, "SAL_FIELD"]-hobo_data.loc[find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker), "Salinity Value (Offset +15)"]
            commonDataRangeCorrector(hobo_data, correction_amt_1, start_time_1, end_time_1)
            print("hobo_start_index", find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker))
            print("bbc in middle correction_amt_1", correction_amt_1)
            
            start_time_2 = time_ranges[3]
            end_time_2 = time_ranges[4]

            hobo_index_tracker = find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker)

            if time_ranges[0] == "2":
                bbc_avg_value = round(((bbc_deep_df["SAL_FIELD"].sum())/len(bbc_deep_df["SAL_FIELD"])), 4)
                correction_amt_3 = bbc_avg_value-hobo_data.loc[find_closest_hobo(hobo_data, end_time_1, hobo_index_tracker), "Salinity Value (Offset +15)"]
                commonDataRangeCorrector(hobo_data, correction_amt_3, end_time_1, start_time_2)

                hobo_index_tracker = find_closest_hobo(hobo_data, end_time_1, hobo_index_tracker)
                print("bbc in middle correction_amt_3", correction_amt_3)

            correction_amt_2 = bbc_deep_df.loc[bbc_indexc+1, "SAL_FIELD"]-hobo_data.loc[find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc+1, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker), "Salinity Value (Offset +15)"]
            commonDataRangeCorrector(hobo_data, correction_amt_2, start_time_2, end_time_2)
            
            hobo_index_tracker = find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc+1, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker)
            print("hobo end index", find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc+1, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker))
            print("bbc in middle correction_amt_2", correction_amt_2)
            
            if time_ranges[0] == "1":
                print ("should be working")
            elif time_ranges[0] != "2":
                print("you screwed up")
        
        if bbc_indexc == len(bbc_deep_df)-1:
            time_ranges = find_midpoint_range(bbc_deep_df, bbc_indexc)
            start_time_1 = time_ranges[1]
            end_time_1 = time_ranges[2]
            correction_amt_1 = bbc_deep_df.loc[bbc_indexc, "SAL_FIELD"]-hobo_data.loc[find_closest_hobo(hobo_data, (bbc_deep_df.loc[bbc_indexc, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker), "Salinity Value (Offset +15)"]
            hobo_index_tracker = find_closest_hobo(hobo_data,  (bbc_deep_df.loc[bbc_indexc, "Datetime_noyear"]).strftime('%Y-%m-%d %H:%M:%S'), hobo_index_tracker)

            commonDataRangeCorrector(hobo_data, correction_amt_1, start_time_1, end_time_1)
            print("bbc end correction_amt_1", correction_amt_1)

            bbc_avg_value = round((bbc_deep_df["SAL_FIELD"].sum())/len(bbc_deep_df["SAL_FIELD"]), 4)
            correction_amt_2 = bbc_avg_value-hobo_data.loc[find_closest_hobo(hobo_data, end_time_1, 0), "Salinity Value (Offset +15)"]
            
            commonDataRangeCorrector(hobo_data, correction_amt_2, end_time_1, "1900-12-31 23:59:59")
            print("bbc end correction_amt_2", correction_amt_2)

            print("hobo_value", hobo_data.loc[find_closest_hobo(hobo_data, end_time_1, 0), "Salinity Value (Offset +15)"])
            print("bbc_avg", bbc_avg_value)

        bbc_indexc += 1


    hobo_data["Sal_Value_Test_2"] = corrected_sal_value_list


    hobo_data.to_csv("HOBO_2023_From_2022_1_MSTL_Filtered_Data.csv", index=None)

# Test Run 1
hobo_2023_corrector("Used_Data\\Salinity\\HOBO_Used\\HOBO_#1_2022_MSTL_Filtered_Data.csv",
                    "Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv",
                    "Conductivity\\Sourced_Data\\Scallop_Bay_Marina\\Scallop_Bay_Marina_2023_Salinity.csv")