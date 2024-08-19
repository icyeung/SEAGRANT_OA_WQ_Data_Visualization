import pandas as pd

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