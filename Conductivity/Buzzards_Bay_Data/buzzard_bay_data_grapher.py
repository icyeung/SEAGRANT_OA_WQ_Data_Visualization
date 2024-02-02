import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import datetime

# saves csv as dataframe
# sorts by station
# checks start date & end date
# if there is no valid start or end date, uses entire time frame
# 

def buzzard_bay_grapher(file, station, title, start_date, end_date):

    numofLinesS = 0
    date_list = []
    time_list = []
    temp_list = []
    salinity_list = []


    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, file),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
      
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[3] == "-" and not row[4] == "-" and not row[11] == "-" and not row[20] == "-" and not row[22] == "-" and not row[3] == "" and not row[4] == "" and not row[11] == "" and not row[20] == "" and not row[22] == "" and numofLinesS > 0:
                if row[3] == station:
                    date_list.append(row[4])
                    time_list.append(row[11])
                    temp_list.append(row[20])
                    salinity_list.append(row[22])
                    numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1
    
    for date in date_list:
        dateObj = datetime.datetime.strptime(date, '%m/%d/%y %H:%M:%S')
        