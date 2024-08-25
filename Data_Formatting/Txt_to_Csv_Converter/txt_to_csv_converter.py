# Converts folder of files from TXT to CSV

import pandas as pd
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
convert_from_folder_location = os.path.join(__location__, "Convert_From_Txt")
converted_to_folder_location = os.path.join(__location__, "Converted_To_Csv")
print(converted_to_folder_location)
for file in os.listdir(convert_from_folder_location):
    print(file)
    file_name_main = file[:-4]
    file_read = pd.read_csv(os.path.join(convert_from_folder_location, file), delimiter="\t")
    file_read.to_csv(converted_to_folder_location + "\\" + file_name_main + ".csv", sep = ",", index = None)


# To use, please txt files that you would like to convert to csv into "Convert_From_Txt" folder
# Then run program
# Converted files will be saved to "Converted_To_Csv" folder