import pandas as pd
import glob
import os
import csv
from decimal import Decimal
import datetime

# Input: base table with bottle labels & dates
# Output: Table with each row being a bottle from the base table

# for name in file list, keep track of index for name
# use index to retrieve the date_table
# need name decoder to break down by -
# keeps the first part as station
# second part will be the location of sample
# need to map the location name to the depth letter
# surface = A
# middle = C
# bottom = E
# break down "PROF_DATE_TIME_LOCAL" into date and time
# use date to check
# check conditions of "STAT_ID" == station name, "ORDERED_DEPTH_CODE" == depth letter, and break_down("PROF_DATE_TIME_LOCAL") == date_table
# condition = df[parameters].index
# if conditions do not fit, delete line using df.drop(condition, inplace = True)


# Decodes bottle label
# Bottom or surface sample
def labelDecoder(label_name):
   label_split = label_name.split("-")
   # print(label_split)
   depth_code = label_split[1]
   # print(depth_code)
   if depth_code[0] == "d":
      depth_translated = "bottom"
   if depth_code[0] == "m":
      depth_translated = "middle"
   elif depth_code[0] == "s":
      depth_translated = "surface"
   # print(depth_translated)
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
      #print("file in directory:", file)
      breakdown = file.split("_")
      breakdown1 = breakdown[1]
      mf, df, yf = [int(datef) for datef in breakdown1.split("-")]
      datef = datetime.datetime(yf, mf, df)
      #print(date)

      md, dd, yd = [int(ddate) for ddate in date.split("-")]
      print(md, dd, yd)
      conv_date = datetime.datetime(yd, md, dd)

      #print("breakdown", breakdown)
      print("equal?", conv_date, datef)
      if conv_date == datef :
   
            filename_list.append(file)
            print(filename_list)
            print("hell yeah")
            filetime = file.split("_")[3]
            filetime = filetime.replace(".csv", "")

            if len(filetime) > 5:
               print('yay')
               filetime = filetime[:-3]

            print(filetime)
            filetime_list.append(filetime)
            print(filetime_list)

   
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
            # print("min time diff", min_time_diff)
            min_time_diff_index = difference_list.index(min_time_diff)
            opt_time = filename_list[min_time_diff_index]

            # Opens file with minimum time difference

            # print("opt_time", opt_time)
            with open(os.path.join("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data\\", opt_time)) as castaway_file:
               file = castaway_file.read()
               castaway_file_df = pd.read_csv(os.path.join("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data\\", opt_time), skiprows=28)

            # print(castaway_file_df)

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
               output_list.append(max_depth-0.5)
               # output_list.append(max_depth_temp)
               # output_list.append(max_depth_sal)
            if label == "middle":
               print("get depth from MWRA Data")
            elif label == "surface":
               output_list.append(0.5)

   return(output_list)



def MWRARetriever (bottle_inventory_input, mwra_data):

   # Makes start and end dates datetime objects to be used in date interval checker
   # start_date_dt = datetime.datetime.strptime(start_date, '%m-%d-%Y')
   # end_date_dt = datetime.datetime.strptime(end_date, '%m-%d-%Y')

   # Used to find location of specified file within Python code folder
   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
   folder = "MWRA_Data"

   data_location = os.path.join(__location__, folder)

   bottle_name_df = pd.read_csv(os.path.join(__location__, bottle_inventory_input))

   mwra_file_df = pd.read_csv(os.path.join(data_location, mwra_data))
  
   bottle_list_index = 0
   bottle_name_list = bottle_name_df["Bottle Label"].tolist()
   bottle_date_list = bottle_name_df["Sampling Date"].tolist()

   for name in bottle_name_list:
      label = labelDecoder(name)
      logger_date_index += 1

   
   # print(logger_df["Date"])


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
      # print(logger_date_index)
      # print("current date", date)
      m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
      date1 = datetime.datetime(y1, m1, d1)
      
      if ((date1 <= date3) & (date1>= date2)):
         # print("yayyyyyyyy")
         valid_date_list.append(date)
         valid_date_index_list.append(logger_date_index)
      else:
         print("bruh is it working", date)
      logger_date_index += 1
   
   # print("list of indices", valid_date_index_list)



   # print(logger_df_current)
   # print(current_index_list)
   # date interval checker
   # if date is in-between start and end interval, inputs values
   
   #print(logger_df)
   logger_df.to_csv("test_filler.csv")
   return logger_df
   
MWRARetriever("base_table - Sheet1.csv", "01-07-2021", "12-10-2022")