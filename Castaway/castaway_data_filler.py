import pandas as pd
import glob
import os
import csv
import datetime
from decimal import Decimal

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

# Decodes bottle label
# Bottom or surface sample
def labelDecoder(label_name):
   label_split = label_name.split("-")
   print(label_split)
   depth_code = label_split[1]
   print(depth_code)
   if depth_code[0] == "d":
      depth_translated = "bottom"
   elif depth_code[0] == "s":
      depth_translated = "surface"
   print(depth_translated)
   return depth_translated

# Chooses appropriate castaway file and returns list with depth
def castawayFileChooser(date, label, collection_time):
   # Return list [depth]
   output_list = []

   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

   filename_list = []
   filetime_list = []
   filetime_conv_list = []
   for file in os.listdir("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data"):
      print("file in directory:", file)
      breakdown = file.split("_")
      print(breakdown)
      if date in breakdown:
            filename_list.append(file)
            print(file)
            filetime = file.split("_")[3]
            filetime = filetime.replace(".csv", "")

            if len(filetime) > 5:
               print('yay')
               filetime = filetime[:-3]

            print(filetime)
            filetime_list.append(filetime)
            print(filetime_list)
   
   # for filename in glob.glob(directory + str(date)):
      #filetime_list = []
      #print(filename)
      #filetime = filename.split("_")[3]
   
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
            for time in filetime_conv_list:
               difference_list = []
               difference = abs(float(collection_time_conv-time))         
               difference_list.append(difference)

            # Chooses file with minimum time difference
            min_time_diff = min(difference_list)
            print("min time diff", min_time_diff)
            min_time_diff_index = difference_list.index(min_time_diff)
            opt_time = filename_list[min_time_diff_index]

            # Opens file with minimum time difference

            print("opt_time", opt_time)
            with open(os.path.join("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data\\", opt_time)) as castaway_file:
               file = castaway_file.read()
               castaway_file_df = pd.read_csv(os.path.join("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data\\", opt_time), skiprows=28)

            print(castaway_file_df)

            if label == "bottom":
               # Obtains column with max depth
               max_depth = castaway_file_df["Depth (Meter)"].max()
               max_depth_index = castaway_file_df["Depth (Meter)"].idxmax()
               print("max depth", max_depth)
               #max_depth_index = castaway_file_df.query("`Depth (Meter)` == max_depth").index[0]
               print("max depth index", max_depth_index)
               # max_depth_temp = castaway_file_df.loc[max_depth_index, "Temperature (Celsius)"]
               # print("max depth temp", max_depth_temp)
               # max_depth_sal = castaway_file_df.loc[max_depth_index, "Salinity (Practical Salinity Scale)"]
               # print("max depth sal", max_depth_sal)
               output_list.append(max_depth-0.15)
               # output_list.append(max_depth_temp)
               # output_list.append(max_depth_sal)
            elif label == "surface":
               output_list.append(0.5)

   return(output_list)



def castawayRetriever (file_logger_input, start_date, end_date):

   # Makes start and end dates datetime objects to be used in date interval checker
   start_date_dt = datetime.datetime.strptime(start_date, '%m-%d-%Y')
   end_date_dt = datetime.datetime.strptime(end_date, '%m-%d-%Y')

   # Used to find location of specified file within Python code folder
   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

   logger_df = pd.read_csv(os.path.join(__location__, file_logger_input))
  
   dates = logger_df["Date"]
   
   logger_df_current = logger_df.loc[(logger_df["Date"] >= start_date) & (logger_df["Date"] <= end_date)]

   # creates new dataframe for only dates needed to be filled in
   
   # logger_df_current = logger_df.index.get_loc[(logger_df["Date"] >= start_date_dt) & (logger_df["Date"] =< end_date_dt)]

   current_index_list = logger_df_current.index.to_list()

   print(logger_df_current)
   print(current_index_list)
   # date interval checker
   # if date is in-between start and end interval, inputs values
   for index in current_index_list:
      date = logger_df.loc[index, "Date"]
      time = logger_df.loc[index, "TimeWaterCollection"]
      
      if not(pd.isnull(logger_df.loc[index, "Label_1"])):
         label1 = labelDecoder(logger_df.loc[index, "Label_1"])
         if pd.isnull(logger_df.loc[index, "Depth_1"]):
            date = date.replace("/", "-")
            print("new date", date)
            print(label1)
            print("list", castawayFileChooser(date, label1, time))
            if castawayFileChooser(date, label1, time) != []:
               logger_df.at[index, "Depth_1"] = round(castawayFileChooser(date, label1, time)[0], 3)
      
      if not(pd.isnull(logger_df.loc[index, "Label_2"])):
         label2 = labelDecoder(logger_df.loc[index, "Label_2"])
         if pd.isnull(logger_df.loc[index, "Depth_2"]):
            date = date.replace("/", "-")
            print("new date", date)
            print(label2)
            print("list", castawayFileChooser(date, label2, time))
            if castawayFileChooser(date, label2, time) != []:
               logger_df.at[index, "Depth_2"] = round(castawayFileChooser(date, label2, time)[0], 3)

      if not(pd.isnull(logger_df.loc[index, "Label_3"])):
         label3 = labelDecoder(logger_df.loc[index, "Label_3"])
         if pd.isnull(logger_df.loc[index, "Depth_3"]):
            date = date.replace("/", "-")
            print("new date", date)
            print(label3)
            print("list", castawayFileChooser(date, label3, time))
            if castawayFileChooser(date, label3, time) != []:
               logger_df.at[index, "Depth_1"] = round(castawayFileChooser(date, label3, time)[0], 3)

      if not(pd.isnull(logger_df.loc[index, "Label_4"])):
         label4 = labelDecoder(logger_df.loc[index, "Label_4"])
         print(label4)
         if pd.isnull(logger_df.loc[index, "Depth_4"]):
            date = date.replace("/", "-")
            print("new date", date)
            print(label4)
            print("list", castawayFileChooser(date, label4, time))
            if castawayFileChooser(date, label4, time) != []:
               logger_df.at[index, "Depth_4"] = round(castawayFileChooser(date, label4, time)[0], 3)
   print(logger_df)
   logger_df.to_csv("test_filler.csv")

   
   return logger_df
   
castawayRetriever("Field_LOG - Field_LOG.csv", "05-08-2021", "11-30-2022")
   