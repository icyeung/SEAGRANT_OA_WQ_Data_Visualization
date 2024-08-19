import pandas as pd

# Files you would like to concat together
# Make sure files are listed in the sequential order you would like them to be saved as in the concatted file
file1 = pd.read_csv("C:\\Users\\isabe\Desktop\\File Data\\pCO2SAMI Data Export_20210802")
file2 = pd.read_csv("C:\\Users\\isabe\Desktop\\File Data\\pCO2SAMI Data Export_20210928")
file3 = pd.read_csv("C:\\Users\\isabe\Desktop\\File Data\\pCO2SAMI Data Export_20211210")

# Concat command
new_file = pd.concat([file1,file2,file3])

# Saves the concatted file as a csv under desired name
new_file.to_csv("File Name", index=False, header=True)
