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
# use concat to merge row to row in bottle name df

# if cannot find merging parameter, make row of new dataframe null
# df.loc[len(df)] = pd.Series(dtype='float64')

# new_row = df.loc[1].copy()
# new_df = new_df._append(new_row)

# condition = df[parameters].index
# if conditions do not fit, delete line using df.drop(condition, inplace = True)

# Deciphers station from label
def stationDecoder(label_name):
   label_split = label_name.split("-")
   return label_split[0]


# Decodes bottle label
# Bottom or surface or middle sample
def labelDecoder(label_name):
   label_split = label_name.split("-")
   # print(label_split)
   depth_code = label_split[1]
   # print(depth_code)
   if depth_code[0] == "d":
      depth_translated = "bottom"
   elif depth_code[0] == "m":
      depth_translated = "middle"
   elif depth_code[0] == "s":
      depth_translated = "surface"
   # print(depth_translated)
   return depth_translated
print(labelDecoder("NO7-m2"))
def MWRAlabelDecoder(depth_code):
   label_translated = ""
   if depth_code == "A":
      label_translated = "surface"
   elif depth_code == "C":
      label_translated = "middle"
   elif depth_code == "E":
      label_translated = "bottom"
   elif label_translated == "":
      label_translated = "not it"
   return label_translated

def MWRAdateConverter(datetime):
   date = (datetime.split(" "))[0]
   return date

def dateConverter(date):
   m1, d1, y1 = [int(date) for date in date.split("/")]
   if len(str(y1)) == 2:
      y1 += 2000
   date_trunc = datetime.datetime(y1, m1, d1)
   return date_trunc

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

   rows_stored_df = pd.DataFrame()
   rows_stored_df = pd.DataFrame(data=rows_stored_df, columns=mwra_file_df.columns)
   print(rows_stored_df)

   print("Mwra date", dateConverter(MWRAdateConverter(mwra_file_df.loc[1, "PROF_DATE_TIME_LOCAL"])))
   print("bottle date", dateConverter(bottle_name_df.loc[0, "Sampling Date"]))

   for indexA in range(0, len(bottle_name_df)):
      #print("A:", indexA)
      for indexB in range(0, len(mwra_file_df)):
        # print("B:", indexB)
         # checks date

         if (dateConverter(MWRAdateConverter(mwra_file_df.loc[indexB, "PROF_DATE_TIME_LOCAL"])) == dateConverter(bottle_name_df.loc[indexA, "Sampling Date"])):
            print("yay the date works")

         if (dateConverter(MWRAdateConverter(mwra_file_df.loc[indexB, "PROF_DATE_TIME_LOCAL"])) == dateConverter(bottle_name_df.loc[indexA, "Sampling Date"])) and (mwra_file_df.loc[indexB, "STAT_ID"] == stationDecoder(bottle_name_df.loc[indexA, "Bottle Label"])) and (MWRAlabelDecoder(mwra_file_df.loc[indexB, "SAMPLE_DEPTH_CODE"]) == labelDecoder(bottle_name_df.loc[indexA, "Bottle Label"])):
            
            print("Mwra date", dateConverter(MWRAdateConverter(mwra_file_df.loc[indexB, "PROF_DATE_TIME_LOCAL"])))
            print("bottle date", dateConverter(bottle_name_df.loc[indexA, "Sampling Date"]))
         
            print("Mwra station", mwra_file_df.loc[indexB, "STAT_ID"])
            print("bottle station", stationDecoder(bottle_name_df.loc[indexA, "Bottle Label"]))

            print("mwra depth", MWRAlabelDecoder(mwra_file_df.loc[indexB, "ORDERED_DEPTH_CODE"]))
            print("bottle depth", labelDecoder(bottle_name_df.loc[indexA, "Bottle Label"]))
            
            
            new_row = mwra_file_df.loc[indexB].copy()
            rows_stored_df.loc[indexA] = new_row
            print("yay")
            break
   print(rows_stored_df)

   output_df = pd.concat([bottle_name_df, rows_stored_df], axis=1)
   '''
   if len(bottle_name_df) == len(rows_stored_df):
      print("maybe it works?")
   ''' 
   output_df.to_csv("mwra_filler_2022.csv")
   return output_df

MWRARetriever("base_table - Sheet1.csv", "MWRA_TA_DIC_2017_to_2022.csv")