# Program is used to determine tide times for subordinate stations from harmonic stations
# file_name = name of harmonic tide file
# harmonic_location = harmonic station folder
# harmonic_station = name of harmonic station used for conversion
# subordinate_station = name of desired tide station from harmonic
# save_location = folder name of subordinate tide

# To use the program, navigate to the end, and follow instructions there.

import pandas as pd
import os
from datetime import datetime as dt
import datetime
import csv
import numpy as np


def tide_subordinate_time_adjustor(file_name, harmonic_location, subordinate_station, save_location, file_save_name):
    
    # Obtains location of Tide_Data main folder
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    # Location finders for harmonic data location
    harmonic_data_folder = os.path.join(__location__, 'NOAA_Tide_Harmonic_Data\\')
    harmonic_data_location_folder = os.path.join(harmonic_data_folder, harmonic_location)

    # Location finders for subordinate save location
    subordinate_data_folder = os.path.join(__location__, 'NOAA_Tide_Subordinate_Data\\')
    subordinate_data_location_folder = os.path.join(subordinate_data_folder, save_location)

    # Opens harmonic data as dataframe
    harmonic_data = pd.read_csv(os.path.join(harmonic_data_location_folder, file_name))


    # Converts from AM/PM time to 24-hr time in harmonic data
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

    # Runs AM/PM to 24-hr converter for all times in harmonic data file
    NOAA_tidal_data_time_converted_list = []
    for time in harmonic_data["Time"]:
        NOAA_tidal_data_time_converted_list.append(timeConverterto24(time))

    # Converts date format to MM/DD/YYYY for all dates in harmonic data file
    NOAA_tidal_data_date_converted_list = []
    for date in harmonic_data["Date"]:
        NOAA_tidal_data_date_converted_list.append(dt.strptime(date, "%m/%d/%Y"))

    # Combines time and date together to be saved in one column: "DateTime (UTC)"
    NOAA_tidal_data_datetime_combined_list = []
    for index in range(0, len(NOAA_tidal_data_date_converted_list)):
        NOAA_tidal_data_datetime_combined_list.append(dt.combine(NOAA_tidal_data_date_converted_list[index], NOAA_tidal_data_time_converted_list[index].time()))

    harmonic_data["DateTime (UTC)"] = NOAA_tidal_data_datetime_combined_list

    '''
    # Creates new column too hold adjusted times for subordinate data
    harmonic_data["Subordinate DateTime (Adjusted)"] = np.nan

    # Goes through all of the harmonic data, and depending on which subordinate station is desired,
    # the highs/lows are adjusted by certain amounts and saved under a new column: "Subordinate DateTime (Adjusted)".
    for index in range(0, len(harmonic_data)):
        
        tide_type = harmonic_data.loc[index, "High/Low"]
        
        if subordinate_station == "Herring River, MA":    
            if tide_type == "H":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 68)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
            if tide_type == "L":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 45)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
        
        if subordinate_station == "Pocasset River Entrance, MA":
            if tide_type == "H":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 9)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
            if tide_type == "L":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 6)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted

        if subordinate_station == "Fiddlers Cove, MA":
            if tide_type == "H":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 13)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
            if tide_type == "L":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 16)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted

        if subordinate_station == "Dead Neck, MA":
            if tide_type == "H":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 3)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
            if tide_type == "L":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 1)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted

        if subordinate_station == "Deer Island, MA":
            if tide_type == "H":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 1)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
            if tide_type == "L":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 0)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted

        if subordinate_station == "Dennis, MA":
            if tide_type == "H":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 17)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted
            if tide_type == "L":
                date = harmonic_data.loc[index, "DateTime (UTC)"]
                time_change = datetime.timedelta(minutes = 23)
                date_adjusted = date + time_change
                harmonic_data.loc[index, "Subordinate DateTime (Adjusted)"] = date_adjusted

        '''
    # Saves subordinate data file under desired save name
    harmonic_data.to_csv(os.path.join(subordinate_data_location_folder, file_save_name), index=None)


# To use the program, identify the harmonic data file name, harmonic data folder name, subordinate location name, subordinate location folder name, and save name for subordinate file.
# Write in a new line: tide_subordinate_time_adjustor(harmonic data file name, harmonic data folder name, subordinate location name, subordinate location folder name, subordinate file save name) 
# See below lines as examples.
# Each line will make the program run once for that instance, so if you only want to run one line, please comment out all other lines to prevent overwriting existing data.


'''
# Herring River uses Boston
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2020_Boston_GMT.csv", "Boston_MA\\", "Herring River, MA", "Herring_River_MA", "NOAA_Tidal_HL_202o_HerringRiver_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2021_Boston_GMT.csv", "Boston_MA\\", "Herring River, MA", "Herring_River_MA", "NOAA_Tidal_HL_2021_HerringRiver_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2022_Boston_GMT.csv", "Boston_MA\\", "Herring River, MA", "Herring_River_MA", "NOAA_Tidal_HL_2022_HerringRiver_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2023_Boston_GMT.csv", "Boston_MA\\", "Herring River, MA", "Herring_River_MA", "NOAA_Tidal_HL_2023_HerringRiver_GMT.csv")

# Pocasset River Entrance uses Piney Point
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2022_PineyPoint_GMT.csv", "Piney_Point_MA\\", "Pocasset River Entrance, MA", "Pocasset_River_Entrance_MA", "NOAA_Tidal_HL_2022_PocassetRiverEntrance_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2023_PineyPoint_GMT.csv", "Piney_Point_MA\\", "Pocasset River Entrance, MA", "Pocasset_River_Entrance_MA", "NOAA_Tidal_HL_2023_PocassetRiverEntrance_GMT.csv")

# Fiddlers Cove uses Newport
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2021_Newport_GMT.csv", "Newport_RI\\", "Fiddlers Cove, MA", "Fiddlers_Cove_MA", "NOAA_Tidal_HL_2021_FiddlersCove_GMT.csv")

# Dead Neck uses Boston
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2020_Boston_GMT.csv", "Boston_MA\\", "Dead Neck, MA", "Dead_Neck_MA", "NOAA_Tidal_HL_2020_DeadNeck_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2021_Boston_GMT.csv", "Boston_MA\\", "Dead Neck, MA", "Dead_Neck_MA", "NOAA_Tidal_HL_2021_DeadNeck_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2022_Boston_GMT.csv", "Boston_MA\\", "Dead Neck, MA", "Dead_Neck_MA", "NOAA_Tidal_HL_2022_DeadNeck_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2023_Boston_GMT.csv", "Boston_MA\\", "Dead Neck, MA", "Dead_Neck_MA", "NOAA_Tidal_HL_2023_DeadNeck_GMT.csv")

# Deer Island uses Boston
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2018_Boston_GMT.csv", "Boston_MA\\", "Deer Island, MA", "Deer_Island_MA", "NOAA_Tidal_HL_2018_DeerIsland_GMT.csv")
tide_subordinate_time_adjustor("NOAA_Tidal_HL_2019_Boston_GMT.csv", "Boston_MA\\", "Deer Island, MA", "Deer_Island_MA", "NOAA_Tidal_HL_2019_DeerIsland_GMT.csv")
'''

# Dennis uses Boston
#tide_subordinate_time_adjustor("NOAA_Tidal_HL_2019_Boston_GMT.csv", "Boston_MA\\", "Dennis, MA", "Dennis_MA", "NOAA_Tidal_HL_2019_Dennis_GMT.csv")

# Dead Neck uses Boston
tide_subordinate_time_adjustor("NOAA_Tidal_1MIN_May-Dec_2022_Boston_GMT.csv", "Boston_MA\\", "Dead Neck, MA", "Dead_Neck_MA", "NOAA_Tidal_1MIN_May-Dec_2022_DeadNeck_GMT.csv")

