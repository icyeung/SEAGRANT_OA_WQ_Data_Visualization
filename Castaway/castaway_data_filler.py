import pandas as pd
import glob
import os
import csv
from decimal import Decimal
import datetime

# how should this thing work
# you input field log file (has a set format)
# field log should be placed next to program for ease of access
# program looks through dates in water collection date column
# if date is between start and end date, then the following would apply
# on the current date in the field log, looks for castaway file with that same date
# if date is not possible, then will skip date entry in field log and print the date skipped
# if date is possible, then the appropriate depths will be recorded based on bottle label
# checks bottle string for depth indicator word
# bottom = deepest depth - 0.15m
# mid = middle depth measurement
# top = 0.15m
# shallow = middle depth measurement
# salinity and temperature measurements are recorded
# can be done by using column index
# use dataframe if possible
# program goes through table line by line
# hi

# Decodes bottle label
# Bottom or surface sample
def labelDecoder(label_name):
   label_split = label_name.split("-")
   depth_code = label_split[1]
   if depth_code[0] == "d":
      depth_translated = "bottom"
   elif depth_code[0] == "s":
      depth_translated = "surface"
   return depth_translated

# Chooses appropriate castaway file and returns list with depth
def castawayFileChooser(date, label, collection_time, special_case):
   output_list = []

   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
   folder = "Castaway_Data"

   repository_location = os.path.join(__location__, folder)


   print(__location__)

   filename_list = []
   filetime_list = []
   filetime_conv_list = []
   for file in os.listdir(repository_location):
      #print("file in directory:", file)
      breakdown = file.split("_")
      breakdown1 = breakdown[1]
      mf, df, yf = [int(datef) for datef in breakdown1.split("-")]
      datef = datetime.datetime(yf, mf, df)


      md, dd, yd = [int(ddate) for ddate in date.split("-")]
      conv_date = datetime.datetime(yd, md, dd)

      
      if conv_date == datef :
   
            filename_list.append(file)
            filetime = file.split("_")[3]
            filetime = filetime.replace(".csv", "")

            if len(filetime) > 5:
               print('yay')
               filetime = filetime[:-3]

            filetime_list.append(filetime)
   
            # File time is converted from hour.min to float
            filetime_hour = int(float(filetime))
            filetime_minute = Decimal(float(filetime))
            filetime_min_percent = round(filetime_minute/60, 4)
            filetime_conv = float(filetime_hour + filetime_min_percent)
            filetime_conv_list.append(filetime_conv)

            # Collection time is converted from hour:min to float
            collection_time_hour = int(collection_time.split(":")[0])
            collection_time_minute = int(collection_time.split(":")[1])
            collection_time_min_percent = round(collection_time_minute/60, 4)
            collection_time_conv = float(collection_time_hour + collection_time_min_percent)

            # Finds difference in collection time and time of file to look for which file to take info from
            difference_list = []
            for time in filetime_conv_list:   
               difference = abs(float(collection_time_conv-time))         
               difference_list.append(difference)

            # Chooses file with minimum time difference
            min_time_diff = min(difference_list)
            min_time_diff_index = difference_list.index(min_time_diff)
            opt_time = filename_list[min_time_diff_index]

            # Opens file with minimum time difference


            with open(os.path.join(repository_location, opt_time)) as castaway_file:
               file = castaway_file.read()
               castaway_file_df = pd.read_csv(os.path.join(repository_location, opt_time), skiprows=28)


            if label == "bottom":
               # Obtains column with max depth
               max_depth = castaway_file_df["Depth (Meter)"].max()
               max_depth_index = castaway_file_df["Depth (Meter)"].idxmax()
               output_list.append(max_depth-0.5)
            elif (label == "surface") and not(special_case):
               output_list.append(0.5)
            elif(label == "surface") and (special_case):
               output_list.append(1.5)

   return(output_list)

def castawayRetriever (file_logger_input, start_date, end_date):

   # Makes start and end dates datetime objects to be used in date interval checker
   # start_date_dt = datetime.datetime.strptime(start_date, '%m-%d-%Y')
   # end_date_dt = datetime.datetime.strptime(end_date, '%m-%d-%Y')

   # Used to find location of specified file within Python code folder
   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

   logger_df = pd.read_csv(os.path.join(__location__, file_logger_input))


   # how about this
   # we get list of date column
   # and then we keep track of index number while subscripting through it
   # for each date we go through,
   # the date is converted to datetime object and then comparted using the "yayyyyy" code above
   # if correct, the index number is added to "current" list
   # index += 1
      
   m2, d2, y2 = [int(date) for date in start_date.split("-")]
   date2 = datetime.datetime(y2, m2, d2)

   m3, d3, y3 = [int(date) for date in end_date.split("-")]
   date3 = datetime.datetime(y3, m3, d3)   

   valid_date_list = []
   valid_date_index_list = []
   logger_date_index = 0

   logger_dates_list = logger_df["Date"].tolist()
   for date in logger_dates_list:
      m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
      date1 = datetime.datetime(y1, m1, d1)
      
      if ((date1 <= date3) & (date1>= date2)):
         valid_date_list.append(date)
         valid_date_index_list.append(logger_date_index)
      else:
         print("bruh is it working", date)
      logger_date_index += 1


   # date interval checker
   # if date is in-between start and end interval, inputs values
   # if location is Pocasset, inputs depth as 1.5m
   print("index list", valid_date_index_list)
   for index in valid_date_index_list:
      print ("current index", index)
      date = logger_df.loc[index, "Date"]
      time = logger_df.loc[index, "TimeWaterCollection"]
      if logger_df.loc[index, "LocationName"] == "Pocasset":
         station_case = True
      else:
         station_case = False

      
      if not(pd.isnull(logger_df.loc[index, "Label_1"])):
         label1 = labelDecoder(logger_df.loc[index, "Label_1"])
         if pd.isnull(logger_df.loc[index, "Depth_1"]):
            date = date.replace("/", "-")
            if castawayFileChooser(date, label1, time, station_case) != []:
               logger_df.at[index, "Depth_1"] = round(castawayFileChooser(date, label1, time, station_case)[0], 3)
      
      if not(pd.isnull(logger_df.loc[index, "Label_2"])):
         label2 = labelDecoder(logger_df.loc[index, "Label_2"])
         if pd.isnull(logger_df.loc[index, "Depth_2"]):
            date = date.replace("/", "-")
            if castawayFileChooser(date, label2, time, station_case) != []:
               logger_df.at[index, "Depth_2"] = round(castawayFileChooser(date, label2, time, station_case)[0], 3)

      if not(pd.isnull(logger_df.loc[index, "Label_3"])):
         label3 = labelDecoder(logger_df.loc[index, "Label_3"])
         if pd.isnull(logger_df.loc[index, "Depth_3"]):
            date = date.replace("/", "-")
            if castawayFileChooser(date, label3, time, station_case) != []:
               logger_df.at[index, "Depth_3"] = round(castawayFileChooser(date, label3, time, station_case)[0], 3)

      if not(pd.isnull(logger_df.loc[index, "Label_4"])):
         label4 = labelDecoder(logger_df.loc[index, "Label_4"])
         if pd.isnull(logger_df.loc[index, "Depth_4"]):
            date = date.replace("/", "-")
            if castawayFileChooser(date, label4, time, station_case) != []:
               logger_df.at[index, "Depth_4"] = round(castawayFileChooser(date, label4, time, station_case)[0], 3)

   logger_df.to_csv("test_filler.csv")
   return logger_df
   
castawayRetriever("Field_LOG - Field_LOG.csv", "05-07-2021", "12-01-2022")
   