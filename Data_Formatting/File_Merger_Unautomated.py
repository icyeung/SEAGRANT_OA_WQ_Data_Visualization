import pandas as pd

d1 = pd.read_csv("C:\\Users\\isabe\Desktop\\File Data\\pCO2SAMI Data Export_20210802")
d2 = pd.read_csv("C:\\Users\\isabe\Desktop\\File Data\\pCO2SAMI Data Export_20210928")
d3 = pd.read_csv("C:\\Users\\isabe\Desktop\\File Data\\pCO2SAMI Data Export_20211210")
 
new_file = pd.concat([d1,d2,d3])

new_file.to_csv("C:\\Users\\isabe\\Desktop\\Test1.txt", index=False, header=True)

print(new_file)