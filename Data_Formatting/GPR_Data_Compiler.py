import pandas as pd


# Creates dataframes of data grapher without outliers
pco2DF = pd.DataFrame({"Date": xDataTrueNO, "Temperature (C)": extractedData.get("Temp"), 
                       "CO2": extractedData.get("CO2"), "Battery": extractedData.get("Battery")})

weatherDF = pd.DataFrame({"Date": weaDateTrue, "Wind Speed (mph)": wyData, "Rainfall (in)": ryData})

tideDF = pd.DataFrame({"Date": tidDateTrue, "Height (ft)": tidHeightData})


# Saves dataframes to csv files
pco2DF.to_excel("pco2_Data_Compiled.xlsx")

pco2DF['Date'] = pd.to_datetime(pco2DF['Date'])

weatherDF.to_excel("weather_Data_Compiled.xlsx")

weatherDF['Date'] = pd.to_datetime(weatherDF['Date'])

tideDF.to_excel("tide_Data_Compiled.xlsx")
'''
mergedDF = pd.merge_asof(pco2DF, weatherDF, on="Date", tolerance=pd.Timedelta("1d"), allow_exact_matches=True)
mergedDF = pd.merge_asof(mergedDF, tideDF, on="Date", tolerance=pd.Timedelta("1ms"), allow_exact_matches=False)
'''

mergedDF = pd.concat([pco2DF,weatherDF,tideDF], axis=0, ignore_index=True)

mergedDF.to_excel("merge_tester.xlsx")
print(mergedDF)
