# Program is used to adjust Waquoit Bay Salinity times for comparison with Harwich
# NERRS station used for comparison is Metoxit Point; location = "Metoxit Point\\"

import pandas as pd
import os
from datetime import datetime as dt
import datetime

def NERRS_sal_grapher(file_name, location):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    raw_data_folder = os.path.join(__location__, 'Sourced_Data\\NERRS_Data\\Waquoit_Bay_Raw_Data\\')
    raw_data_location_folder = os.path.join(raw_data_folder, location)

    adjusted_data_folder = os.path.join(__location__, 'Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\')

    # Opens NERRS raw data file
    NERRS_data = pd.read_csv(os.path.join(raw_data_location_folder, file_name))


    # Converts string time stamps from EST to GMT/UTC + 1
    # 1 hour ahead of GMT/UTC to account for delay in tide of 1 hour for Harwich as compared to Waquoit Bay
    def NERRS_time_converter(date_time):
        
        date = date_time.split(" ")[0]
        time = date_time.split(" ")[1]
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
        date1 = dt(y1, m1, d1)
        converted_time = dt.strptime(time, "%H:%M")
        datetime_dt_est = dt.combine(date1, converted_time.time())

        datetime_dt_utc = datetime_dt_est + datetime.timedelta(hours=6)

        return datetime_dt_utc

    nerrs_datetime_list = []
    for value in NERRS_data["DateTimeStamp"]:
        nerrs_datetime_list.append(NERRS_time_converter(value))


    NERRS_data["Datetime_Adjusted_UTC+1"] = nerrs_datetime_list

    print(NERRS_data)


    # Updates data file name to reflect the time being adjusted
    file_name_base = file_name[:-4]
    file_name_adjusted = file_name_base + "_adjusted_UTC+1.csv"

    NERRS_data.to_csv(os.path.join(adjusted_data_folder ,file_name_adjusted))


# Metoxit Point 2020
NERRS_sal_grapher("wqbmpwq2020.csv", "Metoxit_Point\\")

# Metoxit Point 2021
NERRS_sal_grapher("wqbmpwq2021.csv", "Metoxit_Point\\")

# Metoxit Point 2022
NERRS_sal_grapher("wqbmpwq2022.csv", "Metoxit_Point\\")

# Metoxit Point 2023
NERRS_sal_grapher("wqbmpwq2023.csv", "Metoxit_Point\\")




