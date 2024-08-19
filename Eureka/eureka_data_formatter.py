# Date time column, index = 0
# Specific coonductivity column, index = 17
# Water temperature column, index = 15
# pH column, index = 16
# Depth column, index = 18
# Chloropyll column, index = 19
# DO column, index = 20

import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


def eureka_grapher(file):

    numofLinesS = 0
    raw_datetime_list = []
    battery_list = []
    air_temp_list = []
    rel_humidity_list = []
    rel_bar_pressure_list = []
    wind_speed_list = []
    max_wind_speed_list = []
    wind_direction_list = []
    wet_bulb_temperature_list = []
    precip_type_list = []
    rain_intensity_list = []
    total_rain_list = []
    interval_rain_list = []
    solar_rad_list = []
    heading_list = []
    water_temp_list = []
    ph_list = []
    cond_list = []
    depth_list = []
    chlorophyll_list = []
    do_list = []
    do_sat_list = []
    ph_mv_list = []
    internal_bat_list = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, file),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:

            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[0] == "" and not row[15] == "" and not row[16] == "" and not row[17] == "" and not row[18] == "" and not row[19] == "" and not row[20] == "" and numofLinesS > 3:
                raw_datetime_list.append(row[0])
                battery_list.append(float(row[1]))
                air_temp_list.append(float(row[2]))
                rel_humidity_list.append(float(row[3]))
                rel_bar_pressure_list.append(float(row[4]))
                wind_speed_list.append(float(row[5]))
                max_wind_speed_list.append(float(row[6]))
                wind_direction_list.append(float(row[7]))
                wet_bulb_temperature_list.append(float(row[8]))
                precip_type_list.append(float(row[9]))
                rain_intensity_list.append(float(row[10]))
                total_rain_list.append(float(row[11]))
                interval_rain_list.append(float(row[12]))
                solar_rad_list.append(float(row[13]))
                heading_list.append(float(row[14]))
                water_temp_list.append(float(row[15]))
                ph_list.append(float(row[16]))
                cond_list.append(float(row[17]))
                depth_list.append(float(row[18]))
                chlorophyll_list.append(float(row[19]))
                do_list.append(float(row[20]))
                do_sat_list.append(float(row[21]))
                ph_mv_list.append(float(row[22]))
                internal_bat_list.append(float(row[23]))
                

                numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1
    
    eureka_df = pd.DataFrame({"Time (America/New_York)": raw_datetime_list,
                              "Battery": battery_list,
                              "Air Temperature": air_temp_list,
                              "Relative Humidity": rel_humidity_list,
                              "Rel. Barometric Pressure": rel_bar_pressure_list,
                              "Wind Speed": wind_speed_list, 
                              "Max Wind Sp": max_wind_speed_list,
                              "Wind Direction": wind_direction_list,
                              "Wet Bulb Temperature": wet_bulb_temperature_list,
                              "Precip Type": precip_type_list,
                              "Rain Intensity": rain_intensity_list,
                              "Total Rain": total_rain_list,
                              "Interval Rain": interval_rain_list,
                              "Solar Rad": solar_rad_list,
                              "Heading": heading_list,
                              "Temperature": water_temp_list, 
                              "pH": ph_list, 
                              "Sp Cond": cond_list, 
                              "Depth": depth_list, 
                              "Chlorophyll": chlorophyll_list, 
                              "DO": do_list,
                              "DOSat": do_sat_list,
                              "pH mV": ph_mv_list,
                              "Internal Bat": internal_bat_list,})


