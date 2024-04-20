import pandas as pd
import glob
import os
import csv
from decimal import Decimal
import datetime

# how should this thing work
# Input: Castaway Files, Field log, date parameter
# Output: Table with Sample #, Bottle Label, Sampling Date, Actual Depth, Salinity, Temperature, Date Processed (empty), Bottle Cleaned (empty), Observations (empty)
# how to do this
# dataframe with all appropriate columns is created
# set sample number equal to index number
# for each date in the logger that fits the date parameter
# inputs sampling date into "Sampling Date"

output_column_names = ["Bottle_Number", "Bottle_Label", "Sampling_Date", "Sampling_Time_LST", "Actual_Depth", "Salinity", "Temperature", "Date_Processed", "Bottle_Cleaned", "Observations"]
output_df = pd.DataFrame(columns = output_column_names)

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
   # Return list [depth]
   output_list = []

   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

   filename_list = []
   filetime_list = []
   filetime_conv_list = []
   used_files = []
   for file in os.listdir("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data"):
      breakdown = file.split("_")
      breakdown1 = breakdown[1]
      mf, df, yf = [int(datef) for datef in breakdown1.split("-")]
      datef = datetime.datetime(yf, mf, df)
  

      md, dd, yd = [int(ddate) for ddate in date.split("-")]
      conv_date = datetime.datetime(yd, md, dd)


      if conv_date == datef :
   
            output_list = []

            filename_list.append(file)
            filetime = file.split("_")[3]
            filetime = filetime.replace(".csv", "")

            if len(filetime) > 5:
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
            for time in filetime_conv_list:
               difference_list = []
               difference = abs(float(collection_time_conv-time))         
               difference_list.append(difference)

            # Chooses file with minimum time difference
            min_time_diff = min(difference_list)
            min_time_diff_index = difference_list.index(min_time_diff)
            opt_time_file = filename_list[min_time_diff_index]
            used_files.append(opt_time_file)
            # Opens file with minimum time difference


            with open(os.path.join("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data\\", opt_time_file)) as castaway_file:
               file = castaway_file.read()
               castaway_file_df = pd.read_csv(os.path.join("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Castaway\\Castaway_Data\\", opt_time_file), skiprows=28)


            if label == "bottom":
               # Obtains column with max depth
               max_depth = castaway_file_df["Depth (Meter)"].max()
               max_depth_index = castaway_file_df["Depth (Meter)"].idxmax()
               max_depth_temp = castaway_file_df.loc[max_depth_index, "Temperature (Celsius)"]
               max_depth_sal = castaway_file_df.loc[max_depth_index, "Salinity (Practical Salinity Scale)"]
               output_list.append(max_depth-0.5)
               output_list.append(max_depth_temp)
               output_list.append(max_depth_sal)

            
            elif (label == "surface") and not(special_case):
               output_list.append(0.5)
               surface_depth = 0.5
               castaway_depths_list = castaway_file_df["Depth (Meter)"]
               minimum_depth_diff_list = []
               for depth in castaway_depths_list:
                  difference_depth = abs(surface_depth-depth)
                  minimum_depth_diff_list.append(difference_depth)
               ideal_depth_index = minimum_depth_diff_list.index(min(minimum_depth_diff_list))
               ideal_depth = castaway_file_df.loc[ideal_depth_index, "Depth (Meter)"]
               ideal_depth_temp = castaway_file_df.loc[ideal_depth_index, "Temperature (Celsius)"]
               ideal_depth_sal = castaway_file_df.loc[ideal_depth_index, "Salinity (Practical Salinity Scale)"]
               output_list.append(ideal_depth_temp)
               output_list.append(ideal_depth_sal)
            elif(label == "surface") and (special_case):
               output_list.append(1.5)
               surface_depth = 1.5
               castaway_depths_list = castaway_file_df["Depth (Meter)"]
               minimum_depth_diff_list = []
               for depth in castaway_depths_list:
                  difference_depth = abs(surface_depth-depth)
                  minimum_depth_diff_list.append(difference_depth)
               ideal_depth_index = minimum_depth_diff_list.index(min(minimum_depth_diff_list))
               ideal_depth = castaway_file_df.loc[ideal_depth_index, "Depth (Meter)"]
               ideal_depth_temp = castaway_file_df.loc[ideal_depth_index, "Temperature (Celsius)"]
               ideal_depth_sal = castaway_file_df.loc[ideal_depth_index, "Salinity (Practical Salinity Scale)"]
               output_list.append(ideal_depth_temp)
               output_list.append(ideal_depth_sal)

   return(output_list)



def bottleTableFiller (file_logger_input, start_date, end_date):

   output_column_names = ["Bottle_Number", "Bottle_Label", "Sampling_Date", "Sampling_Time_LST", "Actual_Depth", "Salinity", "Temperature", "Date_Processed", "Bottle_Cleaned", "Observations"]
   output_df = pd.DataFrame(columns = output_column_names)

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

   valid_date_time_list = []

   logger_dates_list = logger_df["Date"].tolist()
   for date in logger_dates_list:
      m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
      date1 = datetime.datetime(y1, m1, d1)
      
      if ((date1 <= date3) & (date1>= date2)):
         valid_date_list.append(date)
         valid_date_index_list.append(logger_date_index)
         valid_date_time_list.append(logger_df.loc[logger_date_index, "TimeWaterCollection"])
      else:
         print("bruh is it working", date)
      logger_date_index += 1


   output_df["Sampling_Date"] = valid_date_list
   output_df["Sampling_Time_LST"] = valid_date_time_list
   output_index = 0

   # date interval checker
   # if date is in-between start and end interval, inputs values
   for index in valid_date_index_list:
      date = logger_df.loc[index, "Date"]
      time = logger_df.loc[index, "TimeWaterCollection"]

      if logger_df.loc[index, "LocationName"] == "Pocasset":
         station_case = True
      else:
         station_case = False
      
      if not(pd.isnull(logger_df.loc[index, "Label_1"])):
         label1 = labelDecoder(logger_df.loc[index, "Label_1"])
         output_df.at[output_index, "Sampling_Date"] = date
         output_df.at[output_index, "Sampling_Time_LST"] = time
         output_df.at[output_index, "Bottle_Label"] = logger_df.loc[index, "Label_1"]
         output_df.at[output_index, "Bottle_Number"] = output_index+1
         date = date.replace("/", "-")
         if castawayFileChooser(date, label1, time, station_case) != []:
            output_df.at[output_index, "Actual_Depth"] = round(castawayFileChooser(date, label1, time, station_case)[0], 3)
         if len(castawayFileChooser(date, label1, time, station_case)) == 3:
            output_df.at[output_index, "Temperature"] = round(castawayFileChooser(date, label1, time, station_case)[1], 3)
            output_df.at[output_index, "Salinity"] = round(castawayFileChooser(date, label1, time, station_case)[2], 3)
         output_index += 1

      
      if not(pd.isnull(logger_df.loc[index, "Label_2"])):
         label2 = labelDecoder(logger_df.loc[index, "Label_2"])
         output_df.at[output_index, "Sampling_Date"] = date
         output_df.at[output_index, "Sampling_Time_LST"] = time
         output_df.at[output_index, "Bottle_Label"] = logger_df.loc[index, "Label_2"]
         output_df.at[output_index, "Bottle_Number"] = output_index+1
         date = date.replace("/", "-")
         if castawayFileChooser(date, label2, time, station_case) != []:
            output_df.at[output_index, "Actual_Depth"] = round(castawayFileChooser(date, label2, time, station_case)[0], 3)
         if len(castawayFileChooser(date, label2, time, station_case)) == 3:
            output_df.at[output_index, "Temperature"] = round(castawayFileChooser(date, label2, time, station_case)[1], 3)
            output_df.at[output_index, "Salinity"] = round(castawayFileChooser(date, label2, time, station_case)[2], 3)
         else:
            print("something broke")
            break
         output_index += 1

      if not(pd.isnull(logger_df.loc[index, "Label_3"])):
         label3 = labelDecoder(logger_df.loc[index, "Label_3"])
         output_df.at[output_index, "Sampling_Date"] = date
         output_df.at[output_index, "Sampling_Time_LST"] = time
         output_df.at[output_index, "Bottle_Label"] = logger_df.loc[index, "Label_3"]
         output_df.at[output_index, "Bottle_Number"] = output_index+1
         date = date.replace("/", "-")
         if castawayFileChooser(date, label3, time, station_case) != []:
            output_df.at[output_index, "Actual_Depth"] = round(castawayFileChooser(date, label3, time, station_case)[0], 3)
         if len(castawayFileChooser(date, label3, time, station_case)) == 3:
            output_df.at[output_index, "Temperature"] = round(castawayFileChooser(date, label3, time, station_case)[1], 3)
            output_df.at[output_index, "Salinity"] = round(castawayFileChooser(date, label3, time, station_case)[2], 3)
         else:
            print("something broke")
            break
         output_index += 1

      if not(pd.isnull(logger_df.loc[index, "Label_4"])):
         label4 = labelDecoder(logger_df.loc[index, "Label_4"])
         output_df.at[output_index, "Sampling_Date"] = date
         output_df.at[output_index, "Sampling_Time_LST"] = time
         output_df.at[output_index, "Bottle_Label"] = logger_df.loc[index, "Label_4"]
         output_df.at[output_index, "Bottle_Number"] = output_index+1
         date = date.replace("/", "-")
         if castawayFileChooser(date, label4, time, station_case) != []:
            output_df.at[output_index, "Actual_Depth"] = round(castawayFileChooser(date, label4, time, station_case)[0], 3)
         if len(castawayFileChooser(date, label4, time, station_case)) == 3:
            output_df.at[output_index, "Temperature"] = round(castawayFileChooser(date, label4, time, station_case)[1], 3)
            output_df.at[output_index, "Salinity"] = round(castawayFileChooser(date, label4, time, station_case)[2], 3)
         else:
            print("something broke")
            break
         output_index += 1
      
   output_df.to_csv("test_bottle_filler_castaway.csv", index=False)
   return logger_df
   
bottleTableFiller("Field_LOG - Field_LOG.csv", "01-01-2022", "12-10-2022")