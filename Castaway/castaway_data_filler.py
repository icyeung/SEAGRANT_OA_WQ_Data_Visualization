import pandas as pd

import os
import csv

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

def castawayRetriever (file_logger_input, start_date, end_date):
    # Used to find location of specified file within Python code folder
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


    # Used in taking out empty values from salinity data
    numofLinesS = -1

    # Takes out empty values in salinity data set
    with open(os.path.join(__location__, 'Salinity_Carolina_12-10-21.csv'),'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
      
            # Checks if time entry has corresponding Time and Verified Measurement
            # If not, does not include data point in graph
            if not row[0] == "-" and not row[1] == "-" and not row[2] == "-" and not row[0] == "" and not row[1] == "" and not row[2] == "" and numofLinesS > 0:
                salDate.append(row[0])
                print(row[0])
                condData.append(float(row[1]))
                condTempData.append(float(row[2]))
                numofLinesS += 1
            elif numofLinesS <= 0:
                numofLinesS += 1