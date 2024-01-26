import pandas as pd

import os
import csv
import datetime

'''
# semi-automated loop to merge files specified by used into one csv file
def main():
    
   # user specifies name of file (if in same folder as program) or file path
   # new data file will be saved there
   writingFileName = input("What file do you want to write to? ")
   mergedFile = open(writingFileName,"a")
   
   # used to hold all data files to be merged
   dataFiles = []
   
   # loop adds files to holder list dataFiles
   while True:
      answer = input("Do you have another file to compile? (y/n) ")
      if answer == "y":
         readFileName = input("What is the path of the file? ")
         try:
            dataFiles.append(pd.read_csv(readFileName))
         except:
            print("Error. Please input a correct file name.")
      else:
         break
   
   # merges files into new data file     
   mergedFile = pd.concat(dataFiles)
   
   # converts new data file to csv format
   # does not include index as a column
   mergedFile.to_csv(writingFileName, index=False, header=True)
     
main()
'''

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

def labelDecoder(label_name):
   label_split = label_name.split("-")
   depth_code = label_split[1]
   if depth_code.charAt(0) == "d":
      depth_translated = "bottom"
   elif depth_code.charAt(0) == "s":
      depth_translated = "surface"
   return depth_translated

def castawayRetriever (file_logger_input, start_date, end_date):

   start_date_dt = datetime.datetime.strptime(start_date, '%b %d %Y %I:%M%p')
   end_date_dt = datetime.datetime.strptime(end_date, '%b %d %Y %I:%M%p')

   # Used to find location of specified file within Python code folder
   __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

   logger_df = pd.read_csv(os.path.join(__location__, file_logger_input))
  
   dates = logger_df["Date"]

   for date in dates:
      date = datetime.datetime.strptime(date, '%b %d %Y %I:%M%p')
      if start_date_dt <= date <= end_date_dt:
         print("Yes, in between")
      else:
         print("No, not in between")

      print(logger_df.loc[date])
      if logger_df.loc[date, "Depth_1"] == "":
         label1 = logger_df.loc[date, "Label_1"]
         print(label1)
         if labelDecoder(label1) == "bottom":
            time1 = logger_df.loc[date, ""]


   print(logger_df)

# issue: dates repeat, so cannot really identify solely based on that
#- could use index
#- could use some sort of and? from dataframe