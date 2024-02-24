import pandas as pd
import glob
import os
import csv
from decimal import Decimal
import datetime

# how should this thing work
# Input: bast_table - Sheet1.csv, date parameter
# Output: Table with Sample #, Bottle Label, Sampling Date, Actual Depth, Salinity, Temperature, Date Processed (empty), Bottle Cleaned (empty), Observations (empty)
# how to do this
# dataframe with all appropriate columns is created
# set sample number equal to index number
# for each date in the logger that fits the date parameter
# inputs sampling date into "Sampling Date"

# Chooses appropriate castaway file and returns list with depth


def bottleTableFiller (file_logger_input, start_date, end_date):

   output_column_names = ["Bottle_Number", "Bottle_Label", "Sampling_Date", "Actual_Depth", "Salinity", "Temperature", "Date_Processed", "Bottle_Cleaned", "Observations"]
   output_df = pd.DataFrame(columns = output_column_names, dtype=str)

   print(output_df)

   # Makes start and end dates datetime objects to be used in date interval checker
   # start_date_dt = datetime.datetime.strptime(start_date, '%m-%d-%Y')
   # end_date_dt = datetime.datetime.strptime(end_date, '%m-%d-%Y')

   # Used to find location of specified file within Python code folder
   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

   logger_df = pd.read_csv(os.path.join(__location__, file_logger_input))
   #mwra_data_df = pd.read_csv(os.path.join(__location__, mwra_data))

   m2, d2, y2 = [int(date) for date in start_date.split("-")]
   date2 = datetime.datetime(y2, m2, d2)

   m3, d3, y3 = [int(date) for date in end_date.split("-")]
   date3 = datetime.datetime(y3, m3, d3)   

   valid_date_list = []
   valid_date_index_list = []
   logger_date_index = 0

   logger_dates_list = logger_df["Sampling Date"].tolist()
   for date in logger_dates_list:
      m1, d1, y1 = [int(date_part) for date_part in date.split("/")]

      if len(str(y1)) == 2:
         y1 += 2000

      date1 = datetime.datetime(y1, m1, d1)
      
      if ((date1 <= date3) & (date1>= date2)):
         valid_date_list.append(date)
         valid_date_index_list.append(logger_date_index)
      else:
         print("bruh is it working", date)
      logger_date_index += 1

   output_df["Sampling Date"] = valid_date_list
   output_index = 0

   output_df["Bottle_Label"] = output_df["Bottle_Label"].astype(str)


   for index in valid_date_index_list:
         output_df.at[output_index, "Bottle_Number"] = output_index + 1
         output_df.at[output_index, "Bottle_Label"] = logger_df.loc[index, "Bottle Label"]
         output_df.at[output_index, "Actual_Depth"] = logger_df.loc[index, "DEPTH (m)"]
         output_df.at[output_index, "Temperature"] = logger_df.loc[index, "TEMP (C)"]
         output_df.at[output_index, "Salinity"] = logger_df.loc[index, "SAL (PSU)"]
         output_index +=1
      
   output_df.to_csv("test_bottle_filler_mwra_2022.csv", index=False)
   return output_df
   
bottleTableFiller("mwra_filler_2022.csv", "05-07-2022", "12-10-2022")