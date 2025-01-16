import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as md
import datetime

# Input: Tidal Data, 1.2 Region of conductivity data
# Need to look for dates of nearest time and day comparisons of low tide and high tide daily
# Checks if times are same, if so, concats tidal time and day and conductivity value for nearest fitting time to list
# Plots list as dot plot

# For NOAA data, need to convert the time from 12H to 24H using self-created program
# Break up time string using .split(" ")[-1]
# If that string says "PM", add 12 hours to the hours
# If that string says "AM", and the hour is 12, change the hour to 0
# Piece string back together and convert string to datetime object using dt.strptime(sting, "%H:%M:%S")

# Convert date to datetime object using dt.strptime(string, "%m-%d-%Y")
# Combine date and time datetime objects using dt.combine(date, time)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# HOBO #1 2022 (Pocasset)
hobo_data = pd.read_csv(os.path.join(__location__, "HOBO_Data\\Conductivity_Data_No_Outliers\\Salinity_Carolina_Pocasset_12-9-22_1_NO_offset.csv"))

# Pocasset River Entrance 2023
NOAA_tidal_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Tide_Data\\NOAA_Tide_Subordinate_Data\\Pocasset_River_Entrance_MA\\NOAA_Tidal_HL_2023_PocassetRiverEntrance_GMT.csv"))

#BBC PR1 2023
BBC_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Conductivity\\Sourced_Data\\Buzzards_Bay_Coalition_Data\\bbcdata1992to2023-ver23May2024-export_FC_PR.csv"))

#Wunderground Weather 2023- POCAS16
weather_data_1 = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Conductivity\\Sourced_Data\\Wunderground_Weather_Data\\KMAPOCAS16.csv"))

#Wunderground Weather 2023- POCAS25
weather_data_2 = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Conductivity\\Sourced_Data\\Wunderground_Weather_Data\\KMAPOCAS25.csv"))

#Wunderground Weather 2023- POCAS30
weather_data_3 = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Conductivity\\Sourced_Data\\Wunderground_Weather_Data\\KMAPOCAS30.csv"))

#Wunderground Weather 2023- POCAS12
weather_data_4 = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Conductivity\\Sourced_Data\\Wunderground_Weather_Data\\KMAPOCAS12.csv"))

# Scallop Bay Marina 2023 (SBM)
sbm_data = pd.read_csv(os.path.join(os.path.realpath(os.getcwd()), "Conductivity\\Sourced_Data\\Scallop_Bay_Marina\\Scallop_Bay_Marina_2023_Salinity.csv"))


# Need to cut out section of NOAA_tidal_data that fits with date range of pco2_section_data
# Program where you input time period to get overlay instead of having a manual overlay? probably

# Cuts out data that do not fit within desired date range
# Input: dataframe, start date in "mm-dd-yyyy", end date in "mm-dd-yyyy"
# Output: dataframe with only data that is within the start and end date
def commonDataRange(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["Date"].tolist()
    for date in logger_dates_list:
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



def commonDataRange_bbc(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["SAMP_DATE"].tolist()
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


def commonDataRange_weather(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["Datetime_UTC"].tolist()
    for date in logger_dates_list:
        if date == np.nan:
            break
        else:
            date = str(date)
            date = date.split(" ")[0]
            print(date)
            y1, m1, d1 = [int(date_part) for date_part in date.split("-")]
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


def commonDataRange_weather_2(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["Date"].tolist()
    for date in logger_dates_list:
        if date == np.nan:
            break
        else:
            date = str(date)
            date = date.split(" ")[0]
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


def commonDataRange_sbm(data_df, start_date, end_date):
    m2, d2, y2 = [int(date) for date in start_date.split("-")]
    date2 = dt(y2, m2, d2)

    m3, d3, y3 = [int(date) for date in end_date.split("-")]
    date3 = dt(y3, m3, d3)   

    invalid_date_list = []
    invalid_date_index_list = []
    logger_date_index = 0

    logger_dates_list = data_df["Date"].tolist()
    for date in logger_dates_list:
        if date == np.nan:
            break
        else:
            date = str(date)
            date = date.split(" ")[0]
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



def timeConverterto24_nosec(time):
    ending = time.split(" ")[-1]
    time_number = time.split(" ")[0]
    h1, m1 = [int(number) for number in time_number.split(":")]
    if ending == "PM" and h1 != 12:
        h1 += 12
    if ending == "AM" and h1 == 12:
        h1 = 0
    converted_time = str(h1) + ":" + str(m1)
    return converted_time



def timeConverterto24(time):
    ending = time.split(" ")[-1]
    time_number = time.split(" ")[0]
    h1, m1, s1 = [int(number) for number in time_number.split(":")]
    if ending == "PM" and h1 != 12:
        h1 += 12
    if ending == "AM" and h1 == 12:
        h1 = 0
    converted_time = str(h1) + ":" + str(m1) + ":" + str(s1)
    converted_time_dt = dt.strptime(converted_time, "%H:%M:%S")
    return converted_time_dt


bbc_s_date_list = []
bbc_s_time_list = []
bbc_s_sal_list = []
bbc_s_samp_depth_list = []
bbc_s_total_depth_list = []


bbc_d_date_list = []
bbc_d_time_list = []
bbc_d_sal_list = []
bbc_d_samp_depth_list = []
bbc_d_total_depth_list = []

for bbc_index in range(0, len(BBC_data)):
    if BBC_data.loc[bbc_index, "STN_ID"] == "PR1":
        #print(BBC_data.loc[bbc_index, "SAMP_DATE"].split("/")[2])
        if BBC_data.loc[bbc_index, "SAMP_DATE"].split("/")[2] == "2023":
            print(BBC_data.loc[bbc_index, "UNIQUE_ID"].split("-")[-3])
            if BBC_data.loc[bbc_index, "UNIQUE_ID"].split("-")[-3] == "S":
                bbc_s_date_list.append(BBC_data.loc[bbc_index, "SAMP_DATE"])
                bbc_s_time_list.append(BBC_data.loc[bbc_index, "TIME"])
                bbc_s_sal_list.append(BBC_data.loc[bbc_index, "SAL_FIELD"])
                bbc_s_samp_depth_list.append(BBC_data.loc[bbc_index, "SAMPDEP_M"])
                bbc_s_total_depth_list.append(BBC_data.loc[bbc_index, "TOTDEP_M"])
            if BBC_data.loc[bbc_index, "UNIQUE_ID"].split("-")[-3] == "D":
                bbc_d_date_list.append(BBC_data.loc[bbc_index, "SAMP_DATE"])
                bbc_d_time_list.append(BBC_data.loc[bbc_index, "TIME"])
                bbc_d_sal_list.append(BBC_data.loc[bbc_index, "SAL_FIELD"])
                bbc_d_samp_depth_list.append(BBC_data.loc[bbc_index, "SAMPDEP_M"])
                bbc_d_total_depth_list.append(BBC_data.loc[bbc_index, "TOTDEP_M"])

bbc_s_24_time_list = []
for time in bbc_s_time_list:
    bbc_s_24_time_list.append(timeConverterto24_nosec(time))

bbc_d_24_time_list = []
for time in bbc_d_time_list:
    bbc_d_24_time_list.append(timeConverterto24_nosec(time))

bbc_s_datetime_utc_list = []
for bbc_indexa in range(0, len(bbc_s_24_time_list)):
    bbc_s_datetime_string = bbc_s_date_list[bbc_indexa] + " " + bbc_s_24_time_list[bbc_indexa]
    # Convert the combined string to a datetime object
    bbc_s_datetime_object = dt.strptime(bbc_s_datetime_string, "%m/%d/%Y %H:%M")
    if (bbc_s_datetime_object >= dt(2023,3,12,2,0)) & (bbc_s_datetime_object <= dt(2023,11,5,2,0)):
        bbc_d_datetime_utc = bbc_s_datetime_object + pd.Timedelta(hours=4)
    else:
        bbc_d_datetime_utc = bbc_s_datetime_object + pd.Timedelta(hours=5)
    bbc_s_datetime_utc_list.append(bbc_d_datetime_utc)
    

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



weather1_datetime_utc_list = []
for weather_index in range(0, len(weather_data_1)):
    weather1_datetime_str = weather_data_1.loc[weather_index, "Date"] + " " + timeConverterto24_nosec(weather_data_1.loc[weather_index, "Time"])
    weather1_datetime_obj = dt.strptime(weather1_datetime_str, "%Y/%m/%d %H:%M")
    if (weather1_datetime_obj >= dt(2023,3,12,2,0)) & (weather1_datetime_obj <= dt(2023,11,5,2,0)):
        weather1_datetime_utc = weather1_datetime_obj + pd.Timedelta(hours=4)
    else:
        weather1_datetime_utc = weather1_datetime_obj + pd.Timedelta(hours=5)
    weather1_datetime_utc_list.append(weather1_datetime_utc)
weather_data_1["Datetime_UTC"] = weather1_datetime_utc_list


weather2_datetime_utc_list = []
for weather_index in range(0, len(weather_data_2)):
    weather2_datetime_str = weather_data_2.loc[weather_index, "Date"] + " " + timeConverterto24_nosec(weather_data_2.loc[weather_index, "Time"])
    weather2_datetime_obj = dt.strptime(weather2_datetime_str, "%Y/%m/%d %H:%M")
    if (weather2_datetime_obj >= dt(2023,3,12,2,0)) & (weather2_datetime_obj <= dt(2023,11,5,2,0)):
        weather2_datetime_utc = weather2_datetime_obj + pd.Timedelta(hours=4)
    else:
        weather2_datetime_utc = weather2_datetime_obj + pd.Timedelta(hours=5)
    weather2_datetime_utc_list.append(weather2_datetime_utc)
weather_data_2["Datetime_UTC"] = weather2_datetime_utc_list


weather3_datetime_utc_list = []
for weather_index in range(0, len(weather_data_3)):
    weather3_datetime_str = weather_data_3.loc[weather_index, "Date"] + " " + timeConverterto24_nosec(weather_data_3.loc[weather_index, "Time"])
    weather3_datetime_obj = dt.strptime(weather3_datetime_str, "%Y/%m/%d %H:%M")
    if (weather3_datetime_obj >= dt(2023,3,12,2,0)) & (weather3_datetime_obj <= dt(2023,11,5,2,0)):
        weather3_datetime_utc = weather3_datetime_obj + pd.Timedelta(hours=4)
    else:
        weather3_datetime_utc = weather3_datetime_obj + pd.Timedelta(hours=5)
    weather3_datetime_utc_list.append(weather3_datetime_utc)
weather_data_3["Datetime_UTC"] = weather3_datetime_utc_list

weather_data_1_fitted = commonDataRange_weather(weather_data_1, "05-16-2023", "12-02-2023")
weather_data_2_fitted = commonDataRange_weather(weather_data_2, "05-16-2023", "12-02-2023")
weather_data_3_fitted = commonDataRange_weather(weather_data_3, "05-16-2023", "12-02-2023")
weather_data_4_fitted = commonDataRange_weather_2(weather_data_4, "05-16-2023", "12-02-2023")

sbm_data_fitted = commonDataRange_sbm(sbm_data, "01-01-2023", "12-31-2023")

NOAA_fitted_data = commonDataRange(NOAA_tidal_data, "05-16-2023", "12-02-2023")
#print(commonDataRange(NOAA_tidal_data, "05-16-2023", "11-01-2023"))

print("yay, time is done?")

NOAA_tidal_data_time_converted_list = []
for time in NOAA_fitted_data["Time"]:
    NOAA_tidal_data_time_converted_list.append(timeConverterto24(time))
#print("time", NOAA_tidal_data_time_converted_list)

NOAA_tidal_data_date_converted_list = []
for date in NOAA_fitted_data["Date"]:
    NOAA_tidal_data_date_converted_list.append(dt.strptime(date, "%m/%d/%Y"))
#print("date", NOAA_tidal_data_date_converted_list)


NOAA_tidal_data_datetime_combined_list = []
for index in range(0, len(NOAA_tidal_data_date_converted_list)):
    NOAA_tidal_data_datetime_combined_list.append(dt.combine(NOAA_tidal_data_date_converted_list[index], NOAA_tidal_data_time_converted_list[index].time()))

# Need to add NOAA_tidal_data_datetime_combined_list into NOAA dataframe as "DateTime"
NOAA_fitted_data["DateTime"] = NOAA_tidal_data_datetime_combined_list
#print(NOAA_fitted_data)
print("another part done?")

# pCO2 2022 data section is good
hobo_sal = hobo_data["Salinity Value (Offset +15)"]
hobo_date_with_year = hobo_data["Date (UTC)"]
hobo_date_no_year = []
for date in hobo_date_with_year:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(date, '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    dt_date_no_year_time_shift = dt_date_no_year - datetime.timedelta(hours=3)
    hobo_date_no_year.append(dt_date_no_year_time_shift)


# Need to decipher NOAA data
NOAA_date_with_year = NOAA_fitted_data["DateTime"]
NOAA_date_no_year = []
for date in NOAA_date_with_year:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_no_year.append(dt_date_no_year)


# Decipher NOAA high/low data
# If high, then puts in time to high_list
# If low, then puts in time to low_list
# High_list -> star points?
# Low_list -> triangle points?
    
NOAA_date_high = []
NOAA_date_low = []
NOAA_data_high = []
NOAA_data_low = []
for index in range(0, len(NOAA_date_with_year)):
    type = NOAA_fitted_data.loc[index, "High/Low"]
    if type == "H":
        NOAA_date_high.append(NOAA_fitted_data.loc[index, "DateTime"])
        NOAA_data_high.append(NOAA_fitted_data.loc[index, "Pred(cm)"])
    if type == "L":
        NOAA_date_low.append(NOAA_fitted_data.loc[index, "DateTime"])
        NOAA_data_low.append(NOAA_fitted_data.loc[index, "Pred(cm)"])


NOAA_date_high_revised = []
for date in NOAA_date_high:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_high_revised.append(dt_date_no_year)


NOAA_date_low_revised = []
for date in NOAA_date_low:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    NOAA_date_low_revised.append(dt_date_no_year)


bbc_s_datetime_noyear_list = []
for date in bbc_s_datetime_utc_list:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    bbc_s_datetime_noyear_list.append(dt_date_no_year)


bbc_d_datetime_noyear_list = []
for date in bbc_d_datetime_utc_list:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    bbc_d_datetime_noyear_list.append(dt_date_no_year)


weather1_datetime_noyear_list = []
for date in weather_data_1_fitted["Datetime_UTC"]:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    weather1_datetime_noyear_list.append(dt_date_no_year)


weather2_datetime_noyear_list = []
for date in weather_data_2_fitted["Datetime_UTC"]:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    weather2_datetime_noyear_list.append(dt_date_no_year)


weather3_datetime_noyear_list = []
for date in weather_data_3_fitted["Datetime_UTC"]:
    date_no_year = '{:%m-%d %H:%M:%S}'.format(dt.strptime(str(date), '%Y-%m-%d %H:%M:%S'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d %H:%M:%S")
    weather3_datetime_noyear_list.append(dt_date_no_year)

weather4_datetime_noyear_list = []
for date in weather_data_4_fitted["Date"]:
    date_no_year = '{:%m-%d}'.format(dt.strptime(str(date), '%m/%d/%Y'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d")
    weather4_datetime_noyear_list.append(dt_date_no_year)

sbm_datetime_noyear_list = []
for date in sbm_data_fitted["Date"]:
    date_no_year = '{:%m-%d}'.format(dt.strptime(str(date), '%m/%d/%Y'))
    date_no_year = str(date_no_year)
    dt_date_no_year = dt.strptime(date_no_year, "%m-%d")
    sbm_datetime_noyear_list.append(dt_date_no_year)

#print(hobo_data)

print("bbc s date:", bbc_s_datetime_utc_list)
print("bbc s sal:", bbc_s_sal_list)
print("bbc d date:", bbc_d_datetime_utc_list)
print("bbc d sal:", bbc_d_sal_list)

measurement_converted = []
for measurement in weather_data_4_fitted["Precipition_Sum (in)"]:
    measurement_float = float(measurement[:-2])
    measurement_mm = measurement_float*25.4
    measurement_converted.append(measurement_mm)

weather_data_4_fitted["Precipitation_Sum (mm)"] = measurement_converted

print(weather_data_4_fitted)

bbc_d_sal_float_list=[]
for number in bbc_d_sal_list:
    if not(np.isnan(number)):
        updated_num = float(number)
        bbc_d_sal_float_list.append(updated_num)

print(sum(bbc_d_sal_float_list))
print("bbc deep avg sal", round((sum(bbc_d_sal_float_list)/len(bbc_d_sal_float_list)), 4))

bbc_d_avg_list = []
i=0
while i < len(hobo_date_no_year):
    bbc_d_avg_list.append(round((sum(bbc_d_sal_float_list)/len(bbc_d_sal_float_list)), 4))
    i+=1

fig, ax1 = plt.subplots(figsize=(14,7))
p1 = ax1.plot(hobo_date_no_year, hobo_sal, color = "b", linestyle = 'solid', label = 'HOBO #1 2022 (+15 PSU)', linewidth=0.75)
#p2 = ax1.plot(bbc_s_datetime_noyear_list, bbc_s_sal_list, color = "r", linestyle = 'solid', label = 'BBC PR1 2023 Surface', linewidth=0.75, marker = "o")
p3 = ax1.plot(bbc_d_datetime_noyear_list, bbc_d_sal_list, color = "g", linestyle = 'solid', label = 'BBC PR1 2023 Deep', linewidth=0.75, marker = "o")
p7 = ax1.plot(hobo_date_no_year, bbc_d_avg_list, color = "r", linestyle = 'dashed', label = 'BBC PR1 Deep Average Salinity', linewidth=0.75)
p6 = ax1.plot(sbm_datetime_noyear_list, sbm_data_fitted["Salinity (psu)"], color = "k", linestyle = 'solid', label = 'Scallop Bay Marina', linewidth=0.75, marker = "P")

# Sets x-axis as Dates

date_form = md.DateFormatter("%m-%d %H:%M")
ax1.xaxis.set_major_formatter(date_form)
ax1.set_xticks(sbm_datetime_noyear_list)
plt.xticks(rotation=90)
ax1.xaxis.set_major_locator(md.WeekdayLocator(interval = 2))     # Displays x-axis label every 14 days
#ax1.xaxis.set_minor_locator(md.HourLocator(interval = 1))       # Indicates each day (without label) on x-axis


    
# Sets axis labels and changes font color of "pco2" label for easy viewing
ax1.set_ylabel("Salinity (PSU)")
ax1.set_xlabel("Dates (MM-DD)")
ax1.yaxis.label.set_color("k")  
ax1.legend()

'''
# Graphs Tide Data
ax3 = ax1.twinx()
p4a = ax3.scatter(NOAA_date_high_revised, NOAA_data_high, color = 'purple', marker = "*", label = 'Pocasset River Entrance- 2023 High Tide')
p4b = ax3.scatter(NOAA_date_low_revised, NOAA_data_low, color = 'brown', marker = "^", label = 'Pocasset River Entrance- 2023 Low Tide')
ax3.set_ylabel("Tide Height (cm)")
'''


# Graphs precipitation
#ax4 = ax1.twinx()
#p5b = ax4.plot(weather2_datetime_noyear_list, weather_data_2_fitted["Precip_Rate_mm"], color = 'magenta', marker = '.', label = "Precipitation: Station 25")
#p5a = ax4.plot(weather1_datetime_noyear_list, weather_data_1_fitted["Precip_Rate_mm"], color = 'cyan', marker = '.', label = "Precipitation: Station 16")
#p5c = ax4.plot(weather3_datetime_noyear_list, weather_data_3_fitted["Precip_Rate_mm"], color = 'orange', marker = '.', label = "Precipitation: Station 30")
#p5d = ax4.plot(weather4_datetime_noyear_list, measurement_converted, color = 'purple', marker = '.', label = "Precipitation: Station 12")
#ax4.set_ylabel("Precipitation (mm)")


# Sets title, adds a grid, and shows legend
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.title("HOBO #1 2022 (-3 Hours) (proxy for 2023) vs BBC 2023 PR1 vs Scallop Bay Marina", loc='center')
plt.grid(True)
plt.legend()

my_path = os.path.dirname(os.path.abspath(__file__))

# Saves without outliers graph to specified name in folder
plt.savefig(my_path + '\\Conductivity_Graphs\\Comparison_Graphs\\hobo_1_2022_vs_2023_bbc_vs_sbm_v2.png')

plt.show()